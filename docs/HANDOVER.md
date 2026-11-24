# Figure Archive AI 후속 개발 결과 · 2026-10-22

## 적용 결과와 검증 범위

첨부 프로젝트를 기준으로 수정했다. `collect_other_makers.py`와 `other_makers_sources.json`은 이미 설치되어 있었지만 7개 제조사가 모두 비활성 상태였다. 이번 버전은 **FuRyu 공식 스케일 피규어 카탈로그만 신규 활성화**했다. 다른 6곳을 수집 성공으로 표시하지 않는다. 기존 MegaHouse 어댑터의 `og:title` 복구 로직과 Compose의 프로젝트명·기존 볼륨명·초기화 흐름은 유지한다.

이 작업 환경에는 Docker와 PostgreSQL 서버가 없다. 사용자 PC의 1,387개 제품, Metadata 1,387 / Documents 2,742 및 최신 `/api/status`는 직접 접근하거나 변경하지 않았다. 첨부 SQL/JSON은 실행 중 DB의 최신 상태를 증명하지 않는다. DB 통합 테스트는 임시 SQLite, 색인은 실제 임시 ChromaDB로 실행했다. PostgreSQL advisory lock과 Docker Compose 전체 기동은 사용자 PC에서 검증해야 한다.

## 제조사별 조사 결과

| 제조사 | 확인한 공식 목록 | 이번 결과 | 배포 설정 |
|---|---|---|---|
| FuRyu | https://furyu-hm.com/collections/scale-figures | 공식 목록 1·2페이지 각각 HTTP 200 / 상품 링크 24개. `<link rel="next">`로 2·3페이지 탐색. 공식 제품 1개 실응답 파싱 성공. robots HTTP 200, 해당 경로 허용 규칙 확인 | 수동·자동 갱신 활성화 |
| Good Smile Company | https://www.goodsmile.com/en/scalefigure_list | 웹 조회에서 제품 목록 확인. 제3 제조사 제품도 혼재. 수집 환경 robots 조회 503. 기존 정책이 목록 경로를 허용하지 않음 | 비활성 |
| Bandai Spirits | https://tamashiiweb.com/item/ | 목록과 robots 조회 503. 사이트 이용 조건은 확인했으나 실제 HTML 수집·파서 검증 미완료 | 비활성 |
| SEGA | https://segaplaza.jp/prize/ | 웹 조회 목록에 상품 링크 없음. JS 의존 가능성. robots 404 | 비활성 |
| TAITO | https://www.taito.co.jp/taito-prize/ | 웹 조회에 `{{item.ProductName}}` 템플릿 잔존. robots HTTP 200, Crawl-delay 20초. 이용 조건상 콘텐츠 저장·전용 제한 확인 | 비활성 |
| Hot Toys | https://www.hottoys.jp/item/ | 웹 조회 목록에 실제 제품 링크 없음. robots 404. 기존 정책은 상세 `/item/view/`만 허용. 이용 조건상 무단 사용·복제 제한 확인 | 비활성 |
| Kotobukiya | https://www.kotobukiya.co.jp/product/ | 목록 웹 조회 503 / robots 직접 조회 403. 기존 도메인 정책 비활성 | 비활성 |

조회 실패는 사이트 자체 장애라고 단정할 수 없다. 지역·프록시·접근 제한의 영향일 수 있다. JS용 비공개 API를 추정하거나 봇 차단을 우회하지 않았다. robots 404는 이 수집기의 기존 처리 관례상 규칙 없음으로 다루지만, 이용 조건의 허가를 뜻하지 않는다.

FuRyu 이용 조건: https://furyu-hm.com/pages/terms

이번 활성화 범위는 로그인·구매 없이 공개된 사실 메타데이터를 개인 학습용으로 읽는 기능이다. 검토한 이용 조건에서 해당 읽기 작업에 대한 명시적 자동 수집 금지를 식별하지 못했고 robots는 경로를 허용했다. 제조사로부터 별도의 허가나 재배포 라이선스를 받은 것은 아니다. 이미지, 원문 상세 설명, 번역 API는 이 통합 수집 경로에서 호출하지 않는다. 해외 이용 관련 조항은 구매 서비스 문맥에 존재하므로, 실제 서비스 공개·재배포로 범위를 확대하기 전에는 별도 재검토가 필요하다.

