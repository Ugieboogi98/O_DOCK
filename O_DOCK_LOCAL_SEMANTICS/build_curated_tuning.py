"""Agent-audited synthetic SFT labels plus corrected development examples.

These labels are not human-reviewed independent accuracy gold.
"""
import hashlib
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'backend'))
from app.services.ollama_semantics import prepare_input
from dataset import components, family, write_jsonl

PAIRS = [
    ('NARUTO-ナルト- 疾風伝', '나루토 질풍전', 'うちはイタチ', '우치하 이타치'),
    ('NARUTO-ナルト- 疾風伝', '나루토 질풍전', 'うずまきナルト', '우즈마키 나루토'),
    ('NARUTO-ナルト- 疾風伝', '나루토 질풍전', 'うちはサスケ', '우치하 사스케'),
    ('BLEACH', '블리치', '黒崎一護', '쿠로사키 이치고'),
    ('BLEACH', '블리치', '朽木ルキア', '쿠치키 루키아'),
    ('葬送のフリーレン', '장송의 프리렌', 'フリーレン', '프리렌'),
    ('葬送のフリーレン', '장송의 프리렌', 'フェルン', '페른'),
    ('ぼっち・ざ・ろっく！', '봇치 더 록!', '後藤ひとり', '고토 히토리'),
    ('ぼっち・ざ・ろっく！', '봇치 더 록!', '喜多郁代', '키타 이쿠요'),
    ('デート・ア・ライブ', '데이트 어 라이브', '時崎狂三', '토키사키 쿠루미'),
    ('デート・ア・ライブ', '데이트 어 라이브', '夜刀神十香', '야토가미 토카'),
    ('HUNTER×HUNTER', '헌터×헌터', 'クラピカ', '크라피카'),
    ('その着せ替え人形は恋をする', '그 비스크 돌은 사랑을 한다', '喜多川海夢', '키타가와 마린'),
    ('その着せ替え人形は恋をする', '그 비스크 돌은 사랑을 한다', '五条新菜', '고죠 와카나'),
    ('機動戦士ガンダム', '기동전사 건담', 'シャア・アズナブル', '샤아 아즈나블'),
    ('魔法少女まどか☆マギカ', '마법소녀 마도카☆마기카', '鹿目まどか', '카나메 마도카'),
    ('魔動王グランゾート', '그랑죠', 'ウインザート', '윈자트'),
    ('魔動王グランゾート', '그랑죠', 'アクアビート', '아쿠아비트'),
]
FORMS = [
    ('ぬいぐるみ', '봉제인형', 'plush'),
    ('ぬーどるストッパーフィギュア', '누들 스토퍼 피규어', 'noodle_stopper'),
    ('1/7スケールフィギュア', '1/7 스케일 피규어', 'scale_figure'),
    ('アクションフィギュア', '액션 피규어', 'action_figure'),
    ('デフォルメフィギュア', '데포르메 피규어', 'chibi_figure'),
    ('ねんどろいど', '넨도로이드', 'nendoroid'),
    ('アクリルスタンド', '아크릴 스탠드', 'acrylic_stand'),
    ('ソフビ', '소프비', 'soft_vinyl'),
    ('ミニフィギュア', '미니 피규어', 'mini_figure'),
    ('アクリルキーチェーン', '아크릴 키체인', 'keychain'),
    ('フィギュア', '피규어', None),
    ('クラシカルワンピースver.', '클래식 원피스 버전', None),
]


def entity(original, ko):
    return {'original': original, 'ko': ko, 'evidence_field': 'name_original', 'evidence': original, 'confidence': 1}


def main():
    target = ROOT / 'data/curated_tuning_20261111'
    if target.exists():
        raise RuntimeError('CURATED_DATASET_EXISTS')
    rows = []
    for index, (work, work_ko, person, person_ko) in enumerate(PAIRS):
        for n, (term, term_ko, code) in enumerate(FORMS):
            title = f'{work} {person} {term}' + ('【再販】' if n % 2 else '')
            source = {'name_original': title, 'manufacturer': 'Example', 'manufacturer_ko': '예시',
                      'product_line': None, 'franchise': None, 'character': None,
                      'scale': '1/7' if code == 'scale_figure' else None, 'type': 'figure',
                      'official_url': f'https://example.invalid/synthetic/{index}/{n}',
                      'document_0': '全高約110mm。スケール感をお楽しみください。' if code is None else None}
            result = {'name_ko': f'{work_ko} {person_ko} {term_ko}' + ('【재판】' if n % 2 else ''),
                      'franchise': entity(work, work_ko), 'characters': [entity(person, person_ko)],
                      'figure_form': {'code': code, 'evidence_field': 'name_original', 'evidence': term, 'confidence': 1} if code else None}
            prepared = prepare_input(source)
            # Ground-truth synthetic names are supplied as source-local hints, just as at inference.
            prepared['_canonical_aliases'] = [{'kind': 'franchises', 'original': work, 'ko': work_ko},
                                              {'kind': 'characters', 'original': person, 'ko': person_ko}]
            prepared['_grounded_candidates'] = {k: result[k] for k in ('franchise', 'characters', 'figure_form')}
            # This is source-only lexical preprocessing, not the target title.
            from app.services.local_semantic_lexicon import translation_input
            prepared['_translation_input'] = translation_input(source, prepared['_canonical_aliases'])
            rows.append({'figure_id': f'synthetic-{index}-{n}', 'source': prepared, 'result': result,
                         'reviewed': True, 'reviewer': 'Codex agent: explicit template audit',
                         'label_origin': 'agent_curated_synthetic_not_human_gold'})
    parts = {'train': [], 'validation': [], 'test': []}
    for group in components(rows):
        bucket = int(hashlib.sha256(min(family(r['source']) for r in group).encode()).hexdigest()[:8], 16) % 10
        part = 'test' if bucket == 0 else 'validation' if bucket == 1 else 'train'
        parts[part].extend(group)
    for part, values in parts.items():
        write_jsonl(target / (part + '.jsonl'), values)
    instruction = (ROOT.parent / 'backend/app/services/local_semantic_prompt.txt').read_text(encoding='utf-8')
    manifest = {'instruction': instruction, 'base_model': 'Qwen/Qwen3-8B',
                'counts': {part: len(values) for part, values in parts.items()},
                'label_scope': 'agent-reviewed synthetic task adaptation; independent real-product evaluation required',
                'human_reviewed_gold_count': 0, 'heldout_real_sources': 'reports/holdout_sources_20261111.json'}
    (target / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(manifest['counts']))


if __name__ == '__main__':
    main()
