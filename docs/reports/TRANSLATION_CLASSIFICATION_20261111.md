# 전체 상품 한국어 번역·분류 실행 보고서

실행일: 2026-11-11 (Asia/Seoul)

실행 상태: **blocked**. 대상 6,161개 중 2,638개 처리.
마지막 상태 갱신(UTC): `2026-11-11T00:38:13.200820+00:00`

`.env`에 등록된 GMS API의 `gpt-4.1-mini`를 사용한다. 키 값은 보고서에 포함하지 않는다.

## 실행과 보존

- 상품별 한국어 상품명·작품명·캐릭터명·피규어 형태를 요청하고 필드별 검증 후 DB에 저장한다.
- 원문과 기존 수동 한국어명, 관심상품·구매 기록은 보존한다.
- 기존 한국어명이 없는 상품은 검증된 번역명으로 채운다. 분류는 `product_semantics`에 근거와 함께 저장한다.
- 초기 4개 동시 요청으로 확인 후 16개로 확대. 검증 보정 1회. 인증·잔액 등 차단 오류 발생 시 신규 요청을 중단한다.
- 영문 상품명도 한국어로 번역하도록 지침을 보완했다. 숫자·스케일·제품 코드를 보존한다.
- 미확인 작품·캐릭터·형태를 추측으로 채우지 않는다. `partial`은 필드 일부만 확인된 상태다.
- DB 백업: `backups/translation_20261111/before.dump` (pg_restore 목록 확인 완료).
- 상품별 원본 모델 응답과 재시도 기록: Docker media 볼륨 `/app/media/semantic_reports/full_20261111/<상품ID>.json`.
- 응답 전체의 로컬 복사본: `backups/translation_20261111/responses/`.
- 일본어 서수(第二弾 → 제2탄)와 작품·제품 라인 소개문 관계를 보완한 v5 규칙으로 기존 응답을 재검증했다. 추가 API 호출 없음.
- 검증: 전용 테스트 DB에서 전체 backend 테스트 180개 통과. 프로젝트 구조 검사 오류 0건.

## 실행 이력

첫 실행은 GMS 키 잔액 소진(`This GMS key has no token left`)으로 중단했다. 이후 사용자가 새 키를 등록하여 기존 결과를 재사용하며 재개했다.

현재 상태: API 오류로 중단. 상품별 응답 파일의 error 코드 확인 필요.

## 이번 순회 집계

| 상태 | 개수 |
|---|---:|
| cached | 2,570 |
| partial | 46 |
| review | 6 |
| failed | 16 |

## DB 최종 필드 검증 집계

전체 6,161개 중 현재 규칙의 응답이 저장된 상품은 2,622개이며, 미처리 상품은 3,539개다.
전체 상품 처리는 아직 완료되지 않았다. 아래 미확인에는 아직 API 처리를 시작하지 못한 상품도 포함된다.

| 필드 | 검증 통과 | 보류 | 미확인 |
|---|---:|---:|---:|
| 한국어 상품명 | 2,570 | 52 | 3,539 |
| 작품명 | 1,542 | 72 | 4,547 |
| 캐릭터명 | 1,657 | 241 | 4,263 |
| 피규어 형태 | 320 | 842 | 4,999 |

### 제조사별 상품명

| 제조사 | 전체 | 번역 검증 통과 |
|---|---:|---:|
| Kotobukiya | 30 | 28 |
| MegaHouse | 1,313 | 1,248 |
| FuRyu | 1,379 | 197 |
| Good Smile Company | 9 | 9 |
| Bandai Spirits | 3,183 | 1,079 |
| SEGA | 84 | 3 |
| TAITO | 160 | 3 |
| Hot Toys | 3 | 3 |

상세 미확인 상품과 검증 오류: [DB 감사 JSON](../evidence/translation_20261111/audit.json).

## 재개 및 확인

```powershell
docker compose -p figure-archive-ai exec -T backend python -m scripts.product_semantics status
# .env 키를 교체했다면 먼저 컨테이너 환경을 다시 로드한다.
docker compose -p figure-archive-ai up -d --no-deps --force-recreate backend
docker compose -p figure-archive-ai exec -T backend python -m scripts.complete_semantics --commit --workers 16 --report-dir /app/media/semantic_reports/full_20261111
python scripts/monitor_semantics.py
```

재개 시 같은 원문에 대한 검증 완료 번역은 API를 다시 호출하지 않는다. 저장된 응답이 있으면 DB 저장을 재시도한다.
