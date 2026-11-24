# 국내 판매처 기술·정책 조사

2026-11-16 공개 페이지를 확인했다. 직접 HTTP 응답코드·응답 SHA-256·robots 규칙은 `docs/evidence/retail_price_20261116.json`에 기록했다. 아래 상세 페이지 실패는 웹 조회 도구의 관측이며 원본 서버의 확정 HTTP 코드로 해석하지 않는다.

## 우선 판매처

| 항목 | 매니아하우스 | 피규어프레소 |
|---|---|---|
| 홈 | `https://maniahouse.co.kr/`, HTTP 200 | `https://www.figurepresso.com/`, HTTP 200 |
| 목록 | `/product/list.html?cate_no=45`, HTTP 200 | `/product/preorder.html?cate_no=24`, HTTP 200 |
| 상세 표본 URL | `/product/detail.html?product_no=26604` | `/product/detail.html?product_no=80537` |
| 상세 접근 | 홈 링크 열기에서 cache miss, 내용 미확인 | 홈 링크 열기에서 Cafe24 challenge로 이동, 접근 차단 관측 |
| 정적 HTML | 홈에 상품명·판매가·제조사 노출 | 홈·예약 목록에 상품명·가격 노출 |
| 상태 근거 | 예약·입고완료·샵특전 등의 제목 구분 | 예약·재판·한정 등의 제목 구분 |
| JAN·모델번호 | 상세 검증 전, 확인하지 못함 | 상세 검증 전, 확인하지 못함 |
| 목록 구조 | `cate_no` 기반, 페이지 순회 미검증 | `cate_no` 기반, 페이지 순회 미검증 |
| 외부 상품 식별자 | `product_no`, 추적 query 제거 필요 | `product_no`, 추적 query 제거 필요 |
| robots | HTTP 200, 공개 `/product/` 금지 규칙 없음 | HTTP 200, 공개 `/product/` 금지 규칙 없음 |
| 약관 | `/member/agreement.html`, HTTP 200, 제22조 확인 | `/member/agreement.html`, HTTP 200, 제22조 확인 |
| 수집·이용 허용 | `REQUIRES_PERMISSION` | `REQUIRES_PERMISSION` |
| 기술 접근 상태 | 상세 검증 미완료 | 상세 `BLOCKED` 관측 |
| 운영 활성화 | 보류 | 보류 |

두 사이트의 robots는 관리·회원·비공개 API·게시글 쓰기 등의 경로를 금지한다. `Crawl-delay: 10`은 bingbot 그룹에 있으며 공통 사용자 에이전트 규칙으로 오해하지 않는다. 후속 허가된 표본 수집은 단일 요청 처리와 최소 3초 간격, 실제 적용되는 robots 지연 중 큰 값을 사용하도록 설계한다.

두 사이트의 약관 제22조는 몰에 지적재산권이 귀속되는 정보의 영리 목적 이용에 사전 승낙을 요구한다. 가격 사실 필드의 구체적인 허용 범위와 O_DOCK 재표시 권한을 확보했다는 증거가 없어, 첨부 지시서 Phase B에 따라 `REQUIRES_PERMISSION`으로 판단했다. 피규어프레소는 디자인·이미지 무단 사용 제한도 별도로 표시한다. [매니아하우스 약관](https://maniahouse.co.kr/member/agreement.html), [피규어프레소 약관](https://www.figurepresso.com/member/agreement.html)

## 판매점 지위

굿스마일 제조사의 한국 판매점 목록에 MANIAHOUSE와 Figure Presso가 등재돼 있다. 두 업체의 `VERIFIED_OFFICIAL` 근거 범위는 굿스마일 판매점 등재다. 다른 제조사 전체의 공식 총판 지위와 데이터 이용 허용까지 확대하지 않는다. 등록 시 `verification_scope=goodsmile_authorized_retailer`와 근거 URL·확인일을 함께 보관하는 설계다. [제조사 한국 판매점 목록](https://partner.goodsmile.info/support/eng/partnershops/kr/)

## API·피드·제휴

확인한 홈·약관·목록에서 제3자용 공개 가격 API·CSV 피드 및 O_DOCK 이용 허가를 찾지 못했다. Cafe24 플랫폼 API의 존재만으로 개별 몰 데이터 접근 권한을 확보했다고 판단하지 않는다. 매니아하우스 홈의 일반 연락 이메일은 `maniahouse801@gmail.com`이며 피규어프레소는 홈의 도매문의·고객센터를 문의 경로로 사용할 수 있다. 제휴 문안은 `04_PERMISSION_REQUEST.md`에 준비했다. [매니아하우스](https://maniahouse.co.kr/), [피규어프레소](https://www.figurepresso.com/)

## IP 상품 선별과 후속 검증

허가 후 피규어·애니메이션·게임·만화·웹툰·소설 IP 굿즈 카테고리만 표본으로 삼는다. 일반 생활용품·비IP 잡화·쿠폰 안내·회원 전용 상품은 제외한다. 제목과 제조사·작품 정보의 원문 근거를 보존하고, 특전·재판·단품/세트·예약금/잔금 표시는 매칭·가격 조건 필드에 반영한다. 제목 끝의 짧은 숫자를 JAN으로 추정하지 않는다.

스마트스토어는 지시서에 따라 제외했다. 추가 후보는 `05_ADDITIONAL_RETAILERS.md`에 발견 결과만 기록했다.
