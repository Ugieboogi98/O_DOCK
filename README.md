# O_DOCK

일본 공식 피규어·굿즈 정보를 한국어로 검색하고, 계정별 관심상품과 구매·배송 기록을 관리하는 앱입니다.

Vue / FastAPI / PostgreSQL / Chroma / Docker Compose.

Instagram 공식 API 행사 수집은 별도 [읽기 전용 가용성 POC](backend/app/integrations/instagram/README.md)로 준비했습니다. 실제 토큰·타사 계정 조회 검증 전에는 수집·DB 저장·공개 기능이 활성화되지 않습니다.

## 현재 프로젝트 실행·업데이트

기존 `.env`, DB 및 이미지 볼륨을 유지한 상태에서 프로젝트 루트에서 실행합니다.

```powershell
powershell -ExecutionPolicy Bypass -File scripts/update.ps1
```

이 스크립트는 서비스 빌드와 명시적인 DB 마이그레이션을 수행합니다. 기존 상품 seed와 수집 worker를 다시 실행하지 않습니다. 새 DB에 초기 데이터를 넣는 최초 설치와 기존 환경 업데이트는 구분해야 합니다. `docker compose down -v`는 기존 데이터를 삭제하므로 사용하지 마세요.

- 웹: http://localhost:8080
- API 문서: http://localhost:8000/docs
- 일반 계정: 상단 로그인에서 생성·접속. 개인 찜·구매 기록은 로그인 필요.
- 공용 카탈로그 관리자: 데이터 현황에서 `.env`의 `ADMIN_TOKEN`으로 연결.
- 관리자 연결 시에만 제한된 최신 상품 갱신을 요청합니다. 일반 방문은 수집을 시작하지 않습니다.

## 코드 위치

| 위치 | 책임 |
|---|---|
| `backend/app/main.py` | 앱·라우터·미들웨어 구성 |
| `backend/app/api/` | HTTP 요청/응답과 권한 의존성 |
| `backend/app/core/security.py` | 관리자 인증과 공통 Origin 검사 |
| `backend/app/services/accounts.py` | 비밀번호 해시, 세션, 사용자 소유권 의존성 |
| `backend/app/services/personal_records.py` | 구매 기록 검증·저장 |
| `backend/app/services/exchange_rates.py` | 환율 검증·캐시 |
| `backend/app/services/catalog_ingest.py` | 수집과 인덱싱·의미 검증 대기 작업 저장 |
| `backend/app/services/import_pipeline.py` | 제조사 가져오기와 의미 검증 대기 작업의 원자적 저장 |
| `backend/app/services/product_semantics.py` | 원문 문맥·유효성 조회·의미 결과 저장 |
| `backend/app/services/semantic_rules.py` | 모델·DB 호출 없는 원문 근거 검증 |
| `backend/app/services/semantic_provider.py` | 모델 호출·응답 해석·재시도 |
| `backend/app/services/semantic_policy.py` | 필드별 게시·보류 정책 |
| `backend/app/services/semantic_queue.py` | 원문 버전별 검증 대기 작업 |
| `backend/app/repositories/` | 카탈로그 조회·목록 일괄 로딩 |
| `backend/app/collectors/` | 허용된 출처 접근과 제조사별 파서 |
| `backend/scripts/` | 실제 사용하는 수집·검증·복구 CLI |
| `frontend/src/` | 화면·인증 상태·계정별 개인 상태 |

제조사 수집 묶음은 모두 `data/imports/`에, 독립 운영 도구는 `tools/`에, 백업은 `backups/`에 보관합니다. 제조사별 폴더를 프로젝트 루트에 만들지 않습니다. 자세한 경계와 이전 경로는 [프로젝트 구조](docs/PROJECT_STRUCTURE.md)를 확인하세요.

공통 가져오기 명령(기본값은 파일 검증, DB 저장 없음):

```powershell
python scripts/import_bundle.py furyu validate
python scripts/import_bundle.py s_fire validate
python scripts/import_bundle.py taito validate
python tools/check_structure.py
```

이미지 중복 도구는 `bash tools/image_dedup/run.sh ...`로 실행합니다. 이미지·원문·복구 journal은 실제 자료이므로 코드 정리 대상으로 삭제하지 않습니다.

## 검증

```powershell
docker compose -p figure-archive-ai run --rm --no-deps backend python -m pytest -q
```

PostgreSQL 통합 테스트는 운영 DB와 다른 `TEST_DATABASE_URL`이 필요합니다. 미설정 시 해당 테스트는 건너뜁니다.

```powershell
cd frontend
npm.cmd test -- --run
npm.cmd run build
```

모델 호출 없이 상태 확인:

```powershell
docker compose -p figure-archive-ai exec -T backend python -m scripts.product_semantics status
docker compose -p figure-archive-ai exec -T backend python -m scripts.product_semantics pending --limit 5
```

의미 추출 `run`, 전체 번역·수집·재색인 명령은 상태 조회와 다릅니다. 실행 범위와 유료 호출 여부를 확인해야 합니다.

## 현재 구현과 작업 기록

전체 진행 내역과 재점검 결과: [종합 작업 보고서](docs/reports/WORK_REPORT_20261110.md). 최신 디렉터리 정리는 [프로젝트 구조](docs/PROJECT_STRUCTURE.md)를 기준으로 합니다.

- [이미지 중복 처리 확인](docs/reports/HANDOFF_PROGRESS_20261110.md)
- [필드별 게시와 목록 조회](docs/reports/SEMANTICS_FIELDS_REFACTOR_20261110.md)
- [수집과 의미 검증 대기열](docs/reports/SEMANTIC_QUEUE_20261110.md)
- [공용 카탈로그 관리자 권한](docs/reports/ADMIN_BOUNDARY_20261110.md)
- [계정과 개인 기록 소유권](docs/reports/USER_OWNERSHIP_20261110.md)
- [불필요한 파일 삭제와 구조 정리](docs/reports/CODE_CLEANUP_20261110.md)
- [제조사별 가져오기와 검증 대기열 통합](docs/reports/IMPORT_PIPELINE_20261110.md)

과거 문서의 시점별 상태와 현재 구현은 다를 수 있습니다. 코드 진입점은 이 README를 기준으로 확인하세요.
