# 국내 판매처 가격 모델·매칭 설계

이 문서는 정책 게이트에서 작성한 구현 설계다. 마이그레이션과 운영 저장 경로는 적용 전이다.

## 기존 모델 확장

상품 연결은 기존 `figure_variants.id`를 기준으로 한다. `figure_id`만 연결하면 재판·한정판을 구별하기 어렵다. 상품 단위 정보는 variant의 `figure_id`로 조회한다.

| 모델 | 제안하는 최소 변경 |
|---|---|
| 기존 `retailers` | nullable unique `code`, `verification_status`, `verification_scope`, `collection_status`, `terms_reviewed_at`, `permission_evidence_url`, 기본 false `collection_enabled` 추가 |
| 기존 `seller_verifications` | 제조사별 판매점 근거와 검증 시각 보관에 재사용 |
| 신규 `retailer_listings` | retailer_id, external_product_id, option_key, canonical_url, title_raw, manufacturer_raw, jan_ean, model_code, edition_raw, scale_raw, reissue_no, bonus_status, is_set, nullable catalog_variant_id, match_status, match_evidence, first_seen_at, last_seen_at |
| 신규 `retailer_offers` | listing_id unique, currency, nullable integer list_price/sale_price/shipping, availability, price_basis, conditions, observed_at, source_url, observation_hash |
| 기존 `retail_price_records` | 현재 조회·승인된 파일 가져오기 경로 유지. 새 수집 결과를 연결할 때는 매칭 확정·무조건부 일반 판매가만 이 경로에 전달하는 후속 호환 설계 필요 |

listing 고유키는 `(retailer_id, external_product_id, option_key)`로 한다. 옵션이 없는 상품의 option_key는 빈 문자열이다. 외부 ID가 없으면 정규화 URL 해시를 외부 키로 사용한다. 같은 canonical URL의 서로 다른 옵션은 허용한다. 같은 업체의 www 유무는 출처에 명시된 별칭으로 정규화한다.

Cafe24 상품 URL은 검증된 `product_no`를 보존하고 cate_no·display_group·추적 query·fragment를 제거한다. 같은 ID의 URL 별칭은 중복 listing을 만들지 않는다. 옵션 식별자는 실제 출처에 있을 때만 사용하며 불명확하면 상품 수준 `REVIEW_REQUIRED`로 남긴다.

## 저장 일관성과 가격

원문→정규화 검증이 끝난 한 관측을 단일 트랜잭션으로 listing upsert와 현재 offer upsert에 반영한다. 관측시각이 기존보다 오래된 입력은 최신 offer를 덮어쓰지 않는다. unique 제약과 DB upsert를 함께 사용해 동시 재시도 중복을 막는다. 같은 관측 ID 재전송은 no-op이며, 새로운 확인 시각의 같은 가격은 last_seen/observed_at을 갱신한다.

KRW 가격은 NULL 또는 0 이상 정수다. NULL과 0을 구분하고 0원도 제목·가격 조건이 확인되기 전 최저가에 포함하지 않는다. 예약금·잔금·회원가·쿠폰가·옵션 범위는 `price_basis`와 `conditions`에 원문 조건을 기록한다. 명확한 일반 판매가가 없으면 sale_price=NULL로 둔다. list_price는 해당 몰의 정가 표시 근거이며 제조사 발매가로 승격하지 않는다.

현재 오퍼만 보관하는 구조를 우선한다. 별도 가격 이력 추가는 보관 목적·기간·판매처 이용 조건을 정한 후 검토한다. 수집 누락만으로 품절을 추정하지 않는다. offer의 관측 시각으로 신선도를 산출하며 오래된 값은 화면에서 ‘확인된 가격’과 확인일을 표시한다.