실제 HTTP 응답과 파싱 증거(전체 HTML은 배포하지 않음): `source-verification-handover.json`. 해당 공식 응답을 임시 DB에서 재생한 등록·중복·색인 검증 결과는 `official-response-replay.json`에 기록했다. 최초 created / 재실행 existing, 제품 1·문서 1·색인 각 1개, 미완료 색인 0개였다.

## 코드 변경

- `backend/scripts/collect_other_makers.py`: 제조사 순차 실행, 페이지 시도 수 제한, 신규 DB 등록 수 제한, 파일 잠금, 원자적 체크포인트, 오류 사유·HTTP 상태 기록, 중단 전 현재 페이지 보존, 저장 URL 선처리, 실패 항목 명시적 재시도, 목록 재탐색, 비활성/실패 종료 코드.
- `backend/app/services/catalog_ingest.py`: 공통 신규 등록, 제조사+SKU/JAN 및 공식 URL 중복 검사, PostgreSQL 트랜잭션 advisory lock, 메타데이터만 추가, 기존 행 덮어쓰기 방지, 기존 CollectionJob 테이블을 활용한 색인 outbox.
- `backend/app/services/catalog_refresh.py`: 공통 수집 경로 사용, 미완료 색인 복구, 작업 시작 시 DB 잠금으로 여러 worker의 cooldown 검사 직렬화, 색인 실패를 작업 실패 통계에 반영.
- `backend/app/collectors/safe_http.py`: 기존 HTTPS/허용 경로/공개 IP 검사 유지. robots 와일드카드·우선순위 처리, Crawl-delay/Request-rate 반영, 각 재시도 pacing, Retry-After 반영, 과도한 대기 필요 시 다음 실행으로 넘김. robots 조회 실패·HTML 차단 응답에서 수집 중지.
- `backend/app/collectors/manufacturers/base.py`, 제조사 어댑터: 상세 URL 검사와 탐색의 공통화, 목록·브랜드 URL 배제, Hot Toys 홍콩 쿼리형 URL 지원. FuRyu는 실응답의 `.tw-table-row` 및 JSON-LD를 결합하고 실제 출시 주체를 검증.
- `backend/scripts/discover_catalogs_all.py`: `<link rel="next">` 추가 인식. 기존 MegaHouse 숫자 페이지 처리 유지.
- `backend/scripts/verify_sources.py`: 활성 소스의 목록·상품 1개 읽기 전용 점검. 정책 변경·DB 저장 없음.
- `backend/scripts/audit_catalog.py`: 실제 DB 제조사별 건수·필드 누락 수·가격 누락·색인 수·미완료 색인 작업 조회.
- `backend/scripts/catalog_scheduler.py`, `docker-compose.yml`: `auto-refresh` 선택 프로필. 1시간마다 cooldown 검사, 성공한 자동 갱신은 24시간 중복 방지. 기본 Compose 실행에는 추가 worker 없음.
- `data/source_policy.json`: FuRyu의 검증된 목록 경로 1개만 추가. 다른 도메인의 활성화 상태는 변경하지 않음.
- `data/other_makers_sources.json`, `data/catalog_sources.json`: FuRyu만 수동 통합·자동 갱신 대상에 추가. 기존 MegaHouse 자동 갱신 설정 유지.
- `backend/tests/test_catalog_pipeline.py`: 수집·복구·정책·실제 SQL/Chroma/API 통합 회귀 테스트.

DB 스키마 마이그레이션은 추가하지 않는다. 기존 이미지·문서·관심상품·구매 기록·제품 ID를 삭제하거나 초기화하는 코드도 추가하지 않았다. 구형 별도 패치 폴더와 비밀 `.env`, node_modules는 결과 압축에 넣지 않았다.

## 적용 방법 · Windows Git Bash

