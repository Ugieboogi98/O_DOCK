# O_DOCK 로컬 번역·분류 구축 결과

작성일: 2026-11-11 (Asia/Seoul)

## 결과

스타터를 현재 v5 앱과 연결했다. 실제 RTX 5060 Ti 16GB와 Docker Ollama에서 Qwen3 8B Q4_K_M의 번역·구조화 분류를 실행했다. 학습 환경 구성과 데이터 준비 도구도 추가했지만 **학습된 O_DOCK 전용 가중치는 아직 없다**.

```text
수집·가져오기 → 원문과 의미 대기 작업 함께 저장
  → 선택적으로 실행하는 로컬 worker (순차 GPU 요청)
  → 로컬 모델 + 원문 일치형 이름 사전
  → 근거·숫자·제품 코드·필드별 검증
  → 검증된 DB 필드 저장 / 불확실한 값 보류
```

## 구현

- `backend/app/services/ollama_semantics.py`: JSON Schema와 think=false, 유료 API 자동 대체 없음. 일반 사용자 조회로 추론하지 않는다.
- `local_semantic_aliases.json`, `local_semantic_lexicon.py`: 나루토·블리치와 기존 사전의 원문 일치형 정규화. 일본 공식 사이트는 원문 이름 확인에 사용했으며 한국어명은 검수 가능한 관용 표기로 구분했다. 제품 라인과 일반적인 ‘오리지널 캐릭터’를 작품·고유 캐릭터로 게시하지 않는다.
- 모델 digest·프롬프트·Schema·원문/규칙·별칭 데이터/코드를 캐시 키에 포함한다. 모델 원시 출력과 정규화 결과를 모두 보관한다. 입력은 자르지 않고 바이트 상한을 검사하며 긴 입력은 보류한다.
- `backend/scripts/local_semantics_worker.py`: 수집 대기열을 소비해 검증·DB 반영. 추론 중 원문 변경은 이전 응답 게시를 거절한다. 기존 수동 이름과 개인 기록 보호 유지.
- `product_semantics run --refresh-local`: 로컬에서만 강제 재평가하고 이전 게시 내용을 보고서에 보존한다.
- `dataset.py`, `train.py`, `evaluate.py`, `merge_adapter.py`: 데이터 분할·QLoRA·평가·병합 도구. 학습 의존성은 backend와 분리했다.

## 실제 실행 증거

| 항목 | 결과 |
|---|---|
| GPU | RTX 5060 Ti, 16,311 MiB |
| Ollama | 0.40.16, 이미지 digest를 Compose에 고정 |
| 모델 | qwen3:8b, 8.2B, Q4_K_M, 파일 약 5.23GB |
| 모델 digest | 500a1f067a9f782620b40bee6f7b0c89e17ae61f686b92c24933e4ca4b2b8b41 |
| GPU 실행 | Ollama ps: 100% GPU, context 16,384, 런타임 약 7.5GB |
| 개발 회귀 6개 | 초기 완전 분류 일치 3/6 → 사전·역할 정규화 보완 후 6/6 |
| 추론 시간 | 작은 사례별 약 1.3~4.2초, 첫 로딩 포함 초기 사례 약 52초 |
| 실제 후류 5개 | 정식 CLI 미리보기 ready 2 / partial 3 / 호출 실패 0 |
| backend 회귀 테스트 | 전용 테스트 DB에서 192개 통과 |
| 로컬 도구 테스트 | 14개 통과 |

6개 사례는 개발 중 보완에 사용한 작은 회귀 사례로 **독립 held-out 성능이나 전체 정확도 100%가 아니다**. 후류 예제에서는 이름 오역이 형식 검증을 통과하기도 했다. ready 비율은 번역 정확도가 아니므로 자동 확대 근거로 사용하지 않았다.

실제 출력은 `O_DOCK_LOCAL_SEMANTICS/reports/`와 Docker `/app/media/local_semantic_reports/`에 보관한다. 원시 응답은 `/app/media/local_semantic_cache/`에 캐시 키별로 남긴다.

## 학습 데이터

최초 147개에서 규칙으로 보완한 값이 원본 정답에는 null로 남는 사례 등을 추가 제외했다. 현재 기준은 `data/teacher_candidates_20261111_v2/`이다. v1은 재점검 전 산출물이다.

| 항목 | 개수 |
|---|---:|
| 최종 학습 후보 | 127 |
| train / validation / test | 107 / 9 / 11 |
| 추가 검수 대기 | 2,495 |
| 사람 검수 완료 정답 | 0 |
| 후보 내 블리치 / 누들스토퍼 | 0 / 0 |

원본 응답과 정규화 라벨을 보존한다. URL·정규화 이름/재판·복제 설명 연결 그룹은 같은 split에 둔다. SKU/JAN·작품·제품 라인 단위 추가 누수 감사와 균형 보완이 필요하다. `reviewed: true`, `reviewer`를 기록해야 기본 학습을 시작할 수 있다. `--allow-silver`는 실험용이며 정답 확보를 의미하지 않는다.

4B QLoRA 레시피는 실제 base revision·데이터 hash·설정·패키지 버전을 기록하고 completion-only loss를 사용한다. 검수 정답이 없고 PyTorch/PEFT 학습 환경도 미설치여서 **실제 파인튜닝·병합·GGUF 변환은 수행하지 않았다**. 학습 GPU 메모리와 라이브러리 호환성도 해당 환경에서 확인해야 한다.

## 반영 범위와 다음 단계

backend를 빌드·갱신했다. 자동 worker는 기본 비활성이며 1회 실행 결과 대기열 0 / 저장 0이었다. 이번에는 운영 DB 번역 결과를 교체하거나 전체 상품을 재처리하지 않았다. 원문·이미지·계정·개인 기록은 변경하지 않았다.

1. 나루토·블리치 및 세 가지 형태를 균형 있게 포함한 실상품 50~100개부터 검수하고 별도의 고정 평가셋을 확정한다.
2. 긴 설명·관련 상품 혼입·제목 오역을 평가하고 사전/입력 선별을 보완한다.
3. 4B 기준 모델과 QLoRA 모델을 같은 고정 평가셋으로 비교한다. 번역 수동 평가, 작품 정확도, 캐릭터 precision/recall, 형태별 F1, 무근거 게시율을 분리한다.
4. 개선된 모델만 배포한 뒤 `local-semantics` 프로필을 켜서 새 수집 상품부터 자동 처리한다.

설정·명령은 [구현 안내](../../O_DOCK_LOCAL_SEMANTICS/IMPLEMENTATION.md)를 확인한다.

참고: [Qwen 공식 모델 카드](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507), [Hugging Face QLoRA 문서](https://huggingface.co/docs/transformers/v4.56.2/quantization/bitsandbytes), [BLEACH 공식 캐릭터](https://bleach-anime.com/character/), [TV Tokyo 나루토](https://www.tv-tokyo.co.jp/contents/naruto/chara.html).
