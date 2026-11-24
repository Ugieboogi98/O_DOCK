# 국내 판매처 가격 수집 POC 결과

후속 요청으로 실제 소량 dry-run을 실행했다. 최신 결과와 코드 변경은 `07_POC_RUN_20261116.md`를 확인한다. 아래 내용은 최초 조사 단계 보고다.

확인일은 2026-11-16이다. 첨부 지시서의 Phase A·B와 권한 대기 상태에서 가능한 모델·매칭 설계 및 후보 조사를 수행했다. 실제 상품 POC는 `NOT_RUN_REQUIRES_PERMISSION`이며 운영 연결은 미구현이다.

## A. 조사한 기존 코드와 재사용 지점

`00_CURRENT_STATE.md`에 구조, 실제 모델·서비스·수집기·마이그레이션 위치를 기록했다. 기존 `Retailer`, `SellerVerification`, `RetailPriceRecord`, JSON-LD 파서, `SafeFetcher`, `match_product`, 승인된 파일 가져오기와 가격 조회 서비스를 재사용하는 설계다.

DB 읽기 전용 집계는 상품 6,161건·버전 6,162건·JAN 보유 버전 3,362건·SKU 보유 버전 1,125건·국내 판매처 가격 관측 0건이다. 한국어 번역 작업의 저장 진행과 이 가격 관측 집계는 다른 테이블의 데이터다.

## B. 기존 수집처와 중복 여부

매니아하우스·히어로타임·피규어팜·코믹스아트는 이미 판매처로 등록돼 있다. 신규 연동 시 기존 retailer를 사용해야 한다. BNKR 국내 가격 파서와 제조사 기준 카탈로그도 존재한다. 새 listing/offer 설계는 미매칭 판매처 상품 보관과 조건부 가격·버전 확인을 보완한다.

## C. 판매처별 정책·권한 상태

| 판매처 | 권한 상태 | 실제 접근 관측 |
|---|---|---|
| 매니아하우스 | REQUIRES_PERMISSION | 홈·목록·robots·약관 HTTP 200, 상세 내용 확보 실패 |
| 피규어프레소 | REQUIRES_PERMISSION | 홈·목록·robots·약관 HTTP 200, 상세 challenge 접근 차단 관측 |
| 추가 후보 5곳 | UNKNOWN | 공개 링크·제조사 판매점 등재 중심 발견 단계 |

두 우선 사이트의 약관 제22조를 확인했으며 O_DOCK의 가격 수집·상업적 표시 이용 허가 증거는 확보하지 못했다. 첨부 지시서 Phase B가 불확실한 경우 검증 보고·구현 설계까지 진행하도록 정하므로 해당 범위에서 종료했다. robots의 공개 상품 경로 허용만으로 운영을 허용 처리하지 않았다. [매니아하우스 약관](https://maniahouse.co.kr/member/agreement.html), [피규어프레소 약관](https://www.figurepresso.com/member/agreement.html)

## D. 매니아하우스 POC 결과

상세 파싱 POC 표본 0개, DB 저장 0건이다. 가격·JAN·상태·매칭 정확도는 분모가 0이므로 산출하지 않았다. `02_MANIAHOUSE_POC.md`와 `maniahouse_public_observation.json`에 공개 홈 관측 1건과 표본 수집 계획을 기록했다. 홈 관측은 파서 검증이나 정확도 측정에 사용하지 않았다.

## E. 피규어프레소 및 추가 후보 검토

논노21·피규어팜·조이하비·코믹스아트·하비팩토리 5곳을 발견했다. `05_ADDITIONAL_RETAILERS.md`에 도메인, 제조사 등재 범위, 운영 주체 확인 수준, 접근 실패, 기존 DB 중복 여부를 기록했다. 각 업체의 정책 상세 조사는 후속 검토 대상이다. [굿스마일 한국 판매점 목록](https://partner.goodsmile.info/support/eng/partnershops/kr/)

## F. DB 스키마·매칭 규칙 변경 사항

`03_DATA_MODEL_AND_MATCHING.md`에 기존 retailer 확장, variant를 nullable로 연결하는 listing, 조건·관측 시각을 갖는 현재 offer, idempotent upsert, 변형별 매칭, 수동 확인 절차, UI 명세를 작성했다. 스키마 변경·함수 변경·마이그레이션 적용은 0건이다.

기존 `match_product`에 합성 식별자를 넣는 읽기 전용 재현에서 JAN 동일·SKU 충돌 사례와 JAN 동일·카탈로그 재판번호 2/판매처 재판 결측 사례가 모두 `MATCHED`를 반환했다. 합성 JAN `123`을 사용한 분기 검증이며 실제 상품 매칭 사례는 아니다. 새 연동 전 모든 식별자 충돌 검사와 판본 근거 확인을 선행하도록 설계했다.

## G. 변경 파일 목록 및 테스트 명령·결과

이번 요청으로 생성한 문서는 아래와 같다.

- `docs/retail_price/00_CURRENT_STATE.md`
- `docs/retail_price/01_SOURCE_AUDIT.md`
- `docs/retail_price/02_MANIAHOUSE_POC.md`
- `docs/retail_price/03_DATA_MODEL_AND_MATCHING.md`
- `docs/retail_price/04_PERMISSION_REQUEST.md`
- `docs/retail_price/05_ADDITIONAL_RETAILERS.md`
- `docs/retail_price/06_RESULT.md`
- `docs/retail_price/maniahouse_public_observation.json`
- `docs/evidence/retail_price_20261116.json`

실행한 검증은 다음과 같다.

```powershell
docker compose run --rm --no-deps backend python -m pytest tests/test_collectors_and_import.py tests/test_catalog_pipeline.py tests/test_api.py -q
# 35 passed, 13 skipped
docker compose run --rm --no-deps backend python -m pytest tests/test_quality.py -q
# 13 passed
python tools/check_structure.py
# python_sources 157, frontend_sources 40, errors []
```

두 JSON 파일도 JSON 파싱에 성공했다. 건너뛴 13개는 별도 PostgreSQL 테스트 DB 설정이 필요한 통합 테스트다. 실제 POC·새 파서 fixture·신규 upsert·마이그레이션/rollback 검증은 구현과 허가된 입력이 없어 미실행이다. 기존 테스트 통과를 새 판매처의 정확도 검증으로 해석하지 않는다.

기존 `.env` 제외 규칙은 확인했으며 현재 폴더의 Git 추적 상태는 메타데이터 부재로 확인하지 못했다. 보고 자료에는 응답 헤더의 쿠키, API 키, 인증 challenge query, 고객 정보 및 리뷰 본문을 넣지 않았다.

## H. 운영 활성화 전 남은 승인·위험 요소

판매처로부터 수집 대상 필드·페이지·빈도·서비스 내 표시·보관 범위에 대한 허용 증거가 필요하다. 피규어프레소는 상세 접근 제한 해결을 판매처 공식 피드나 승인된 접근 방식으로 확인해야 한다. 매니아하우스는 상세 페이지와 JAN 노출 및 예약금·특전 조건을 실제 표본으로 검증해야 한다.

## I. 다음 작업 제안

`04_PERMISSION_REQUEST.md`의 문안으로 데이터 제휴 창구와 허용 범위를 확인한 뒤 Phase C의 최대 5개 dry-run을 진행한다. 허용된 표본의 파싱·매칭 지표와 격리 DB 반복 저장 검증을 마친 후 운영 활성화 요청을 구체화한다.
