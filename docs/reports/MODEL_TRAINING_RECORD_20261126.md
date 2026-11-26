# 로컬 번역·분류 모델 학습 기록 — 2026-11-26 정리

PC를 비우면서 `O_DOCK_LOCAL_SEMANTICS/`의 대용량 학습 산출물(약 18GB)과 Docker 튜닝 볼륨 `odock_tuning_20261111_v2`(37.8GB)를 보존하지 않기로 했다. 이 문서는 그 산출물로 **무엇을 학습했고 무엇을 알게 되었는지**만 남긴다. 상세 수치와 원본 링크는 [튜닝 보고서](LOCAL_MODEL_TUNING_20261111.md), [후속 수정 보고서](LOCAL_MODEL_REPAIR_20261112.md), [모델 카드](../../O_DOCK_LOCAL_SEMANTICS/MODEL_CARD.md)에 있다.

## 한 줄 결론

Qwen3 8B를 O_DOCK 데이터로 QLoRA 학습했지만(2회, 2026-11-11) **운영 승격 기준에 미달**했다. 현재 서비스는 학습 모델이 아니라 기반 모델(qwen3:8b 번역, qwen3:1.7b 분류)에 **사전 우선 파이프라인**(split-semantics)을 붙여 쓴다. 성능을 끌어올린 것은 가중치가 아니라 사전·검증 규칙이었다.

## 무엇을 학습했나

| 항목 | 내용 |
|---|---|
| 기반 모델 | `Qwen/Qwen3-8B`, revision `b968826d9c46dd6066d109eabc6255188de91218` |
| 방법 | NF4 QLoRA, BF16, rank 16 / alpha 32, batch 1, gradient accumulation 4, 최대 4,096 토큰 |
| 장비 | RTX 5060 Ti 16GB, Docker + WSL |
| 과제 | 일본어 상품명 → 한국어 번역 + 작품 / 캐릭터 / 피규어 형태 구조화 추출 (JSON) |
| v1 | 데이터 216건(train 175 / validation 19 / test 22), 40 스텝, 학습률 1e-4, 497.9초 |
| v2 | v1에서 이어서 학습, 데이터 374건(342 / 16 / 16), 추가 80 스텝, 학습률 5e-5, 970.7초 |
| 학습 데이터 성격 | 에이전트가 작성·대조한 **합성 예제** 590건. 독립적인 사람 검수 정답(gold)은 0건 |
| 등록 | 병합 → BF16 GGUF → Q4_K_M 변환 후 Ollama 태그 `odock-qwen3:8b-v2-experimental`로 등록 (GGUF SHA256 `82087e7a…10245d`, 약 5.02GB) |

학습 데이터 원본은 `O_DOCK_LOCAL_SEMANTICS/data/`의 `curated_tuning_20261111`, `domain_tuning_20261111_v2`(각 train/validation/test JSONL + manifest), 교사 후보 `teacher_candidates_20261111(_v2)`, 웹 조사 결과 `web_research_20261111`이었다. 각 manifest에 파일 SHA256이 기록되어 있었다.

## 결과

### 같은 실제 상품 100건, 기반 모델 대 v2 (원시 출력)

| 지표 | 기반 qwen3:8b | v2 |
|---|---:|---:|
| 작품 정답 / 판단 대상 | 89/98 | 89/98 |
| 캐릭터 precision | 78.4% | **61.8%** |
| 캐릭터 recall | 44.9% | 61.8% |
| 형태 precision | 98.7% | 98.7% |

학습 모델은 캐릭터를 더 많이 내놓았지만 **오탐도 함께 늘었다.** 작품 정확도는 그대로였다.

### 새 상품 100건(seed 20261113, 사전 결합 결과)

작품 precision 98.9%, 캐릭터 precision 98.2%였지만 **캐릭터 recall이 61.1%**로, 미리 정한 기준(캐릭터 recall ≥ 90%)을 통과하지 못했다. 번역 ready 후보는 29~30/100건이었다.

## 알게 된 것 (다음에 다시 학습한다면)

1. **합성 데이터만으로는 부족하다.** 낮은 validation loss가 실제 상품 정확도를 보장하지 않았다. 다음 학습 전에 사람이 검수한 정답 세트가 먼저 있어야 한다.
2. **인명은 가중치보다 사전이 낫다.** 학습 모델은 그럴듯한 한글 독음을 지어냈다(예: 한자 인명 오독). 이후 파이프라인은 "사전에 없는 인명은 모델 출력만으로 승인하지 않는다"는 원칙으로 바뀌었고, 11-24~25에 Wikidata와 큐레이션 사전으로 캐릭터를 대량 보충했다.
3. **분리가 효과적이다.** 번역과 분류를 한 번에 시키는 대신 번역(8B)과 분류(1.7B)를 나누고, 사전 일치 → 모델 → 원문 근거 검증 순서로 처리하는 편이 안정적이었다([사전 우선 분리 파이프라인](SPLIT_SEMANTICS_20261117.md)).
4. **검증 규칙이 정확도의 대부분을 만든다.** 가타카나 부분 문자열(スケー**ルフィ**ギュア → 루피), 의상 '원피스'와 작품 원피스, 높이·날짜를 축척으로 읽기, 버전명을 캐릭터로 읽기 같은 오류는 모두 규칙으로 막았다.
5. **메모리 주의.** 전체 CPU 병합 때 WSL VM 메모리(15GiB)를 넘겨 Docker 엔진이 멈춘 적이 있다. 샤드 단위 병합(`merge_adapter_streaming.py`)을 쓴다.

## 보존하는 것 / 지우는 것

| 보존 (git) | 지움 (이 PC에서만 있던 것) |
|---|---|
| 학습·평가 코드: `train.py`, `dataset.py`, `evaluate*.py`, `merge_adapter*.py`, `build_*_tuning.py` | `training_cache/`(기반 모델 다운로드 캐시, 16GB) |
| 고정 표본·라벨: `samples/*.json(l)` | `models/qwen3-8b-odock-v1·v2/`(어댑터, 약 1.5GB) |
| 문서: `README.md`, `IMPLEMENTATION.md`, `MODEL_CARD.md`, `VALIDATION.json` | `data/`(학습 JSONL·웹 조사, 154MB), `reports/`(추론 원본, 94MB), `vendor/` |
| 이 기록 문서와 위 보고서들 | Docker 볼륨 `odock_tuning_20261111_v2`(병합·변환 중간 산출물, 37.8GB) |

학습된 v2 모델 자체는 Ollama 모델 캐시(`O_DOCK_MOVE_2.zip`)에 GGUF blob으로 함께 옮겼다. 다시 학습하려면 기반 모델을 다시 내려받고(`prepare_qwen8b.py`), `build_curated_tuning.py`·`build_domain_tuning.py`로 데이터를 다시 만든 뒤 `train.py`를 실행한다.
