"""Build a reviewable queue from saved evaluation artifacts, without model or DB calls."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
report = json.loads((root / 'reports/development_replay_v5b_20261111.json').read_text(encoding='utf-8'))
labels = {r['id']: r for r in json.loads((root / 'samples/release_labels_v4_adjudicated_20261111.json').read_text(encoding='utf-8'))['cases']}
lines = ['# 일본어 상품 번역·분류 검수 대기열', '',
    '에이전트 라벨과 제안값을 사람이 대조하기 위한 자료다. 운영 DB에는 적용하지 않았다. v5 개발용 재검사이며 독립 성능 인증이 아니다.', '',
    '정답 후보는 공식 한국어 표기를 보증하지 않는다. 미상은 검수 필요이며 캐릭터가 없다는 뜻이 아니다.', '']
ready = 0
for row in report['records']:
    f = row.get('validated_fields', {})
    title_ready = f.get('field_status', {}).get('name_ko') == 'ready'
    ready += title_ready
    lines += [f"## 상품 {row['figure_id']}", '', f"- 원문: {row['source']['name_original']}",
        f"- 출처: {row['source'].get('official_url', '')}",
        f"- 모델 원시 번역: {(row.get('model_result') or {}).get('name_ko')}",
        f"- 검증 후 번역: {f.get('name_ko')} / 상태: {f.get('field_status', {}).get('name_ko')}",
        f"- 검증 후 작품: {f.get('franchise_ko')}",
        f"- 검증 후 캐릭터: {', '.join(c['ko'] for c in f.get('characters', [])) or '미상'}",
        f"- 검증 후 형태: {f.get('figure_form')}",
        '- 에이전트 정답 후보: `' + json.dumps(labels[row['figure_id']], ensure_ascii=False) + '`',
        '- 경고: `' + json.dumps(row.get('issues', []), ensure_ascii=False) + '`', '']
lines.insert(6, f'번역 ready: {ready}/{len(report["records"])}. ready는 기계 검증 상태이며 사람의 의미 검수 통과가 아니다.')
target = root.parent / 'docs/reports/LOCAL_MODEL_TUNING_REVIEW_QUEUE_20261111.md'
target.write_text('\n'.join(lines), encoding='utf-8')
print(json.dumps({'records': len(report['records']), 'title_ready': ready}))
