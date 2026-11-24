# O_DOCK 일본어 번역·분류

일본어·영문 상품명을 한국어로 번역하고 **작품 / 캐릭터 / 피규어 종류**를 추출하는 로컬 실행·학습 프로젝트다.

현재 Qwen3 8B Q4_K_M을 RTX 5060 Ti 16GB에서 실행했고, backend 검증·DB 저장·수집 대기열에 로컬 공급자를 연결했다. 나루토·블리치와 누들스토퍼·스케일·액션의 개발 회귀 사례 6개를 통과했다. 전체 상품 정확도가 아니다. 실제 후류 5개에서는 오역과 보류가 남아 자동 worker는 기본 비활성이다.

2026-11-11에 Qwen3 8B **QLoRA 가중치 학습을 실제로 두 차례 실행했다.** v1 40스텝, v2 추가 80스텝이며, 실험 태그는 `odock-qwen3:8b-v2-experimental`이다. 학습 자료는 에이전트가 작성한 합성 예제 216개와 374개이며 독립적인 사람 검수 정답은 0개다. 원문 사전과 게시 보류 규칙도 함께 수정했다. 자동 운영 승인을 뜻하지 않는다.

실제 100건의 동일 기준 비교에서 작품명 정답은 기본/학습 모델 모두 89/98건이었다. 원시 캐릭터 precision은 78.4%에서 61.8%로 악화했다. 학습 loss가 낮아도 안전한 분류기로 승격하지 않는다. 기존 60건과 100건은 사전 보강에 사용해 개발 표본으로 전환했으며 새 100건을 별도 검증한다. [학습·평가 상세 보고서](../docs/reports/LOCAL_MODEL_TUNING_20261111.md)를 확인한다.

- [실행·자동 처리·학습 안내](IMPLEMENTATION.md)
- [구현 결과와 남은 작업](../docs/reports/LOCAL_SEMANTICS_20261111.md)
- `dataset.py`: API 응답 재검증, 라벨 정규화, 누수 방지 분할.
- `train.py`: QLoRA, Qwen3 8B 실제 실행 확인. 라벨의 `reviewer`·`label_origin`으로 에이전트 합성과 사람 검수를 구분한다.
- `evaluate.py`: 고정 정답셋의 작품·캐릭터·형태 지표.
- `merge_adapter_streaming.py`: 원래 revision의 기반 모델에 샤드 단위 어댑터 병합. 이 환경에서는 전체 CPU 병합을 사용하지 않는다.
- `local_semantics.py`: 독립 연결 시험 도구. 미리보기는 DB 적용 보고서가 아니다.
- `samples/classification_sanity.jsonl`: 개발 회귀 사례. 학습/독립 평가에 사용하지 않는다.
- `data/teacher_candidates_20261111_v2/`: 현재 학습 후보와 검수 대기열(소스 관리 제외).
- `reports/`: 실제 로컬 추론 결과(소스 관리 제외).

스타터 원본은 `../backups/local_semantics_20261111/starter_original.zip`에 보존했다. `VSCODE_TASK.md`는 당시의 참고 자료이며 현재 앱 상태를 설명하는 문서는 아니다.


- [2026-11-11 Web classification and manual review](../docs/reports/WEB_CLASSIFICATION_REVIEW_20261111.md)