압축 안 `patch/`의 **내용물**을 기존 `C:\Users\SSAFY\Desktop\figure-archive-ai` 폴더에 덮어쓴다. `patch` 폴더 자체를 프로젝트 안에 넣는 방식이 아니다. 기존 `.env`는 그대로 둔다. `source/`는 전체 수정 소스이며, 새 PC 구성이나 코드 열람용이다. 기존 프로젝트를 새 폴더로 옮기거나 프로젝트명을 바꾸지 않는다.

먼저 기존 프로젝트 폴더에서 PostgreSQL 백업을 저장한다. 실패하거나 파일 크기가 0이면 적용을 진행하지 말고 연결 상태를 확인한다.

```bash
cd ~/Desktop/figure-archive-ai
export MSYS_NO_PATHCONV=1
mkdir -p backups
docker compose exec -T postgres sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "backups/before_update_$(date +%Y%m%d_%H%M%S).dump"
```

파일을 덮어쓴 뒤 실행 중인 backend 이미지만 다시 만든다. 이미지에 소스가 COPY되므로 restart만으로 새 Python 코드가 적용되지 않는다.

```bash
docker compose config --quiet
docker compose up -d --build --no-deps backend
```

`--no-deps`로 이번 업데이트에서 init/seed 및 기존 DB·Chroma 서비스를 다시 실행하지 않는다. 이미 기존 시스템이 정상 기동 중이라는 전제다. `data/`는 읽기 전용 bind mount이므로 호스트 설정 파일 변경이 컨테이너에서 반영된다.

### 읽기 전용 사전 점검

```bash
docker compose exec backend python -m scripts.verify_sources
docker compose exec backend python -m scripts.audit_catalog
curl -s http://localhost:8000/api/status
```

`verify_sources`가 FuRyu를 `verified`로 출력해야 한다. 네트워크 실패·robots 차단·0개 URL이면 통합 수집을 대량 실행하지 말고 출력 JSON의 오류부터 확인한다. 이 개발 호스트에서는 공개 DNS 직접 검사가 불가능하여 SafeFetcher 실시간 점검은 `gaierror`로 실패했다. DNS 검사를 해제하지 않았으며, 공식 HTTP 응답을 별도 프록시 조회해 파서를 검증했다. 사용자 PC의 사전 점검을 생략해서는 안 된다.

### 먼저 소규모 확인

```bash
docker compose exec backend python -m scripts.collect_other_makers --max-pages 1 --max-new 2
```

이 단계는 URL 탐색·체크포인트 저장만 수행한다. PostgreSQL과 ChromaDB를 변경하지 않는다.

```bash
docker compose exec backend python -m scripts.collect_other_makers --max-pages 1 --max-new 2 --commit
```

앞서 탐색한 URL도 처리한다. 성공하면 실제 신규 제품 2개 이하를 추가하고 색인한다. 기존 제품은 제품명이나 기존 문서를 덮어쓰지 않는다.

### 일괄 수집

```bash
docker compose exec backend python -m scripts.collect_other_makers \
  --max-pages 20 \
  --max-new 500 \
  --commit
```

두 제한은 **제조사별·이번 실행 기준**이다. 현재는 FuRyu만 실행하고 다른 6곳은 사유와 함께 SKIP한다. `--max-new`는 신규 등록 수이므로 기존 제품 확인 수는 제한하지 않는다. `--max-pages`는 실패를 포함한 목록 요청 시도 수다. `--commit`은 각 상품별로 저장하므로 명령 전체가 하나의 트랜잭션인 것은 아니다.

### 중단·실패·신상품 재탐색

같은 명령을 다시 실행하면 저장된 목록 큐와 제품 URL부터 이어서 처리한다. Ctrl+C는 종료 코드 130을 반환하며 진행 상태를 남긴다. 성공적으로 끝낸 목록은 기본적으로 다시 읽지 않는다.

