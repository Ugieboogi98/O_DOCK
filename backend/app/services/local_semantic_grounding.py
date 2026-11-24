"""Source-bound candidates for local inference, independent of model guesses."""
import re
import json
from pathlib import Path
from app.services.reference_classifier import cached_record


def candidates(source):
    complete = {'official_url': '', 'type': 'figure', **source}
    record = cached_record(complete, '', 0) or {'patch': {}, 'proofs': {}}
    patch = record['patch']
    work = None
    if patch.get('franchise_ko'):
        proof = record['proofs']['franchise_ko'][0]
        work = {'original': proof['match'], 'ko': patch['franchise_ko'],
                'evidence_field': proof['field'], 'evidence': proof['match'], 'confidence': 1}
    characters = [{k: row[k] for k in ('original', 'ko', 'evidence_field', 'evidence')} | {'confidence': 1}
                  for row in patch.get('character_ko', [])]
    if work is None:
        from app.services.reference_classifier import work_match
        groups = json.loads(Path(__file__).with_name('local_semantic_domain_extension.json').read_text(encoding='utf-8'))['groups']
        hits = []
        for group in groups:
            for field in ('franchise', 'name_original'):
                for alias in group['aliases']:
                    found = work_match(alias, source.get(field) or '')
                    if found:
                        hits.append((field == 'franchise', len(alias), found, group['work'], field))
        if hits:
            _, _, original, ko, field = max(hits)
            work = {'original': original, 'ko': ko, 'evidence_field': field,
                    'evidence': original, 'confidence': 1}
    form = explicit_form(source)
    if form is None and patch.get('figure_form'):
        proof = record['proofs']['figure_form'][0]
        if proof.get('verification') != 'stored_catalog_metadata':
            form = {'code': patch['figure_form'], 'evidence_field': proof['field'],
                    'evidence': proof['match'], 'confidence': 1}
    return {'franchise': work, 'characters': characters, 'figure_form': form}


def explicit_form(source):
    if (source.get('product_line') or '').startswith('フリューくじ'):
        return {'code': 'lottery_goods', 'evidence_field': 'product_line',
                'evidence': source['product_line'], 'confidence': 1}
    patterns = [
        ('figure_parts', r'ポンチョ|おようふくセット|専用台座|オプションパーツセット'),
        ('model_kit', r'プラキット|プラモデル|組み立てキット'),
        ('plush', r'ぬいぐるみ|plush|봉제인형'),
        ('noodle_stopper', r'ぬーどるストッパー|ヌードルストッパー|Noodle Stopper|누들\s?스토퍼'),
        ('nendoroid', r'ねんどろいど|Nendoroid|넨도로이드'),
        ('acrylic_stand', r'アクリルスタンド|アクスタ|아크릴 스탠드'),
        ('keychain', r'キーホルダー|アクリルキーチェーン'),
        ('rubber_mascot', r'ラバーマスコット|ラバーストラップ'),
        ('action_figure', r'アクションフィギュア|可動フィギュア|action figure|액션 피규어'),
        ('chibi_figure', r'デフォルメフィギュア|るかっぷ|\bLook Up\b'),
        ('soft_vinyl', r'ソフビ|ソフトビニール'),
        ('mini_figure', r'ミニフィギュア|ミニサイズ|\[mini\]'),
        ('scale_figure', r'(?<![0-9０-９/／])[1１]\s*[/／]\s*[0-9０-９]+(?![0-9０-９/／])'),
        ('non_scale_figure', r'ノンスケールフィギュア'),
        ('completed_figure', r'彩色済み完成品フィギュア|塗装済み完成品フィギュア'),
    ]
    for field in ('name_original', 'scale', 'product_line', 'document_0', 'document_1', 'document_2'):
        value = source.get(field) or ''
        if field.startswith('document_'):
            try:
                payload = json.loads(value)
            except (ValueError, TypeError):
                payload = None
            if isinstance(payload, dict):
                # A brand page's complete text can advertise unrelated products.
                # Use actual description/specifications, never an arbitrary page dump.
                selected = []
                description = payload.get('description')
                if isinstance(description, str) and description in value:
                    selected.append(description)
                specs = payload.get('specifications', {})
                if isinstance(specs, dict):
                    for item in specs.values():
                        values = item if isinstance(item, list) else [item]
                        selected.extend(text for text in values if isinstance(text, str) and text in value)
                value = '\n'.join(selected)
            value = re.split(r'※|別売|関連商品|おすすめ', value, maxsplit=1)[0]
        for code, pattern in patterns:
            hit = re.search(pattern, value, re.I)
            if hit:
                if code == 'scale_figure' and field.startswith('document_') and not re.match(r'\s*(?:スケール|scale\b)', value[hit.end():], re.I):
                    continue
                # A negative statement does not establish a product form.
                vicinity = value[hit.end():hit.end() + 12]
                if re.match(r'(?:では(?:あり)?ません|ではない|でない|非対応)', vicinity):
                    continue
                return {'code': code, 'evidence_field': field, 'evidence': hit.group(), 'confidence': 1}
    return None
