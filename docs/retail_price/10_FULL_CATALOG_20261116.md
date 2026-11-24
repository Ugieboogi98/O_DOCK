# 국내 판매처 전체 상품 수집 실행

## 현재 실행 방식: Windows 로컬 수집

2026-11-16 사용자 요청으로 Docker의 `domestic-price-worker`를 중지하고 Windows의 로컬 Python으로 전환했다. 기존 체크포인트 폴더를 그대로 사용하며 수집 결과는 기존 PostgreSQL에 저장한다. 따라서 수집 프로세스는 Docker 밖에서 동작하지만 DB 서비스는 실행되어 있어야 한다.

프로젝트 루트에서 다음 명령으로 이어서 수집한다. 이미 실행 중이면 중복 실행하지 않는다.

```powershell
.\.venv\Scripts\python.exe tools/collect_domestic_local.py --commit --report-dir data/private/retail_price/20261116_full_catalog
```

로컬 실행 환경은 프로젝트의 `.venv`다. 최초 구성에 필요한 의존성은 SQLAlchemy, psycopg[binary], pydantic-settings, httpx, beautifulsoup4, filelock이다. 로컬 실행기는 `.env`의 PostgreSQL 설정을 읽고 localhost:5432로 접속한다. 비밀값을 로그에 출력하지 않는다.

백그라운드 실행의 로그는 같은 보고서 폴더의 `host.stdout.log`, `host.stderr.log`, 부모 프로세스 PID는 `host.pid`에 기록한다. 판매처별 `progress.json`의 `platform: Windows`, `process_id`, `updated_at`으로 실제 수집 프로세스를 확인할 수 있다. Windows 가상환경의 실행기와 실제 Python 프로세스 PID는 다를 수 있다. 파일 잠금은 Windows/Linux 공용 filelock을 사용한다.

아래 Docker 실행 명령은 전환 이전 운영 기록이다. 현재 로컬 수집과 동시에 실행하면 안 된다.

2026-11-16 ‘전 상품 전체적인 유통사 가격 수집 시작해’ 요청으로 30건 제한이 없는 일회성 전체 수집 worker를 시작했다. 대상은 매니아하우스·히어로타임·코믹스아트·피규어팜이다.

## 순회 범위와 저장

각 사이트 홈에서 공개 카테고리와 상품 링크를 발견하고, 각 목록의 페이지 번호를 따라 순회한다. 기존 `pagination_links`를 재사용하고 알려진 카탈로그 경로·카테고리 번호·페이지 번호만 허용한다. 실제 매니아하우스와 피규어팜 목록의 2페이지 이후 링크도 확인했다. 상품과 목록 URL은 추적 파라미터·www 별칭·중복 카테고리 표기를 정규화한다.

판매처당 동시에 요청하는 작업은 1개다. 네 판매처는 독립적으로 실행되며 각각 최소 3초 요청 간격을 적용한다. 공개 상품의 가격·상태·JAN·상품 URL을 기존 listing/offer 저장 서비스로 upsert한다. 상품 카탈로그 연결 후보는 기록하되 매칭 미확정 가격은 판매처 상품으로 보관한다.

404·410 상품은 unavailable, 성인인증이 필요한 상품은 restricted로 기록하고 다음 상품으로 진행한다. 개인결제·잔금결제 안내 등의 항목은 제외한다. 403·429 또는 접근 확인 화면이 발생하면 해당 판매처 실행을 blocked로 기록한다. 다른 판매처 작업은 계속된다.

## 중단과 재개

각 판매처의 `checkpoint.sqlite`에 발견한 목록·상품 URL과 pending/done/failed 등의 상태를 저장한다. 진행 기록은 `progress.json`이다. DB 저장 후 체크포인트 기록 전에 중단돼도 같은 관측의 upsert를 다시 수행하므로 중복 listing을 만들지 않는다. 출처별 파일 잠금으로 같은 체크포인트의 동시 수집을 막는다.

기본 저장 위치는 `data/private/retail_price/20261116_full_catalog/`이며, 그 아래에 판매처 코드별 폴더가 있다. 동일 폴더를 사용하면 미완료 항목을 이어서 처리한다. 완료된 항목까지 모두 새로 확인하려면 새 보고서 경로로 별도 일회성 실행을 시작해야 한다.

Docker가 꺼지면 수집은 중단된다. Docker를 다시 켠 뒤 아래 명령으로 재개한다.

```powershell
docker compose --profile domestic-prices up -d --no-deps domestic-price-worker
```

코드 변경 후 갱신하는 경우 먼저 해당 서비스를 빌드한다.

```powershell
docker compose --profile domestic-prices build domestic-price-worker
docker compose --profile domestic-prices up -d --no-deps domestic-price-worker
```

진행 조회와 로그 확인 명령은 다음과 같다.

```powershell
docker compose ps domestic-price-worker
docker compose logs --tail 5 domestic-price-worker
Get-Content data/private/retail_price/20261116_full_catalog/progress.json -Encoding utf8
```

`product_done`은 이번 전체 실행에서 처리한 수이며, 기존 DB 행을 갱신한 항목을 포함한다. `storage.inserted`와 `updated`는 출처별 작업 기록이다. 대기 상품 수는 목록 탐색이 진행되면서 늘어나므로 초기 발견 건수를 전체 상품 수로 해석하지 않는다.

## 검증과 현재 실행

전체 백엔드 회귀 테스트는 354 passed, 18 skipped였다. 이후 삭제·성인인증 상품 처리 보완은 `test_domestic_catalog.py`의 7개 테스트로 재검증했다. 목록 정규화·페이지 순회·중복 제거·프로세스 중단 후 재개·차단 시 무재시도도 검사했다.

실행 초기에 히어로타임의 삭제 상품 404로 출처가 멈춘 것을 확인해 개별 unavailable 처리로 수정하고 같은 체크포인트에서 재개했다. 본문이 없는 일부 상품은 성인인증 페이지로 이동하는 안내임을 확인했고, 이후 해당 응답은 restricted로 기록하도록 보완했다. 기존 failed 항목은 체크포인트에 남아 있어 성공 건수에 포함되지 않는다.

서비스는 Docker Compose의 `domestic-prices` 프로필에 있는 `domestic-price-worker`다. `restart: on-failure:3`은 예기치 않은 프로세스 오류 재개를 위한 설정이다. 정상 완료 후 주기적으로 재수집하는 스케줄러는 아니다. 저장 가격 조회는 기존 `/api/retail-offers`를 사용한다.