```bash
# 실패한 상세 파싱/목록만 명시적으로 다시 시도
docker compose exec backend python -m scripts.collect_other_makers --max-pages 20 --max-new 500 --commit --retry-failed

# 완료한 목록을 다시 방문하여 나중에 나온 상품도 탐색
docker compose exec backend python -m scripts.collect_other_makers --max-pages 20 --max-new 500 --commit --refresh-catalog

# 공식 사이트를 다시 요청하지 않고 미완료 Chroma 작업만 복구
docker compose exec backend python -m scripts.collect_other_makers --retry-index-only
```

`--reset-state`는 페이지 체크포인트를 초기화하지만, 저장 URL 파일과 DB는 삭제하지 않는다. 일반적인 이어받기에는 필요 없다. 0개 신규 등록은 기존 제품뿐일 때 정상이다. 목록 상품 링크 자체가 0이면 점검 오류로 기록한다.

종료 코드: 0=정상 완료, 1=실패/부분 실패/실행 중 잠금, 2=활성 소스 없음 또는 잘못된 CLI 인수, 130=사용자 중단. 외부 사이트 형식이 바뀌거나 robots가 차단하면 활성 소스라도 실행 중 중지된다.

### 결과 확인

```bash
docker compose exec backend python -m scripts.audit_catalog
curl -s http://localhost:8000/api/status
curl -s http://localhost:8000/api/manufacturers
```

웹 `http://localhost:8080/figures`를 새로고침해 FuRyu 필터와 상품 상세를 확인한다. CLI 수집은 자동 갱신 상태를 바꾸지 않으므로 이미 열린 화면은 새로고침이 필요하다. 방문 기반 자동 갱신은 기존 UI의 7초 polling 및 `catalog-updated` 이벤트로 목록이 갱신된다.

`/api/status`의 `search_ready=false`는 **외부 검색 API 키 미설정**을 뜻한다. ChromaDB 연결 실패를 뜻하지 않는다. 벡터 색인은 `index.metadata`, `index.documents`, `index_error`로 확인한다. PostgreSQL `document_count`는 원문 문서 수이고 Chroma `documents`는 청크 수이므로 서로 같을 필요가 없다. `audit_catalog`의 메타데이터 수 비교 기준은 제품 수가 아니라 **variant 수**다. count 일치는 필요한 기본 점검이며 모든 항목의 검색 품질을 보장하지는 않는다.

미완료 색인은 DB의 `collection_jobs`에 `collector=catalog_index, status=pending`으로 남는다. DB 상품·원문 메타데이터와 outbox는 같은 seed 트랜잭션으로 저장된다. 색인 장애는 DB 제품 등록을 되돌리지 않는다. 복구 upsert는 기존 컬렉션을 초기화하지 않는다. 기존 전체 DB를 다시 색인해야 하는 경우에도 다음 명령은 `--reset` 없이 사용한다.

```bash
docker compose exec backend python -m scripts.index
```

이 명령은 신규분만이 아니라 기존 variant 전체를 재색인한다. 임베딩 제공자가 API인 경우 비용·호출 수가 증가할 수 있다. 이번 변경의 기본 경로는 신규 variant만 색인한다.

## 자동 갱신

기존 화면 접속 시 `POST /api/catalog/refresh` 흐름을 유지했다. 마지막 성공 작업 기준 24시간, 실패/부분 실패는 1시간 cooldown이다. 프로세스 내 잠금과 PostgreSQL 잠금으로 중복 시작을 방지한다. 선택 worker는 사이트 접속 없이도 같은 기능을 주기적으로 호출한다.

```bash
docker compose --profile auto-refresh up -d --build --no-deps catalog-worker
docker compose --profile auto-refresh logs --tail 100 catalog-worker
```

사용을 중지하려면 다음 명령으로 worker만 멈춘다.

```bash
docker compose --profile auto-refresh stop catalog-worker
```

자동 갱신은 최신 목록 일부를 점검하는 bounded 작업으로, 전체 과거 카탈로그를 매일 재수집하는 기능이 아니다. 대량 과거 데이터 수집에는 수동 명령을 사용한다. 원래 `scripts.collect`는 기존 제품 보강용 refresh 동작을 유지했으므로 신규 통합 수집과 동시에 실행하지 않는 것이 좋다.

