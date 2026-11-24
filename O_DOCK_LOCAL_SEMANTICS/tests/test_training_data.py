import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import dataset
from train import load_rows
from evaluate import score


class TrainingDataTests(unittest.TestCase):
    def test_recovered_fields_cannot_leave_null_training_targets(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            reports = root / 'responses'
            reports.mkdir()
            record = {'figure_id': 1, 'source': {'name_original': 'フリーレン ぬーどるストッパー',
                'manufacturer': 'FuRyu', 'product_line': None,
                'document_0': '『葬送のフリーレン』より「フリーレン」が登場します。'},
                'result': {'name_ko': '프리렌 누들 스토퍼', 'franchise': None, 'characters': [], 'figure_form': None}}
            (reports / '1.json').write_text(json.dumps(record), encoding='utf-8')
            with patch.object(sys, 'argv', ['dataset', '--reports', str(reports), '--output', str(root / 'data')]):
                dataset.main()
            manifest = json.loads((root / 'data/manifest.json').read_text(encoding='utf-8'))
            self.assertEqual(manifest['counts']['needs_review'], 1)
            self.assertEqual(manifest['counts']['train'], 0)
    def test_extra_character_reduces_precision_and_missing_prediction_is_failure(self):
        gold = [{'figure_id': 1, 'expected': {'franchise_ko': '나루토', 'characters': ['나루토'], 'figure_form': 'action_figure'}}]
        predictions = [{'figure_id': 1, 'fields': {'franchise_ko': '나루토',
            'characters': [{'ko': '나루토'}, {'ko': '사스케'}], 'figure_form': 'action_figure', 'translation_status': 'ready'}}]
        metrics = score(gold, predictions)
        self.assertEqual(metrics['character_precision'], 0.5)
        self.assertEqual(metrics['character_recall'], 1)
        self.assertEqual(score(gold, [])['validated_prediction_rate'], 0)
    def test_reissues_and_url_and_description_remain_in_same_split(self):
        rows = [{'source': {'name_original': 'フィギュア【再販】', 'official_url': 'https://a/1'}},
                {'source': {'name_original': 'フィギュア', 'official_url': 'https://b/2'}},
                {'source': {'name_original': '別名', 'official_url': 'https://b/2', 'document_0': 'x' * 200}},
                {'source': {'name_original': '別商品', 'document_0': 'x' * 200}}]
        splits = dataset.split_rows(rows)
        self.assertEqual(sorted(len(v) for v in splits.values()), [0, 0, 4])

    def test_teacher_labels_not_automatically_gold(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'train.jsonl'
            path.write_text(json.dumps({'reviewed': False}), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'UNREVIEWED_LABELS'):
                load_rows(path)
            self.assertEqual(len(load_rows(path, allow_silver=True)), 1)

    def test_approved_labels_require_reviewer(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'train.jsonl'
            path.write_text(json.dumps({'reviewed': True}), encoding='utf-8')
            with self.assertRaises(ValueError):
                load_rows(path)
            path.write_text(json.dumps({'reviewed': True, 'reviewer': 'human-reviewer'}), encoding='utf-8')
            self.assertEqual(len(load_rows(path)), 1)


if __name__ == '__main__':
    unittest.main()
