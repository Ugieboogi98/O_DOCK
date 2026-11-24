"""Explicit post-output label errata; never overwrite the pre-output audit."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
source = root / 'samples/release_labels_v4_20261111.json'
target = root / 'samples/release_labels_v4_adjudicated_20261111.json'
if target.exists():
    raise RuntimeError('REFUSE_OVERWRITE')
data = json.loads(source.read_text(encoding='utf-8'))
notes = {
    146: 'Valid Korean localized family title; retain original score and report this post-output synonym adjudication.',
    787: 'Valid family title without GPX token; not a different work.',
    1426: 'Parser delimiter split Fate/kaleid incorrectly in pre-output annotation; explicit full title alternative restored.',
    4785: 'Movie subtitle without leading theatrical word denotes same source work.',
    1051: 'Original audit confused palm-sized te-no-hira with LookUp chibi. Source lacks explicit body type; allow abstention.',
    4754: 'Official specMaterial explicitly states 1/7 scale; original title-only form annotation omitted this.'}
alternatives = {146: '달의 요정 세일러문 (만화)', 787: '신세기 사이버 포뮬러',
                1426: 'Fate/kaleid liner 프리즈마☆이리야', 4785: '체인소 맨 레제편'}
for row in data['cases']:
    ident = row['id']
    if ident in alternatives:
        row['work'].append(alternatives[ident])
    if ident == 1051:
        row['forms'] = [None, 'completed_figure', 'non_scale_figure']
    if ident == 4754:
        row['forms'] = ['scale_figure']
    if ident in notes:
        row['post_output_adjudication'] = notes[ident]
data['post_output_adjudication'] = 'Six explicit label errata after inspecting outputs; original labels and scores retained. Do not describe adjusted metrics as a pristine pre-output audit.'
target.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