## 테스트 결과

| 검증 | 결과 | 한계 |
|---|---|---|
| Python 기존·신규 회귀 테스트 | 53개 통과 | PostgreSQL 전용 18개 제외 |
| 신규 제품 → SQL → 실제 Chroma → 조회 API | 통과 | 임시 SQLite 사용 |
| 동일 URL·제조사+SKU 재실행 | 제품 1개 유지 | PostgreSQL 동시성 실증 미실행 |
| Chroma 장애 후 outbox 재시도 | DB 제품 보존, 복구 후 색인 존재 | 임시 Chroma 사용 |
| 체크포인트·중단·페이지 제한·실패 재시도 | 통과 | 실제 컨테이너 강제 종료는 미실행 |
| MegaHouse og:title / 숫자 페이지 회귀 | 통과 | 공식 사이트 대량 재수집은 미실행 |
| robots wildcard / crawl-delay / private IP | 통과 | 통합 수집기 live DNS는 호스트 제한 |
| FuRyu 공식 응답 파싱 | 목록 2페이지·제품 1개 확인 | 전체 500개 대량 등록 미실행 |
| Vue production build | 통과 | 브라우저 시각 검증 미실행 |
| Vitest | 2개 통과 | 기존 API helper 테스트 |
| Compose YAML 구조 | parse 성공, 기존 볼륨명 유지 | Docker compose config/build는 사용자 PC 확인 필요 |

검증 호스트의 Python 패키지 버전은 `tested-environment.json`에 기록했다. 원본 requirements.txt의 모든 고정 버전과 동일한 Docker 이미지에서 테스트한 것은 아니다.

실행 명령(backend 작업 폴더):

```bash
python -m pytest -q --disable-warnings --junitxml=../docs/test-results-handover.xml
```

전용 테스트 PostgreSQL이 있다면 기존 18개도 실행할 수 있다. **운영 DB URL을 TEST_DATABASE_URL에 넣지 않는다.** 현재 테스트 fixture는 테스트용 테이블을 생성한다.

프론트엔드는 첨부 Windows용 node_modules를 Linux에서 바로 쓸 수 없어서 Linux용 네이티브 빌드 의존성을 임시 설치한 후 빌드했다. 이 node_modules는 결과물에 포함하지 않는다. Dockerfile은 원래대로 `npm ci`로 설치한다.

## 남은 과제

1. 사용자 PC에서 사전 점검 → 소량 commit → 재실행 → 제조사별 건수/API/웹 확인. PostgreSQL 동시 실행·재시작/볼륨 유지 확인.
2. 비활성 6개 제조사의 robots·이용 조건·공개 HTML 또는 허용된 API 확인. 현재 regex 개선은 코드 회귀 검증이며 공식 HTML 전체 지원을 검증한 것은 아니다.
3. `audit_catalog`로 실제 1,387개 데이터의 누락률 확인. 없는 값은 임의 추정하지 않는다. FuRyu의 발매월은 공식 `お届け時期` 예정 출고월에서 추출하며 실제 출시일과 다를 수 있다.
4. hash 임베딩은 문자열 기준선이다. 한국어·일본어 의미 검색·번역 품질 평가는 미완료다. 모델을 바꾸려면 기존 컬렉션을 임의 삭제하지 말고 별도 컬렉션으로 검증·전환할 설계가 필요하다.
5. 기존 번역 보강의 RateLimitError는 이번 수집 경로에서 번역을 호출하지 않아 재발시키지 않는다. 별도 번역 배치의 공급자 quota, Retry-After, 지수 backoff 및 최대 재시도 정책은 별도 후속 작업으로 남긴다.
6. 첨부 요구사항 PDF의 전체 F2001~F2012 충족 판정, LLM 실제 답변 품질 비교, 제출용 화면 캡처·상호 체크리스트는 이번 수집 개선 테스트만으로 완료 판정하지 않는다.

`docker compose down -v`, `docker volume prune`, PostgreSQL 초기화, Chroma 컬렉션 삭제를 실행하지 않는다.