판매 상태는 IN_STOCK / PREORDER / SOLD_OUT / COMING_SOON / UNKNOWN이다. 명시적인 품절 표시를 예약 제목보다 우선하고, 재고 소진이라는 일반 안내만으로 품절 판정하지 않는다. 상충하는 표시나 예약·입고일만으로 판매 여부가 불명확하면 UNKNOWN이다. 기존 가격 조회에 연결할 때 in_stock / preorder / sold_out / unknown으로 변환하며 COMING_SOON은 별도 표시를 보존한다.

## 매칭 결정

JAN/EAN은 체크디지트 검증 후 동일 코드의 모든 카탈로그 후보를 조회한다. 제조사·스케일·판본·재판·특전·옵션·세트의 명시적 충돌이 하나라도 있으면 거절한다. 관련 변형 정보를 확인하지 못했거나 같은 코드에 여러 버전이 있으면 `REVIEW_REQUIRED`다. 정확한 식별자와 버전 확인 근거가 있는 유일 후보만 `MATCHED`로 확정한다.

SKU는 제조사 원래 모델번호임이 확인될 때 제조사 정규화와 함께 비교한다. 판매처 내부 품번은 제조사 SKU와 동일시하지 않는다. 이름·작품·스케일·버전 비교는 후보 제시만 수행하고, 코드와 동일 버전 근거가 부족하면 수동 확인 대상으로 둔다. 현재 코드가 반환하는 `MATCH_REVIEW_REQUIRED`와 신규 설계의 `REVIEW_REQUIRED`는 어댑터 경계에서 변환한다.

기존 `match_product`는 코드·제조사·스케일·판본·세트 검사에 재사용 가능한 부분이 있다. 다만 JAN 일치 시 반환하기 전에 SKU 등 뒤쪽 식별자 충돌을 모두 확인하는 구조가 아니며, 재판번호 결측은 자동 확정을 막지 않는다. 신규 연동에서는 모든 충돌·필수 버전 근거를 먼저 검사해야 한다. 현재 함수의 동작 변경은 이번 정책 조사 단계에 포함하지 않았다.

| 경계 사례 | 목표 판정 |
|---|---|
| 정확한 JAN, 제조사·일반판·스케일·옵션 확인, 유일 후보 | MATCHED |
| JAN 동일, 제조사 SKU는 서로 다름 | REJECTED 또는 원문 확인 전 REVIEW_REQUIRED |
| JAN 동일, 카탈로그는 재판 2차이나 판매처 재판 정보 없음 | REVIEW_REQUIRED |
| 캐릭터명만 동일 | REVIEW_REQUIRED |
| 일반판과 샵특전 포함판 | 별도 listing, 일반판 자동 연결 거절 |
| 동일 상품이나 예약금만 표시 | 상품 매칭 근거와 별개로 일반 최저가 비교 제외 |
| 단품과 세트, 색상·사이즈 불일치 | REJECTED |

수동 검토는 match_status·후보 variant ID·필드별 근거·충돌 이유·검토자 결정·관측 hash를 저장하는 관리 절차로 설계한다. 원문 또는 카탈로그 식별 근거가 바뀌면 종전 결정을 다시 검증한다. 이 작업은 행사 검수함과 별개인 가격 매칭 설계이며 새로운 화면은 구현 전이다.

## 후속 마이그레이션·UI 검증

기존 행은 nullable 컬럼과 false 기본값으로 유지한다. retailer code는 기존 업체와 도메인 별칭을 확인한 뒤 backfill한다. 신규 테이블 및 인덱스만 먼저 추가하고, downgrade는 신규 테이블과 신규 컬럼만 대상으로 한다. 실제 rollback 검증은 별도 테스트 DB에서 upgrade→동일 입력 반복→downgrade를 확인해야 한다.

상세 UI 제안은 판매처명, 가격·조건, 판매 상태, 구매 원문 링크, 마지막 확인 시각, 오래된 관측 표시다. 현재 최저가 계산 규칙과 호환되는 매칭 확정·무조건부·신선한 재고 오퍼만 최저가에 사용한다.
