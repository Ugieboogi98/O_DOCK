"""Keep the frontend classification choices synchronized with backend taxonomy."""
import json
from pathlib import Path
import re
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
from app.services.semantic_rules import FORMS
(ROOT / 'frontend/src/services/figure_forms.json').write_text(json.dumps(FORMS, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
path = ROOT / 'frontend/src/views/FigureListView.vue'
text = path.read_text(encoding='utf-8')
if 'import figureForms ' not in text:
    text = text.replace('<script setup>', "<script setup>\nimport figureForms from '../services/figure_forms.json'", 1)
text = re.sub(r'<option value="noodle_stopper">.*?<option value="acrylic_stand">.*?</option>',
    '<option v-for="(label,code) in figureForms" :key="code" :value="code">{{label}}</option>', text, count=1, flags=re.DOTALL)
path.write_text(text, encoding='utf-8')
print(json.dumps({'figure_form_choices': len(FORMS)}))
