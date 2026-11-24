import importlib.util
import json
from pathlib import Path
import sys
import pytest


def test_streamed_weights_match_peft_merge(tmp_path, monkeypatch):
    torch = pytest.importorskip('torch')
    peft = pytest.importorskip('peft')
    from safetensors.torch import save_file, load_file
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location('stream_merge', root / 'merge_adapter_streaming.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    class Toy(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.q_proj = torch.nn.Linear(3, 2, bias=False, dtype=torch.bfloat16)

        def forward(self, value):
            return self.q_proj(value)

    torch.manual_seed(42)
    toy = Toy()
    base, adapter, output = [tmp_path / name for name in ('base', 'adapter', 'output')]
    base.mkdir()
    shard = 'model-00001-of-00001.safetensors'
    save_file({'q_proj.weight': toy.q_proj.weight.detach().clone()}, str(base / shard))
    (base / 'model.safetensors.index.json').write_text(json.dumps({'weight_map': {'q_proj.weight': shard}}))
    wrapped = peft.get_peft_model(toy, peft.LoraConfig(r=2, lora_alpha=4, target_modules=['q_proj']))
    layer = wrapped.base_model.model.q_proj
    with torch.no_grad():
        layer.lora_A['default'].weight.copy_(torch.arange(6).reshape(2, 3) / 17)
        layer.lora_B['default'].weight.copy_(torch.arange(4).reshape(2, 2) / 13)
    wrapped.save_pretrained(adapter)
    (adapter / 'training_manifest.json').write_text('{}')
    expected = wrapped.merge_and_unload().q_proj.weight.detach().clone()
    monkeypatch.setattr(sys, 'argv', ['merge', '--base', str(base), '--adapter', str(adapter), '--output', str(output)])
    module.main()
    actual = load_file(str(output / shard))['q_proj.weight']
    assert torch.equal(actual, expected)
    assert (output / 'MERGE_COMPLETE').exists()
