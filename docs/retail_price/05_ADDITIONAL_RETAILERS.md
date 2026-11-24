# 추가 국내 판매처 발견 결과

2026-11-16 조사한 추가 후보 5곳이다. 굿스마일 제조사 한국 판매점 목록에서 업체와 사이트 링크를 대조했다. 지위 확인 범위는 해당 제조사 판매점이며 업체 전체의 모든 제조사 총판 지위를 의미하는 라벨로 사용하지 않는다. [제조사 판매점 목록](https://partner.goodsmile.info/support/eng/partnershops/kr/)

| 후보 | 발견·상품 URL 구조 근거 | 지위 | 운영 주체·정책·중복 상태 |
|---|---|---|---|
| 논노21 | `https://nonno21.com/`, 홈 상품 링크는 `/shop/shopdetail.html?branduid=...` | VERIFIED_OFFICIAL, GSC Partner Shop | 법인 정보 추가 확인 필요. 홈 상품 접근, 상세 표본 cache miss. 정책 UNKNOWN. 기존 판매처 4곳과 별개 |
| 피규어팜 | `https://www.figurefarm.net/`, 홈에 예약·입고·품절과 상품 링크 | VERIFIED_OFFICIAL, GSC Partner Shop | 홈 운영 주체 주식회사 토이앤테크. 정책 UNKNOWN. 기존 DB 판매처 재사용 대상 |
| 조이하비 | `https://www.joyhobby.co.kr/`, `/mall/main.asp?siteid=joyhobby&`로 이동하며 상품 링크 노출 | VERIFIED_OFFICIAL, GSC Partner Shop | 신도림 매장 등재와 사이트 연결 확인. 사업자 명칭 추가 확인 필요. 정책 UNKNOWN. 일반 취미품이 섞여 IP 선별 필요 |
| 코믹스아트 | `https://www.comics-art.co.kr/`, 홈에 상품·제조사·가격 링크 | VERIFIED_OFFICIAL, GSC Other Authorized Retailer | 홈 운영 주체 주식회사 삼나무. 정책 UNKNOWN. 기존 DB 판매처 재사용 대상 |
| 하비팩토리 | `https://www.hobbyfactory.kr/`, 제조사 목록에서 공식 사이트 링크 확인 | VERIFIED_OFFICIAL, GSC Other Authorized Retailer | 홈 열기에서 리디렉션 루프 관측. 운영 주체·상품 상세·정책 UNKNOWN. 자동 수집 연결 보류 |

각 후보의 robots·약관·피드·제휴 조건은 추가 검토 대상이다. 이번 발견만으로 ALLOW로 분류한 후보는 0곳이다. 하비팩토리는 상품 URL 자체를 검증하지 못했으므로 구현 우선순위에서 보류한다. [논노21](https://nonno21.com/), [피규어팜](https://www.figurefarm.net/), [조이하비](https://www.joyhobby.co.kr/), [코믹스아트](https://www.comics-art.co.kr/)

네이버 스마트스토어 링크를 사용하는 업체는 이 목록에서 제외했다. 기존 히어로타임도 별도 업체를 중복 등록하는 대신 기존 판매처를 재검토하는 대상으로 둔다.
