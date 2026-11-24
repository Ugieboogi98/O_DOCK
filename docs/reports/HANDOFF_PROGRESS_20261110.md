> 이 문서는 작업 당시의 이력입니다. 이후 변경된 경로는 [현재 프로젝트 구조](../PROJECT_STRUCTURE.md)를 확인하세요.

# 인계 후 1차 작업 결과 — 2026-11-10

## 실제 상태 확인

- 현재 폴더는 Git 저장소가 아니다. 자동 커밋은 하지 않았다.
- 상품 6,158개. 의미 레코드 ready 3 / partial 1 / review 1. 유료 API 호출 없음.
- backend / postgres 정상, frontend / chroma 실행 중. catalog-worker 중지 상태 유지.
- `migration_backup/image_dedup/apply_20261110_145718_2276.json`은 committed이며 변경 1,555건이다.
- 컨테이너의 동일 journal을 현재 PostgreSQL과 대조했다. 1,555건 전부 duplicate_hidden, 누락 행과 상태 불일치 0건.
- 현재 이미지 행: duplicate_hidden 1,555 / personal_local 28,077.
- 영향받은 551개 상품을 실제 `ordered_images()`로 조회해 숨김 이미지 노출 0건 확인. 카드 대표 이미지와 상세 API가 이 함수를 공유한다.
- 과거 audit 후보 1,599건과 실제 처리 1,555건은 다른 수치다. 현재 잔여 중복 수는 새로 검사하지 않아 미확정이다.
- audit 제외 ID 16193 / 16400 / 16552 / 16594는 모두 `ValueError:PIXELS_TOO_LARGE`. 손상 또는 누락으로 단정하지 않는다.
- 원본 파일과 DB 행은 보존되어 있다. 영구 삭제 없음.

## 수정

- `backend/app/services/enrichment.py`: 같은 variant/source URL의 duplicate_hidden 행은 재다운로드하거나 personal_local로 되돌리지 않는다. 파일이 없어도 운영자의 숨김 결정을 유지한다.
- `backend/app/services/bnkr_catalog.py`: 동일한 숨김 보존 정책 적용.
- `backend/tests/test_asset_repair.py`: 두 경로 × 파일 존재/누락의 4개 회귀 사례 추가. 두 번 재수집해도 숨김 유지 및 추가 행 없음 확인.
- 서로 다른 URL에 새로 올라온 유사 이미지까지 자동 차단하는 기능은 포함하지 않는다.

## 검증과 반영

- 운영 DB 대신 각 테스트의 SQLite fixture를 사용했다. 모델과 이미지 다운로드는 모의 처리했다.
- asset_repair / product_semantics / semantics_context / semantics_migration: **46 passed**.
- 로컬 Python에는 pytest가 없어 기존 Docker 백엔드 환경에서 로컬 소스를 별도 읽기 전용 마운트해 실행했다.
- `docker compose -p figure-archive-ai up -d --build --no-deps backend`로 반영. init/seed/worker 재실행 없음.
- 반영 후 backend healthy, `/api/health` HTTP 200.

## 기존 복구 자료

- DB 백업: `migration_backup/image_dedup/before_20261110_145718_2276.dump`
- 원래 적용 journal: `migration_backup/image_dedup/apply_20261110_145718_2276.json`
- 이미지 숨김 복구는 기존 `O_DOCK_IMAGE_DEDUP/run.sh restore --report ...` 사용. 이번 작업에서는 복구나 apply를 반복하지 않았다.
- 이번 소스 수정은 위 두 서비스의 duplicate_hidden 조기 건너뛰기 조건을 되돌린 후 backend를 다시 빌드하면 되돌릴 수 있다. DB 마이그레이션 없음.

## 다음 작업

후속 진행: [필드별 게시 및 목록 조회 리팩터링](SEMANTICS_FIELDS_REFACTOR_20261110.md)에 52번 응답 재검증·반영과 조회 구조 개선 결과를 기록했다. 아래 목록은 최초 점검 당시의 다음 작업 목록이다.

1. 실제 유사 이미지 표본을 육안 대조해 오탐 여부 확인. 이번 검증은 DB/갤러리 조회 경로 검증이며 브라우저 육안 확인은 아니다.
2. 기존 52번 모델 응답을 재사용해 필드별 검증/게시 정책 설계 및 구현. 현재는 한 형태 오류로 전체 의미 레코드가 review가 되는 기존 정책이다.
3. API/검색/UI/저장/캐시의 일관성을 함께 검증한 뒤 책임 단위로 리팩터링. 전체 번역·전체 재수집·대량 유료 호출은 실행하지 않는다.
