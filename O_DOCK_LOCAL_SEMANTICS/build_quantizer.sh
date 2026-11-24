#!/usr/bin/env bash
set -euo pipefail
python -m pip install 'cmake>=3.24,<4' 'ninja>=1.11,<2'
cmake -S /work/vendor/llama.cpp -B /tmp/odock-llama-build -G Ninja \
  -DGGML_CUDA=OFF -DBUILD_SHARED_LIBS=OFF -DLLAMA_BUILD_SERVER=OFF \
  -DLLAMA_CURL=OFF -DGGML_NATIVE=OFF
cmake --build /tmp/odock-llama-build --target llama-quantize -j 2
mkdir -p /work/models/tools
cp /tmp/odock-llama-build/bin/llama-quantize /work/models/tools/llama-quantize
git -C /work/vendor/llama.cpp rev-parse HEAD > /work/models/tools/llama_cpp_revision.txt
