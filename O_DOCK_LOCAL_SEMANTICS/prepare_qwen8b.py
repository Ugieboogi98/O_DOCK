"""Download the exact public 8B base for a separate experimental adapter."""
from huggingface_hub import snapshot_download
path = snapshot_download('Qwen/Qwen3-8B', cache_dir='/work/training_cache',
                         allow_patterns=['*.json', '*.safetensors', '*.txt', '*.model', '*.jinja'])
print(path, flush=True)
