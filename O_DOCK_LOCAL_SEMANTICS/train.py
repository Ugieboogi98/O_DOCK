"""QLoRA SFT on reviewed examples. Training dependencies stay outside backend."""
import argparse
import hashlib
import json
from pathlib import Path


def load_rows(path, allow_silver=False):
    rows = [json.loads(s) for s in path.read_text(encoding='utf-8').splitlines() if s.strip()]
    if not rows:
        raise ValueError('EMPTY_DATASET')
    if not allow_silver and any(r.get('reviewed') is not True or not r.get('reviewer') for r in rows):
        raise ValueError('UNREVIEWED_LABELS: review labels and record reviewer, or explicitly use --allow-silver for an experimental model')
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--model', default='Qwen/Qwen3-4B-Instruct-2507')
    p.add_argument('--revision', default='main')
    p.add_argument('--max-length', type=int, default=4096)
    p.add_argument('--epochs', type=float, default=2)
    p.add_argument('--allow-silver', action='store_true')
    p.add_argument('--max-steps', type=int, default=-1)
    p.add_argument('--gradient-accumulation-steps', type=int, default=8)
    p.add_argument('--initial-adapter', type=Path)
    p.add_argument('--learning-rate', type=float, default=1e-4)
    args = p.parse_args()
    train_rows = load_rows(args.data / 'train.jsonl', args.allow_silver)
    eval_rows = load_rows(args.data / 'validation.jsonl', args.allow_silver)
    # Also check the untouched test set exists and was split before training.
    test_rows = load_rows(args.data / 'test.jsonl', args.allow_silver)
    manifest = json.loads((args.data / 'manifest.json').read_text(encoding='utf-8'))
    if args.output.exists() and any(args.output.iterdir()):
        p.error('Use a new model output directory')
    from dataset import components
    combined = [dict(r, _split=part) for part, rows in [('train', train_rows), ('validation', eval_rows), ('test', test_rows)] for r in rows]
    if any(len({r['_split'] for r in group}) > 1 for group in components(combined)):
        p.error('DATA_LEAKAGE_ACROSS_SPLITS')
    import torch
    from datasets import Dataset
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, Trainer, TrainingArguments, DataCollatorForSeq2Seq
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, PeftModel
    if not torch.cuda.is_available():
        p.error('CUDA GPU required for this QLoRA recipe')
    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    tokenizer = AutoTokenizer.from_pretrained(args.model, revision=args.revision, trust_remote_code=False)
    tokenizer.pad_token = tokenizer.eos_token
    def encode(row):
        messages = [{'role': 'system', 'content': manifest['instruction']},
                    {'role': 'user', 'content': json.dumps(row['source'], ensure_ascii=False)}]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
        completion = json.dumps(row['result'], ensure_ascii=False) + tokenizer.eos_token
        prefix = tokenizer(prompt, add_special_tokens=False)['input_ids']
        suffix = tokenizer(completion, add_special_tokens=False)['input_ids']
        if len(prefix) + len(suffix) > args.max_length:
            raise ValueError(f"TRAINING_EXAMPLE_TOO_LONG:{row['figure_id']}; select evidence or raise max length, never truncate labels")
        return {'input_ids': prefix + suffix, 'attention_mask': [1] * (len(prefix) + len(suffix)),
                'labels': [-100] * len(prefix) + suffix}
    train_set = Dataset.from_list([encode(r) for r in train_rows])
    eval_set = Dataset.from_list([encode(r) for r in eval_rows])
    model = AutoModelForCausalLM.from_pretrained(args.model, revision=args.revision, trust_remote_code=False,
        device_map={'': 0}, torch_dtype=dtype, attn_implementation='sdpa',
        quantization_config=BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=dtype))
    model = prepare_model_for_kbit_training(model)
    model.config.use_cache = False
    if args.initial_adapter:
        model = PeftModel.from_pretrained(model, str(args.initial_adapter), is_trainable=True)
    else:
        model = get_peft_model(model, LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05,
            target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj', 'gate_proj', 'up_proj', 'down_proj'], task_type='CAUSAL_LM'))
    options = TrainingArguments(output_dir=str(args.output), num_train_epochs=args.epochs,
        per_device_train_batch_size=1, per_device_eval_batch_size=1, gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate, gradient_checkpointing=True, bf16=dtype == torch.bfloat16,
        fp16=dtype == torch.float16, logging_steps=5, eval_strategy='epoch', save_strategy='epoch',
        save_total_limit=2, report_to='none', seed=20261111, max_steps=args.max_steps)
    trainer = Trainer(model=model, args=options, train_dataset=train_set, eval_dataset=eval_set,
        data_collator=DataCollatorForSeq2Seq(tokenizer, padding=True, label_pad_token_id=-100))
    trainer.train()
    trainer.save_model(str(args.output))
    tokenizer.save_pretrained(args.output)
    import importlib.metadata
    record = {'base_model': args.model, 'resolved_revision': model.config._commit_hash,
        'training_args': vars(args) | {'data': str(args.data), 'output': str(args.output),
                                      'initial_adapter': str(args.initial_adapter) if args.initial_adapter else None},
        'dataset_hashes': {name: hashlib.sha256((args.data / name).read_bytes()).hexdigest()
                           for name in ('train.jsonl', 'validation.jsonl', 'test.jsonl', 'manifest.json')},
        'packages': {name: importlib.metadata.version(name) for name in ('torch', 'transformers', 'peft', 'bitsandbytes')},
        'status': 'experimental_silver' if args.allow_silver else 'trained_not_yet_evaluated'}
    (args.output / 'training_manifest.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
