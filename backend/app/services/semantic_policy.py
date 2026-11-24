"""Publication decisions for independently validated semantic fields.

Only sanitized values are stored in searchable fields. Rejected proposals remain
in the input report; issue codes and field states remain available for review.
"""

FIELDS = ('name_ko', 'franchise_ko', 'character_ko', 'figure_form')


def publication_status(fields, issues):
    states = fields.get('field_status')
    if not states:
        # Legacy/structurally invalid results cannot use the field policy.
        return 'review' if issues else ('partial' if fields.get('missing_fields') else 'ready')
    if all(state in ('ready', 'not_applicable') for state in states.values()):
        return 'ready'
    return 'partial' if any(state in ('ready', 'not_applicable') for state in states.values()) else 'review'


def finalize(fields, field_issues):
    """Remove an entire uncertain field, including its evidence and list aliases."""
    states = {}
    for key in FIELDS:
        errors = field_issues[key]
        states[key] = 'review' if errors else ('ready' if fields.get(key) else 'missing')
        if errors:
            fields[key] = None
            if key == 'character_ko':
                fields['characters'] = []
            if key == 'figure_form':
                fields['figure_form_ko'] = None
            evidence_key = {'franchise_ko': 'franchise', 'character_ko': 'characters',
                            'figure_form': 'figure_form'}.get(key)
            fields['evidence'].pop(evidence_key, None)
    fields['field_status'] = states
    fields['field_issues'] = field_issues
    fields['missing_fields'] = [key for key in FIELDS if key != 'name_ko' and not fields.get(key)]
    fields['translation_status'] = states['name_ko']
    classification = [states[key] for key in FIELDS if key != 'name_ko']
    fields['classification_status'] = ('review' if 'review' in classification else
                                       'partial' if 'missing' in classification else 'ready')
    return fields
