"""Merge an evaluated adapter into its exact original base before GGUF export."""
import argparse
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--adapter', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    # Full CPU PEFT merge exceeded the 15 GiB Docker VM during the 8B run.
    # Prefer the bounded shard merge; never retry the full allocation blindly.
    memory_limits = []
    info = Path('/proc/meminfo')
    if info.exists():
        for line in info.read_text().splitlines():
            if line.startswith('MemAvailable:'):
                memory_limits.append(int(line.split()[1]) * 1024)
    for filename in ('/sys/fs/cgroup/memory.max', '/sys/fs/cgroup/memory/memory.limit_in_bytes'):
        file = Path(filename)
        if file.exists() and file.read_text().strip().isdigit():
            memory_limits.append(int(file.read_text().strip()))
    if not memory_limits or min(memory_limits) < 32 * 1024**3:
        p.error('Full merge requires at least 32 GiB verified available RAM. Use merge_adapter_streaming.py with a memory cap.')
    manifest = json.loads((args.adapter / 'training_manifest.json').read_text(encoding='utf-8'))
    if args.output.exists() and any(args.output.iterdir()):
        p.error('Output directory must be empty')
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from peft import PeftModel
    model = AutoModelForCausalLM.from_pretrained(manifest['base_model'],
        revision=manifest['resolved_revision'], torch_dtype=torch.float16,
        device_map='cpu', trust_remote_code=False)
    model = PeftModel.from_pretrained(model, args.adapter).merge_and_unload()
    model.save_pretrained(args.output, safe_serialization=True)
    AutoTokenizer.from_pretrained(args.adapter).save_pretrained(args.output)
    (args.output / 'odock_training_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
