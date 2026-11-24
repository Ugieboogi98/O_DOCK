# 국내 판매처 3곳 수집 확장 결과

2026-11-16 사용자가 지정한 매니아하우스·코믹스아트·피규어팜을 일회성 미리보기 대상에 연결했다. 기존 실행 범위에 맞춰 각 5건을 확인하는 dry-run으로 진행했다.

## 최종 실행 결과

| 판매처 | 상품 상세 추출 | 판매가 확보 | 유효 JAN 확보 | 판매 상태 | 오류 |
|---|---:|---:|---:|---|---:|
| 매니아하우스 | 5/5 | 5/5 | 5/5 | 예약 5건 | 0 |
| 코믹스아트 | 5/5 | 5/5 | 4/5 | 예약 5건 | 0 |
| 피규어팜 | 5/5 | 5/5 | 1/5 | 예약 5건 | 0 |
| 합계 | 15/15 | 15/15 | 10/15 | 예약 15건 | 0 |

최종 보고서는 `data/private/retail_price/20261116_three_stores_verified/preview.json`에 있다. 이전 `20261116_three_stores` 실행은 코믹스아트의 미래 발매 예약 상태 보완 전 결과이므로 최종 상태 확인에는 verified 보고서를 사용한다.

기존 카탈로그에서 일치하는 JAN 후보는 0건이다. JAN 미확인 5건은 식별자 확인이 필요한 상태로 기록했다. 매니아하우스와 피규어팜에는 JAN `4535123716737`의 원피스 나미가 함께 노출됐고 두 몰의 표시 전액 가격이 각각 221,000원이었다. 이는 판매처 사이의 공통 코드 관측이며, 기존 상품에 확정 연결한 결과는 아니다. 옵션·판본을 확인한 뒤 연결해야 한다.

## 구현과 검증

`backend/app/collectors/retailers/preview_sources.py`에 세 출처의 정확한 호스트·시작 URL·파서 연결을 등록했다. `--sources`로 실행 대상을 선택하며 기본 대상 매니아하우스는 유지했다. 세 출처를 실행하면 출처별 결과와 오류, 전체 결과를 한 보고서에 기록한다. 출처별 접근 실패가 발생해도 다른 출처의 순차 실행은 계속된다.

코믹스아트는 Cafe24 상세 라벨이 li/div 구조이므로 기존 테이블 기반 파서를 확장했다. JAN CODE, 제조사, 판매가를 읽고 ‘1차결제/전체결제’ 옵션을 구분한다. 주문 가능 Offer의 InStock 표시와 별개로 명시된 미래 발매 연도·월·분기를 확인해 예약 상태를 보완한다.

피규어팜은 `figurefarm.py`의 별도 어댑터를 사용한다. 홈페이지의 `.ff-products` 안에서만 상품 링크를 발견해 배너·일반 링크를 제외한다. `#detail`의 구매 form 안에서 가격·제조사와 결제 옵션을 읽는다. 제조사 필드에 노출된 13자리 JAN은 체크디지트를 검증한다. 숨겨진 품절 안내와 비활성 잔금 옵션을 상품 전체 품절로 판정하지 않는다.

두 추가 사이트의 robots 응답은 HTTP 200이었다. 코믹스아트 공개 상품 경로는 관측된 금지 경로에 포함되지 않았으며 피규어팜은 관리 경로를 금지하고 있다. 코믹스아트의 MSF 목록은 웹 조회 도구에서 접근 확인 화면으로 이동했지만, 이번 실행은 공개 홈페이지에 노출된 상세 링크를 순회했고 실제 상세 응답이 정상이어야만 처리했다. 접근 확인 화면을 우회하는 코드는 없다.

기존에 조사한 판매처 재이용 허가 상태는 보고서의 `REQUIRES_PERMISSION_FOR_SERVICE_REUSE`에 기록했다. 피규어팜 공개 약관의 정보 이용 조건도 후속 운영 범위에 포함해 확인해야 한다. [피규어팜 약관](https://www.figurefarm.net/content/content.php?cont=uselaw)

## 실행 명령

```powershell
docker compose run --rm --no-deps -v "${PWD}/backend/app:/app/app:ro" -v "${PWD}/backend/scripts:/app/scripts:ro" -v "${PWD}/data/private/retail_price:/retail-reports" backend python -m scripts.preview_domestic_prices --execute --sources maniahouse comics_art figurefarm --limit 5 --report-dir /retail-reports/<새로운_실행명>
```

호스트 코드를 일회성 컨테이너에 연결했다. 결과는 로컬 JSON에 저장했으며 DB는 JAN 후보 조회에만 사용했다. 운영 listing/offer 저장과 서비스 가격 표시 연동은 추가 구현 대상이다.

## 검사 결과

```powershell
docker compose run --rm --no-deps -v "${PWD}/backend/app:/app/app:ro" -v "${PWD}/backend/scripts:/app/scripts:ro" -v "${PWD}/backend/tests:/app/tests:ro" backend python -m pytest tests/test_domestic_preview_sources.py tests/test_maniahouse_preview.py tests/test_quality.py -q
# 27 passed
python tools/check_structure.py
# python_sources 161, frontend_sources 40, errors []
```

`test_domestic_preview_sources.py`는 코믹스아트 가격·JAN, 미래 발매 판정, 피규어팜 전액결제·품절·옵션 모호성·JAN, 추적 URL 중복, 출처별 장애 격리를 검사한다. 첫 표본과 최종 표본 모두 각 15개를 추출했으나 실제 품절·할인·단품 선택 등 전체 사례의 일반 정확도는 이번 표본만으로 측정하지 않았다.
