"""Merge standard linear LoRA weights one original shard at a time on CPU."""
import argparse
import gc
import hashlib
import json
from pathlib import Path
import shutil


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base', type=Path, required=True)
    p.add_argument('--adapter', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        p.error('Use an empty output directory')
    import torch
    from safetensors import safe_open
    from safetensors.torch import load_file, save_file
    torch.set_num_threads(4)
    config = json.loads((args.adapter / 'adapter_config.json').read_text(encoding='utf-8'))
    if any(config.get(key) for key in ('use_dora', 'use_rslora', 'rank_pattern', 'alpha_pattern', 'modules_to_save', 'fan_in_fan_out')):
        p.error('Only audited standard linear LoRA is supported')
    lora_path = args.adapter / 'adapter_model.safetensors'
    lora = load_file(str(lora_path), device='cpu')
    scale = config['lora_alpha'] / config['r']
    pairs = {}
    for name, value in lora.items():
        if name.endswith('.lora_A.weight'):
            stem = name.removesuffix('.lora_A.weight')
            base_key = stem.removeprefix('base_model.model.') + '.weight'
            pairs[base_key] = (value, lora[stem + '.lora_B.weight'])
        elif not name.endswith('.lora_B.weight'):
            raise RuntimeError('UNSUPPORTED_ADAPTER_TENSOR:' + name)
    index = json.loads((args.base / 'model.safetensors.index.json').read_text(encoding='utf-8'))
    args.output.mkdir(parents=True, exist_ok=True)
    merged = set()
    for shard in sorted(set(index['weight_map'].values())):
        output = {}
        with safe_open(str(args.base / shard), framework='pt', device='cpu') as reader:
            for name in reader.keys():
                tensor = reader.get_tensor(name)
                if name in pairs:
                    first, second = pairs[name]
                    delta = (second.float() @ first.float()) * scale
                    if tuple(delta.shape) != tuple(tensor.shape):
                        raise RuntimeError('ADAPTER_SHAPE_MISMATCH:' + name)
                    tensor = (tensor.float() + delta).to(tensor.dtype).contiguous()
                    merged.add(name)
                    del delta
                output[name] = tensor
            save_file(output, str(args.output / shard), metadata={'format': 'pt'})
        del output, tensor
        gc.collect()
        print(json.dumps({'shard': shard, 'merged_linear_weights': len(merged)}), flush=True)
    if merged != set(pairs):
        raise RuntimeError('UNMERGED_ADAPTER_WEIGHTS')
    for path in args.base.iterdir():
        if path.is_file() and path.suffix in ('.json', '.txt', '.model', '.jinja'):
            shutil.copy2(path, args.output / path.name)
    for name in ('tokenizer.json', 'tokenizer_config.json', 'special_tokens_map.json', 'added_tokens.json', 'chat_template.jinja'):
        path = args.adapter / name
        if path.exists():
            shutil.copy2(path, args.output / name)
    manifest = json.loads((args.adapter / 'training_manifest.json').read_text(encoding='utf-8'))
    manifest['merge'] = {'method': 'float32_delta_per_bf16_shard', 'weights': len(merged),
                         'adapter_sha256': hashlib.sha256(lora_path.read_bytes()).hexdigest()}
    (args.output / 'odock_training_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (args.output / 'MERGE_COMPLETE').write_text('complete\n', encoding='utf-8')


if __name__ == '__main__':
    main()
