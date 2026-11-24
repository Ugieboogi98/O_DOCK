import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from resolve_catalog import match, resolve, knowledge
from review_documents import generate, import_documents

REF = {'url': 'https://example.com/characters', 'evidence': 'name', 'checked_at': '2026-11-11'}


def row(title, franchise=None):
    return {'figure_id': 1, 'source_hash': 'hash', 'fields': {},
            'source': {'name_original': title, 'franchise': franchise, 'character': None,
                       'product_line': None, 'type': 'figure', 'scale': None, 'official_url': 'https://example.com/product'}}


class ResearchTests(unittest.TestCase):
    def test_character_design_category_does_not_make_figure_a_character(self):
        wiki = {'checked_at': 'today', 'entries': {'figure': {
            'url': REF['url'], 'evidence': 'figure', 'alias': '피규어', 'canonical': '피규어',
            'ko': '피규어', 'categories': ['분류:캐릭터 디자인'], 'seed_roles': ['character'], 'language': 'ko'}}}
        self.assertEqual(knowledge({'series': [], 'forms': []}, {}, wiki)[1], [])

    def test_official_work_canonicalization_precedes_long_wiki_variant(self):
        works = [
            {'ko': '번역 변형', 'aliases': ['無職転生Ⅱ ～異世界行ったら本気だす～'], 'priority': 1, 'reference': REF},
            {'ko': '무직전생', 'aliases': ['無職転生'], 'priority': 2, 'reference': REF}]
        result = resolve(row('無職転生Ⅱ ～異世界行ったら本気だす～ ロキシー'), works, [], [])
        self.assertEqual(result['patch']['franchise_ko'], '무직전생')

    def test_verified_single_character_replaces_incorrect_old_single_subject(self):
        item = row('オーバーロード アルベド')
        item['fields'] = {'characters': [{'original': 'フィギュア', 'ko': '피규어'}],
                          'field_status': {'character_ko': 'ready'}}
        works = [{'ko': '오버로드', 'aliases': ['オーバーロード'], 'priority': 2, 'reference': REF}]
        chars = [{'ko': '알베도', 'aliases': ['アルベド'], 'work': '오버로드', 'priority': 2, 'reference': REF}]
        self.assertEqual(resolve(item, works, chars, [])['patch']['character_ko'][0]['ko'], '알베도')

    def test_vs_opponent_is_not_the_product_subject(self):
        works = [{'ko': '드래곤볼 Z', 'aliases': ['드래곤볼 Z'], 'priority': 2, 'reference': REF}]
        characters = [{'ko': name, 'aliases': [name], 'work': '드래곤볼', 'priority': 2, 'reference': REF}
                      for name in ('손오공', '베지터')]
        result = resolve(row('드래곤볼 Z 손오공 (VS베지터)'), works, characters, [])
        self.assertEqual([c['ko'] for c in result['patch']['character_ko']], ['손오공'])

    def test_character_embedded_only_in_work_title_is_not_a_subject(self):
        works = [{'ko': '장송의 프리렌', 'aliases': ['葬送のフリーレン'], 'priority': 2, 'reference': REF}]
        characters = [{'ko': '프리렌', 'aliases': ['フリーレン'], 'work': '장송의 프리렌', 'priority': 2, 'reference': REF}]
        result = resolve(row('葬送のフリーレン フィギュア'), works, characters, [])
        self.assertNotIn('character_ko', result['patch'])

    def test_memory_and_surname_redirects_are_not_character_proofs(self):
        wiki = {'checked_at': 'today', 'entries': {
            'Ram': {'url': REF['url'], 'evidence': 'Ram -> RAM', 'alias': 'Ram', 'canonical': 'RAM',
                    'ko': '랜덤 액세스 메모리', 'categories': ['Computer memory'], 'seed_roles': ['character'], 'language': 'en'},
            '우치하': {'url': REF['url'], 'evidence': '우치하 -> 사스케', 'alias': '우치하', 'canonical': '우치하 사스케',
                    'ko': '우치하 사스케', 'categories': ['가공의 닌자'], 'seed_roles': ['character'], 'language': 'ko'}}}
        _, characters, _ = knowledge({'series': [], 'forms': []}, {}, wiki)
        self.assertEqual(characters, [])

    def test_normalization_keeps_exact_original_quotation_and_word_boundaries(self):
        self.assertEqual(match('Re:ゼロ', 'Re：ゼロ フィギュア'), 'Re：ゼロ')
        self.assertIsNone(match('셀', '셀맥스 피규어'))

    def test_editing_one_group_creates_scoped_manual_patches(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            a, b = row('Rare Hero A'), row('Rare Hero B')
            for i, item in enumerate((a, b), 1):
                item['figure_id'], item['source_hash'] = i, f'hash{i}'
                item['source']['character'] = 'Rare Hero'
                item['fields']['field_status'] = {'franchise_ko': 'ready', 'figure_form': 'ready', 'character_ko': 'missing'}
            manifest = generate({'records': [a, b]}, directory)
            self.assertEqual(manifest['group_count'], 1)
            path = directory / '02_CHARACTERS.md'
            text = path.read_text(encoding='utf-8').replace('"approved": false', '"approved": true').replace('"value": null', '"value": ["희귀 캐릭터"]')
            path.write_text(text, encoding='utf-8')
            patches = import_documents(directory)['records']
            self.assertEqual(len(patches), 2)
            self.assertEqual(patches[0]['patch']['character_ko'][0]['ko'], '희귀 캐릭터')
            self.assertEqual(patches[1]['source_hash'], 'hash2')


if __name__ == '__main__':
    unittest.main()
