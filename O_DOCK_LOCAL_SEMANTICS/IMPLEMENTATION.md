# O_DOCK 로컬 번역·분류 구현

2026-11-11. 현재 앱은 v5 필드 검증 규칙을 사용한다. 기존 README와 VSCODE_TASK.md의 v4 현황은 스타터 작성 당시의 이력이다.

## 현재 구성

상품명 한국어 번역과 작품·캐릭터·형태 추출을 하나의 구조화 JSON 작업으로 수행한다. 제작사는 DB 값을 유지하고, 브랜드와 작품을 구분한다. 모델 출력은 기존 `semantic_rules`와 `semantic_policy`를 통과해야 DB의 검색·표시 필드에 반영된다. 근거 없는 값은 보류한다.

`backend/app/services/ollama_semantics.py`가 로컬 Ollama `/api/chat`을 사용한다. JSON Schema, think=false, 동시 추론 1개, 컨텍스트 16,384, 최대 출력 2,048 토큰으로 시작한다. 공급자·가중치 digest·프롬프트·스키마·원문/규칙을 원시 응답 캐시 키에 포함한다. 원시 JSON과 검증 후 필드는 구분되며, 과거 게시 내용은 재평가 보고서에 남긴다. 로컬 주소만 허용하고 유료 API로 전환하지 않는다.

기준 추론 모델은 스타터의 `qwen3:8b` Q4_K_M이다. 전용 LoRA 학습은 16GB GPU의 메모리를 고려해 별도의 `Qwen/Qwen3-4B-Instruct-2507`을 기본으로 준비했다. 8B 어댑터를 4B에 적용하는 구성이 아니다. 4B는 학습 전 기준점도 따로 측정해야 한다. 16GB에서 모든 학습 길이가 가능하다는 보장은 없으며 실제 학습 메모리 검증이 필요하다.

## 실제 모델 시험

프로젝트 루트에서:

```powershell
docker compose -f O_DOCK_LOCAL_SEMANTICS/compose.yaml up -d
docker compose -f O_DOCK_LOCAL_SEMANTICS/compose.yaml exec -T ollama ollama pull qwen3:8b
python O_DOCK_LOCAL_SEMANTICS/local_semantics.py health
```

앱 컨테이너에서 실행할 번역·분류 전용 설정은 다음과 같다. LLM_BASE_URL과 유료 키는 변경할 필요가 없다. 호스트 Python에서는 SEMANTIC_BASE_URL을 `http://127.0.0.1:11434`로 설정한다.

```dotenv
SEMANTIC_PROVIDER=ollama
SEMANTIC_MODEL=qwen3:8b
SEMANTIC_BASE_URL=http://host.docker.internal:11434
SEMANTIC_TIMEOUT=240
```

```powershell
docker compose build backend
docker compose run --rm --no-deps -e SEMANTIC_PROVIDER=ollama backend python -m scripts.product_semantics run --figure-ids 48,49,50,51,52 --limit 5 --refresh-local --report /app/media/local_semantic_reports/furyu_preview.json
```

위 명령은 추론·검증 보고서만 저장한다. `--commit`을 명시하거나 정식 보고서를 `product_semantics apply --report ...`로 적용해야 DB가 바뀐다. 기존 스타터의 `LOCAL_PREVIEW_NOT_APPLYABLE` 보고서는 직접 apply하지 않는다.

`samples/classification_sanity.jsonl`은 나루토·블리치, 이타치·이치고·루키아·나루토/사스케, 누들스토퍼·스케일·액션과 형태 미확인 음성 사례 6개다. 작은 합성 회귀 시험이며, 실상품 전체 정확도나 번역 품질 평가셋이 아니다. `scripts.local_semantics_benchmark`로 DB 변경 없이 실제 모델을 실행할 수 있다.

## 수집 후 자동 처리

현재 공통 수집 저장 경로와 제조사 importer는 같은 DB 트랜잭션으로 원문과 source hash 기반 대기 작업을 등록한다. `backend/scripts/local_semantics_worker.py`는 이 대기열을 하나씩 처리해 검증 후 DB에 반영한다. 원문이 추론 중 바뀌면 이전 응답 게시를 거절한다. 신규 모델 장애는 대기열에 남고 worker가 종료되어 무한 재시도하지 않는다.

자동 worker는 기본 실행에서 꺼져 있다. 모델 평가 후 다음 명령으로 켠다.

```powershell
docker compose --profile local-semantics up -d --no-deps semantic-worker
docker compose logs -f semantic-worker
# 중지
docker compose stop semantic-worker
```

