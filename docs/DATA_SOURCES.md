> 초기 버전 설명입니다. 개인 컬렉션 v2 변경 사항은 README.md와 ../README.md가 우선합니다.

# 수집 데이터와 출처

수집 기준일: 2026-10-21 (한국 시간). 초기 스냅샷의 사실 메타데이터입니다.

| 제조사 | 제품 수 | 확보 방식 |
|---|---:|---|
| Kotobukiya | 30 | 공식 목록의 제품명·속성 |
| MegaHouse | 17 | 공식 목록의 제품명·속성 |
| FuRyu | 46 | 공식 목록의 제품명·속성 |
| Good Smile Company | 9 | 공식 상세 페이지의 사양 |
| Bandai Spirits | 3 | 공식 상세 페이지의 사양 |
| SEGA | 3 | 공식 상세 페이지의 사양 |
| TAITO | 3 | 공식 상세 페이지의 사양 |
| Hot Toys | 3 | 공식 상세 페이지의 사양 |

합계 114건. 작품·캐릭터·치수·일자·가격의 결측은 그대로 유지합니다.
원본 페이지 전문 및 제품 사진을 재배포하지 않고 사실 필드·원문 링크·짧은 사양 발췌만 포함했습니다.
시드 문서는 각 제품의 정형 사실을 묶은 `official_metadata_extract` 유형입니다. 장문의 리뷰/설명 문서가 확보되었다는 뜻은 아닙니다.

## 실제 수집 시작점

- FuRyu: https://furyu-hm.com/
- Kotobukiya: https://www.kotobukiya.co.jp/en/product/
- MegaHouse Look Up: https://megahobby.jp/products/lookup/
- MegaHouse G.E.M.: https://megahobby.jp/products/gem/
- Good Smile 예시: https://www.goodsmile.com/en/product/6143
- Bandai 예시: https://tamashiiweb.com/item/14690/
- SEGA 예시: https://segaplaza.jp/prize/D121425/
- TAITO 예시: https://www.taito.co.jp/taito-prize/0451852500
- Hot Toys 예시: https://www.hottoys.jp/item/view/100008115.php

세부 URL·수집 시각·본문 사실 텍스트는 `data/figures.json`, 전체 상세 URL은 `data/seed_urls.txt`에 있습니다.
확인일은 관측 시각이고 제품 발매일이 아닙니다. 2027년 발매 예정 제품도 공식 목록에 포함되어 있습니다.

## 접근 및 이용 조건

공개 정보 확인과 대량 자동 수집·이미지 이용 권한은 별개입니다.
Good Smile robots는 검색 경로를 제외하도록 안내하며 해당 경로로 수집하지 않았습니다.
Hot Toys 홍콩 사이트는 확인 시 403 응답이어서 접근을 우회하지 않고 일본 공식 상세 페이지를 이용했습니다.
일부 다른 시작 페이지는 JavaScript 중심이라 제품 상세 URL을 공개 검색으로 발견한 뒤 확인했습니다.
자동 수집 지속 허가는 모두 미확정 상태이므로 배포 기본 정책은 `enabled: false`입니다.

공식 조건 확인 링크(변경 가능):
- https://www.goodsmile.com/en/terms-of-use/
- https://www.bandaispirits.co.jp/site/notice/
- https://www.taito.co.jp/guideline
- https://www.hottoys.jp/info/about.html

후류·메가하우스·세가·코토부키야 및 판매처별 현재 약관/데이터 이용 정책을 확인하여 실제 허용 범위와 증빙을 `source_policy.json`에 기록해야 합니다. 권한을 확보했다고 표시하지 않았습니다.

## 가격 정확성

현재 공식 가격 관측은 일본 공식 목록/상품 페이지의 **표시가**이며 `official_list`입니다.
일본 공식 최초 발매 엔가를 입증하지 못했으므로 `official_release`로 자동 승격하지 않습니다.
국내 판매 가격과 중고 매물의 초기 수량은 0입니다. 예시 수치나 과거 설계서의 가상 가격을 실제 DB에 넣지 않았습니다.
메루카리 JPY와 한국 플랫폼 KRW는 별도로 집계하며 환산/국제 운송비 추정은 하지 않습니다.
