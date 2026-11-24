# 국내 판매처 가격 수집 현재 상태

확인일은 2026-11-16이며, 첨부 작업지시서의 Phase A 조사 결과다.

## 현재 구조와 재사용 지점

| 영역 | 실제 위치 | 확인 결과 |
|---|---|---|
| 프로젝트 경계 | `README.md`, `docs/PROJECT_STRUCTURE.md` | FastAPI, Vue, PostgreSQL, Chroma, Docker Compose |
| 상품 기준 | `backend/app/models/entities.py` | `figures.id`와 버전별 `figure_variants.id`, `sku`, `jan_code`, `edition`, `reissue_no` |
| 판매처 | 같은 파일의 `Retailer`, `SellerVerification` | `retailers`, `seller_verifications`를 재사용 |
| 가격 | 같은 파일의 `RetailPriceRecord` | `retail_price_records.variant_id`는 필수, 현재 미매칭 판매처 상품 보관 불가 |
| 제조사 가격 | `ReleasePrice` | `release_prices`에서 공식 표시가와 발매가 등 구분 |
| 가격 검색 | `backend/app/services/price_refresh.py` | 검색 API → 허용 출처 GET → JSON-LD → 매칭 → 가격 관측 저장 |
| 범용 판매처 파서 | `backend/app/collectors/retailers/jsonld.py` | Product/Offer 추출, AggregateOffer 제외, 판매 상태 정규화 |
| 매칭 | `backend/app/search_agents/matching.py` | JAN/SKU와 제조사·스케일·판본 충돌 검사 |
| 승인된 파일 가져오기 | `backend/scripts/import_observations.py` | 전체 입력 검증 후 트랜잭션, 동일 관측시각 중복 방지 |
| 반다이 국내 가격 | `backend/app/api/korea_prices.py`, `backend/app/collectors/bnkr_prices.py` | BNKR 상세의 판매가 검증과 동일 버전 수동 확인 |
| 가격 조회 | `backend/app/services/prices.py` | 최신 관측, 신선도, 재고, KRW, 매칭 상태로 최저가 산출 |
| HTTP | `backend/app/collectors/safe_http.py` | 공개 HTTPS·DNS·출처·경로 제한, robots, 지연, 응답 크기 제한 |
| 마이그레이션 | `backend/alembic/versions/`, `backend/alembic/env.py` | Alembic, 기존 테이블은 초기 revision부터 존재 |

기존 제조사 어댑터와 국내 BNKR 가격 경로를 중복 작성할 필요가 없다. 신규 작업의 차이는 국내몰 상품을 독립 listing으로 발견하고, 미매칭 상태로 보관한 뒤 상품 버전에 연결하는 부분이다.

## 실제 DB 읽기 전용 집계

2026-11-16 오전 10시 18분경 전체 상품 6,161건, 버전 6,162건, JAN 보유 버전 3,362건, SKU 보유 버전 1,125건이다. 국내 판매처 가격 관측은 0건이다. JAN과 SKU 보유 집계는 단순 비어 있지 않은 값의 수이며 유효성·유일성을 보증하지 않는다.

판매처는 매니아하우스·히어로타임·피규어팜·코믹스아트 4곳이 이미 등록돼 있고 `seller_type=unverified`다. 이번 조사에서 제조사 판매점 등재를 확인했어도 DB 라벨은 변경하지 않았다. 매니아하우스의 기존 URL은 `https://www.maniahouse.co.kr`이며 조사 출처는 `https://maniahouse.co.kr/`다. 추후 명시적인 도메인 별칭으로 같은 업체에 연결해야 한다.

`data/source_policy.json`의 `www.maniahouse.co.kr`는 `enabled=false`다. 피규어프레소는 등록돼 있지 않다. 기존 가격 검색에 필요한 검색 키 설정 여부만 확인했으며 현재 미설정이다. 해당 키는 새 직접 수집 POC의 필수 조건으로 도입하지 않는다.

## 설정과 운영 경계

Compose는 `.env`를 backend에 전달하고 `DATA_DIR=/data`와 DB 연결을 설정한다. 호스트 data는 컨테이너에서 읽기 전용이며 PostgreSQL과 media는 기존 named volume이다. 설정 로딩은 `backend/app/core/config.py`의 `Settings`가 담당한다.

`.gitignore`에는 `.env`, `.env.*`, `data/private/`, 로그·백업 제외 규칙이 있다. 현재 작업 폴더에서는 Git 저장소 메타데이터가 확인되지 않아 실제 추적 여부는 검증하지 못했다. 시크릿 값은 조사·보고서에 포함하지 않았다.

이 작업의 변경 범위는 조사 자료와 설계 문서다. 실제 마이그레이션, 파서 연결, 수집 서비스 등록은 정책 게이트 이후의 단계로 남겼다.