일반 사용자 조회는 모델 호출을 일으키지 않는다. 대기열이 0이라고 기존 전체 상품 분류가 끝난 것은 아니다. 새로운 수집·변경 건을 처리하는 경로이며, 기존 상품의 재평가는 `--refresh-local`로 별도 실행한다. 전용 Docker GPU 모델 서버도 함께 실행돼 있어야 한다.

## 전용 모델 학습

1. `dataset.py`가 기존 API 원본 응답을 현재 규칙으로 다시 검사한다. 모든 필드가 ready인 항목만 학습 후보로 추리고, 그 외는 `review_queue.jsonl`로 분리한다. null 분류를 확인된 음성 정답으로 자동 취급하지 않는다.
2. 같은 정규화 상품명/재판, 공식 URL, 복제 설명은 연결 그룹으로 묶어 train/validation/test에 함께 배치한다. 현재 분할 외에 실제 SKU/JAN과 작품·제품 라인 단위의 추가 누수 감사를 권장한다. manifest에 데이터와 프롬프트·규칙 정보를 남긴다.
3. 검수자는 source와 result를 대조해 잘못된 값·근거를 고친 뒤 `reviewed: true`, `reviewer: 이름`을 기록한다. 학습·검증·평가 세 파일 모두 검수가 필요하다. 검수 없이 학습하려면 `--allow-silver`를 명시해야 하며 산출물은 실험 모델로 기록한다.
4. 독립 WSL2/Linux CUDA 가상환경에서 학습한다. 운영 backend에는 PyTorch/PEFT를 설치하지 않는다. RTX 5060 Ti를 지원하는 PyTorch CUDA 빌드를 먼저 설치하고 실제 CUDA 인식을 확인한다.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-training.txt
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
python train.py --data data/teacher_candidates_20261111_v2 --output models/odock-4b-v1
```

QLoRA NF4, LoRA rank 16, completion-only loss, batch 1, 기본 4,096 토큰이다. 2026-11-11 Qwen3 8B 실제 실행에서는 gradient accumulation 4, v1 40스텝, v2 추가 80스텝을 사용했다. 프롬프트 토큰에는 loss를 적용하지 않는다. 길이 초과 예제는 정답을 자르지 않고 오류로 중단한다. 정확한 패키지 버전과 데이터 해시는 각 어댑터의 `training_manifest.json`에 있다.

데이터 hash·실제 base revision·패키지 버전·학습 설정을 `training_manifest.json`에 남긴다. 검증 loss만으로 배포하지 않는다. 고정 test에서 작품 정확도, 다인 캐릭터 precision/recall, 형태별 F1, 무근거 게시율, 번역 수동 평가·숫자/코드 보존, 실제 처리 시간과 메모리를 기준 모델과 비교해야 한다.

이 환경의 WSL VM은 15 GiB이므로 `merge_adapter_streaming.py`로 샤드 단위 병합한다. 컨테이너 메모리는 병합 10g, GGUF 변환 8g, 양자화 4g으로 제한하고 순차 실행한다. 전체 CPU 병합은 메모리 부족으로 Docker를 중단시킨 적이 있어 32 GiB 미만에서 거절하도록 막았다. 샤드 병합은 소형 모델에서 PEFT 병합과 텐서 단위 동일성을 확인했다.

v2는 BF16 GGUF 변환 후 Q4_K_M 양자화하여 Ollama 실험 태그 `odock-qwen3:8b-v2-experimental`로 등록했다. 현재 설치된 Ollama는 직접 LoRA ADAPTER import를 지원하지 않아 병합된 전체 GGUF를 사용한다. 원본 `qwen3:8b`와 앱의 기본 공급자는 유지한다. 모델 단독과 사전 결합 결과를 별도 평가하며, 학습·변환 성공은 정확도 승인이 아니다. [실제 학습과 평가 결과](../docs/reports/LOCAL_MODEL_TUNING_20261111.md) 참고.

## 근거 문서

- [Qwen3 4B Instruct 공식 모델 카드](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507): 모델·라이선스·Transformers 실행.
- [Hugging Face bitsandbytes 문서](https://huggingface.co/docs/transformers/v4.56.2/quantization/bitsandbytes): 4비트 QLoRA와 양자화 설정.
- [Hugging Face SFT 문서](https://huggingface.co/docs/trl/v0.23.0/en/sft_trainer): 지도학습 데이터와 completion/assistant loss 개념. 현재 train.py는 Transformers Trainer를 직접 사용한다.

정식 완료 증거와 남은 작업은 [구현 결과 보고서](../docs/reports/LOCAL_SEMANTICS_20261111.md)에 기록한다.
