# 국내 유통 가격 DB 수집 결과

2026-11-16 사용자의 ‘그럼 이제 국내 유통 가격 수집하자’ 요청으로 일회성 실제 저장을 실행했다. 시작 목록 각 1페이지에서 판매처별 최대 30건을 확인하는 범위로 진행했다. 피규어팜은 해당 페이지에서 중복 URL을 제거한 상품이 25개여서 총 수집 대상은 85개였다.

## 저장 결과

| 판매처 | 판매처 상품·오퍼 저장 | 전체 판매가 확보 | 유효 JAN 확보 |
|---|---:|---:|---:|
| 매니아하우스 | 30 | 30 | 28 |
| 코믹스아트 | 30 | 29 | 28 |
| 피규어팜 | 25 | 20 | 5 |
| 합계 | 85 | 79 | 61 |

상태는 예약 79건, 품절 6건이다. 네트워크·파싱·DB 저장 오류는 0건이었다. 가격 미확인 6건은 NULL로 저장했으며, 코믹스아트 1건은 표시가와 전액결제 옵션 가격 충돌, 피규어팜 5건은 옵션별 가격 확인 필요 상태다. 경고와 원문 결제 옵션을 함께 보관했다.

기존 상품에 확정 연결된 관측은 0건이다. 확보한 JAN으로 일치 후보를 찾지 못했거나 JAN이 미확인된 상품이므로, 판매처 상품으로 저장하고 catalog_variant_id=NULL을 유지했다. 기존 상품 상세의 가격 비교에는 아직 연결되지 않는다.

기존 판매처 4개를 재사용했다. 실제 DB에서 retailer_listings=85, retailer_offers=85, 가격이 있는 오퍼 79, JAN이 있는 listing 61을 확인했다. 원문 링크·확인 시각·제조사·미매칭 이유·옵션 조건도 조회할 수 있다.

## 구현

- `backend/app/models/retail.py`에 판매처 listing과 현재 offer 모델을 추가했다.
- `backend/alembic/versions/20261116_retail_offers.py`를 적용했다. 기존 `retailers`, `figures`, `figure_variants`, 가격 관측 테이블은 유지하고 신규 테이블을 추가했다.
- `backend/app/services/retail_collection.py`에서 출처·상품 ID·옵션 키를 기준으로 listing을 upsert하고 현재 offer를 트랜잭션으로 저장한다. NULL 가격과 0원을 구분하고 과거 관측은 최신값을 덮어쓰지 않는다.
- 기존 `preview_domestic_prices`에 `--commit`을 추가했다. 기본은 dry-run이며 `--commit`을 명시하면 상품별로 저장 후 진행 보고서를 기록한다. 출처별 제한은 최대 100건이고 이번 실행은 30건이다.
- `backend/app/api/retail_offers.py`와 앱 라우터 연결을 추가했다. 공개 GET 조회만 제공하며 조회가 수집을 실행하지 않는다.
- 데이터 재이용 정책 상태는 각 출처 보고서의 `REQUIRES_PERMISSION_FOR_SERVICE_REUSE`에 계속 기록했다. 이번 요청의 일회성 로컬 수집과 별도로 상시 운영·외부 표시 범위는 판매처 조건을 확인해야 한다.

## 실제 실행

```powershell
docker compose build backend
docker compose run --rm --no-deps backend alembic upgrade head
docker compose run --rm --no-deps -v "${PWD}/data/private/retail_price:/retail-reports" backend python -m scripts.preview_domestic_prices --execute --commit --sources maniahouse comics_art figurefarm --limit 30 --report-dir /retail-reports/20261116_domestic_collection
docker compose up -d --no-deps backend
```

수집 보고서는 `data/private/retail_price/20261116_domestic_collection/preview.json`이다. 재실행 시 보고서 경로는 새 이름을 사용한다. 저장 고유키는 그대로 유지되므로 기존 판매처 상품의 정보가 갱신된다.

## 조회

- 전체 저장 목록은 `http://localhost:8080/api/retail-offers`에서 확인한다.
- 매니아하우스는 `?source=maniahouse`, 코믹스아트는 `?source=comics_art`, 피규어팜은 `?source=figurefarm`으로 필터링한다.
- JAN은 `?jan=4535123716737`, 검색은 `?q=나미`, 판매 상태는 `?availability=PREORDER`를 사용한다.
- `page`, `size`로 페이지를 지정하며 size 최대값은 100이다. 응답에 관측 시각과 stale을 표시한다.

기존 상품 UI 변경은 이번 실행에 포함하지 않았다. 현재 판매처 목록 API에서 독립 저장된 가격을 확인하는 단계다.

## 검증

신규 저장·최신값 보호·NULL 가격·기존 판매처 재사용·조회 필터·마이그레이션 upgrade/downgrade를 SQLite 격리 테스트에서 검사했다. 실제 PostgreSQL에서는 수집 저장 후 동일 관측 1건을 다시 적용해 매니아하우스 listing 수가 30→30으로 유지되는 것을 확인했다.

```powershell
docker compose run --rm --no-deps backend python -m pytest -q
# 343 passed, 18 skipped
python tools/check_structure.py
# python_sources 164, frontend_sources 40, errors []
```

18개 통합 테스트는 별도 PostgreSQL 테스트 DB 미설정으로 건너뛰었다. 가격 API의 전체·출처별·JAN별 조회와 기존 행사 API·health 응답도 확인했다. 이 결과는 이번에 수집한 페이지 범위의 저장 검증이며 판매처 전체 상품을 수집한 건수는 아니다.
