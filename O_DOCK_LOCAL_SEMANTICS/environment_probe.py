"""Print package/GPU availability without changing the environment."""
import importlib.util
import json
print(json.dumps({name: bool(importlib.util.find_spec(name))
                  for name in ('torch', 'transformers', 'peft', 'bitsandbytes', 'datasets', 'accelerate')}))
if importlib.util.find_spec('torch'):
    import torch
    print(torch.__version__, torch.cuda.is_available())
    if torch.cuda.is_available():
        print(torch.cuda.get_device_name(), torch.cuda.get_device_capability())
