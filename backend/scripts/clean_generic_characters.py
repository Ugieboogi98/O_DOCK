"""Remove demonstrably generic automated subjects, preserving manual decisions."""
import argparse
import copy
import json
import os
from pathlib import Path
from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.semantics import ProductSemantics
from app.models.entities import now
from app.services.reference_classifier import GENERIC_SUBJECTS
from app.services.semantic_policy import finalize, publication_status


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--journal', type=Path, required=True)
    p.add_argument('--commit', action='store_true')
    args = p.parse_args()
    args.journal.parent.mkdir(parents=True, exist_ok=True)
    changed = 0
    with args.journal.open('x', encoding='utf-8') as out, SessionLocal() as db:
        for profile in db.scalars(select(ProductSemantics).order_by(ProductSemantics.figure_id)):
            fields = copy.deepcopy(profile.fields)
            override = fields.get('classification_overrides', {}).get('character_ko', {})
            if override.get('method') == 'manual_verified':
                continue
            old_characters = fields.get('characters', [])
            remaining = [c for c in old_characters if c.get('ko') not in GENERIC_SUBJECTS]
            if len(remaining) == len(old_characters):
                continue
            out.write(json.dumps({'figure_id': profile.figure_id, 'previous_fields': profile.fields,
                'previous_status': profile.status, 'previous_issues': profile.issues,
                'removed': [c for c in old_characters if c not in remaining]}, ensure_ascii=False) + '\n')
            out.flush()
            os.fsync(out.fileno())
            fields.get('classification_overrides', {}).pop('character_ko', None)
            fields['characters'] = remaining
            fields['character_ko'] = ' · '.join(c['ko'] for c in remaining) or None
            fields.setdefault('evidence', {})['characters'] = {'method': 'generic_entity_cleanup',
                'reason': 'Product type or generic archetype is not an individual character'}
            errors = copy.deepcopy(fields.get('field_issues', {}))
            if not remaining:
                errors['character_ko'] = []
            fields = finalize(fields, errors)
            # Preserve other fields, including explicit not-applicable decisions.
            from app.services.verified_classification import merge_overrides
            fields = merge_overrides(fields, fields, profile.source_hash)
            profile.fields = fields
            profile.issues = [e for issues in fields['field_issues'].values() for e in issues]
            profile.status = publication_status(fields, [])
            profile.updated_at = now()
            changed += 1
        if args.commit:
            db.commit()
        else:
            db.rollback()
    print(json.dumps({'products': changed, 'committed': args.commit}))


if __name__ == '__main__':
    main()
