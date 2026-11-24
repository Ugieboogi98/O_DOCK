"""Paired NF4 base/LoRA inference on frozen real sources, no DB writes."""
import argparse
from contextlib import nullcontext
import json
from pathlib import Path
import sys
import time
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'backend' if (ROOT.parent / 'backend').exists() else Path('/backend')))
from app.services.ollama_semantics import prepare_input
from app.services.local_semantic_lexicon import grounded_result
from app.services.semantic_rules import validate_result
from app.services.reference_classifier import cached_record


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sources', type=Path, required=True)
    p.add_argument('--adapter', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--batch-size', type=int, default=2)
    p.add_argument('--limit', type=int)
    p.add_argument('--adapter-only', action='store_true')
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    sources = json.loads(args.sources.read_text(encoding='utf-8'))['records']
    if args.limit:
        sources = sources[:args.limit]
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
    from peft import PeftModel
    manifest = json.loads((args.adapter / 'training_manifest.json').read_text(encoding='utf-8'))
    model_name, revision = manifest['base_model'], manifest['resolved_revision']
    tokenizer = AutoTokenizer.from_pretrained(model_name, revision=revision, trust_remote_code=False)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = 'left'
    base = AutoModelForCausalLM.from_pretrained(model_name, revision=revision, trust_remote_code=False,
        device_map={'': 0}, torch_dtype=torch.bfloat16, attn_implementation='sdpa',
        quantization_config=BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.bfloat16))
    model = PeftModel.from_pretrained(base, str(args.adapter))
    model.eval()
    instruction = Path('/backend/app/services/local_semantic_prompt.txt').read_text(encoding='utf-8')
    for mode in (['adapter'] if args.adapter_only else ['base', 'adapter']):
        path = args.output / f'{mode}.json'
        if path.exists():
            raise RuntimeError('EVALUATION_REPORT_ALREADY_EXISTS')
        report = {'mode': mode, 'backend': 'transformers_nf4', 'revision': revision,
                  'db_written': False, 'paid_api_called': False, 'records': []}
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        with (model.disable_adapter() if mode == 'base' else nullcontext()):
            for offset in range(0, len(sources), args.batch_size):
                batch = sources[offset:offset + args.batch_size]
                prompts = [tokenizer.apply_chat_template([
                    {'role': 'system', 'content': instruction},
                    {'role': 'user', 'content': json.dumps(prepare_input(r['source']), ensure_ascii=False)}],
                    tokenize=False, add_generation_prompt=True, enable_thinking=False) for r in batch]
                encoded = tokenizer(prompts, return_tensors='pt', padding=True).to('cuda')
                if encoded['input_ids'].shape[1] > 12000:
                    raise RuntimeError('EVALUATION_INPUT_TOO_LONG_NO_TRUNCATION')
                started = time.monotonic()
                with torch.inference_mode():
                    generated = model.generate(**encoded, max_new_tokens=1024, do_sample=False,
                                               pad_token_id=tokenizer.eos_token_id, use_cache=True)
                elapsed = time.monotonic() - started
                outputs = tokenizer.batch_decode(generated[:, encoded['input_ids'].shape[1]:], skip_special_tokens=True)
                for row, text in zip(batch, outputs):
                    record = {**row, 'raw_text': text, 'batch_seconds': round(elapsed, 3)}
                    try:
                        raw = json.loads(text.strip())
                        raw_fields, raw_issues = validate_result(row['source'], raw)
                        normalized = grounded_result(row['source'], raw)
                        fields, issues = validate_result(row['source'], normalized)
                        record.update(model_result=raw, raw_fields=raw_fields, raw_issues=raw_issues,
                            normalized_result=normalized, validated_fields=fields, issues=issues,
                            reference_patch=cached_record(row['source'], '', row['figure_id'], fields))
                    except Exception as error:
                        record['error'] = getattr(error, 'code', type(error).__name__)
                    report['records'].append(record)
                path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
                print(json.dumps({'mode': mode, 'completed': len(report['records']),
                                  'batch_seconds': round(elapsed, 2)}), flush=True)
    print('evaluation_complete', flush=True)


if __name__ == '__main__':
    main()
