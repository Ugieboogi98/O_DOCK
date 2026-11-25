"""Re-check stored web_verified name overrides against the word-boundary proof rule.

An earlier web pass accepted a proof term found anywhere in the title, so ルフィ inside
スケールフィギュア labelled dozens of unrelated scale figures 몽키 D. 루피. Overrides are never
replaced by the pipeline, so they have to be repaired here:

* a character whose proof is no longer valid is removed from the override;
* an override left without a valid proof is removed and the field cleared, so the next
  pipeline run (``--reprocess --ids-file``) decides it from the source again.

Manual (manual_verified) overrides are never touched. Dry run by default.

  python tools/run_split_semantics.py --repair-web-proofs --out ids.json [--apply]
"""
import argparse
import copy
import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified

from app.core.database import SessionLocal
from app.models.semantics import ProductSemantics
from app.services.semantic_policy import finalize, publication_status
from app.services.verified_classification import NAME_FIELDS, merge_overrides, standalone

EVIDENCE = {'franchise_ko': 'franchise', 'character_ko': 'characters'}


def valid(proof, source, key):
    return standalone(proof.get('match'), source.get(proof.get('field')), prefix=key == 'franchise_ko')


def repair(fields, source):
    """(new_fields, changes) — new_fields is None when nothing changed."""
    overrides = fields.get('classification_overrides') or {}
    out, changes = copy.deepcopy(fields), []
    for key in NAME_FIELDS:
        item = overrides.get(key)
        if not item or item.get('method') != 'web_verified':
            continue
        refs = item.get('evidence', {}).get('references', [])
        good = [p for p in refs if valid(p, source, key)]
        if len(good) == len(refs):
            continue
        item = copy.deepcopy(item)
        kept = None
        if key == 'character_ko':
            matches = {p.get('match') for p in good}
            kept = [c for c in item.get('characters') or [] if c.get('original') in matches]
        if good and (key != 'character_ko' or kept):
            item['evidence']['references'] = good
            if kept is not None:
                item['characters'] = kept
                item['value'] = ' · '.join(c['ko'] for c in kept)
            out['classification_overrides'][key] = item
            changes.append({'field': key, 'action': 'narrowed', 'from': overrides[key].get('value'), 'to': item['value']})
        else:
            del out['classification_overrides'][key]
            out[key] = None
            if key == 'character_ko':
                out['characters'] = []
            out.setdefault('evidence', {}).pop(EVIDENCE[key], None)
            changes.append({'field': key, 'action': 'removed', 'from': overrides[key].get('value')})
    if not changes:
        return None, []
    issues = {k: list(v) for k, v in (out.get('field_issues') or {}).items()}
    for k in ('name_ko', 'franchise_ko', 'character_ko', 'figure_form'):
        issues.setdefault(k, [])
    out = finalize(out, issues)
    if out.get('classification_overrides'):
        out = merge_overrides(out, out, next(iter(out['classification_overrides'].values()))['source_hash'])
    else:
        out.pop('classification_overrides', None)
    return out, changes


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--apply', action='store_true')
    p.add_argument('--out', type=Path, required=True, help='JSON list of repaired figure ids, for --reprocess --ids-file')
    a = p.parse_args()
    report = []
    with SessionLocal() as db:
        for profile in db.scalars(select(ProductSemantics).order_by(ProductSemantics.figure_id)):
            if not isinstance(profile.fields, dict) or not profile.fields.get('classification_overrides'):
                continue
            fields, changes = repair(profile.fields, profile.source or {})
            if not changes:
                continue
            report.append({'figure_id': profile.figure_id, 'title': (profile.source or {}).get('name_original'), 'changes': changes})
            if a.apply:
                profile.fields = fields
                flag_modified(profile, 'fields')
                profile.status = publication_status(fields, [])
        if a.apply:
            db.commit()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps([r['figure_id'] for r in report]), encoding='utf-8')
    print(json.dumps({'applied': a.apply, 'profiles': len(report), 'report': report}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
