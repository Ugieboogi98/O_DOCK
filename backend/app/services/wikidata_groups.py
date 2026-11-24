"""Merge Wikidata work/character labels under the curated dictionary.

The pipeline treats two Korean labels for one Japanese alias as ambiguous and then uses neither,
so Wikidata must never contradict a curated entry:

* a Wikidata work whose alias is already claimed by a curated or verified work is folded into
  that work (its characters keep the curated work's Korean title, its aliases are dropped);
* a Wikidata character whose name the curated groups already map for that work is dropped;
* a Japanese alias that two Wikidata works claim with different Korean titles is dropped.
"""
from collections import defaultdict

from app.services.semantic_rules import normalize


def _names(names):
    return names.split('|') if isinstance(names, str) else list(names)


def merge(curated_groups, known_works, wikidata_groups):
    claimed = {}
    for w in known_works:
        for alias in [w.get('ko'), *w.get('aliases', [])]:
            if alias:
                claimed.setdefault(normalize(alias), w['ko'])
    for g in curated_groups:
        for alias in [g['work'], *g.get('aliases', [])]:
            claimed.setdefault(normalize(alias), g['work'])
    curated_names = defaultdict(set)
    for g in curated_groups:
        for names, _ in g.get('characters', []):
            curated_names[normalize(g['work'])] |= {normalize(n) for n in _names(names)}

    # Aliases Wikidata itself gives to different Korean titles are unusable.
    owners = defaultdict(set)
    for g in wikidata_groups:
        for alias in g.get('aliases', []):
            owners[normalize(alias)].add(g['work'])
    contested = {a for a, works in owners.items() if len(works) > 1}

    merged = {}
    for g in wikidata_groups:
        aliases = [a for a in g.get('aliases', []) if normalize(a) not in contested]
        target = next((claimed[normalize(a)] for a in [g['work'], *aliases] if normalize(a) in claimed), None)
        work = target or g['work']
        out = merged.setdefault(work, {'work': work, 'medium': g.get('medium'), 'aliases': [], 'characters': [],
                                       'wikidata': [], 'provenance': 'wikidata'})
        out['medium'] = out['medium'] or g.get('medium')
        if not target:
            out['aliases'] = list(dict.fromkeys([*out['aliases'], *aliases]))
        out['wikidata'] += g.get('wikidata', [])
        seen = curated_names[normalize(work)] | {normalize(n) for names, _ in out['characters'] for n in _names(names)}
        for names, ko in g.get('characters', []):
            names = _names(names)
            if not any(normalize(n) in seen for n in names):
                out['characters'].append([names, ko])
                seen |= {normalize(n) for n in names}
    return [g for g in merged.values() if g['characters'] or g['aliases']]
