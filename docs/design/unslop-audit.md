# O_DOCK 디자인 점검 · 2026-11-17

## 환경
Vue 3.5, Vue Router 4.5, Pinia 3, Vite 6.4, Tailwind 3.4 및 Lucide를 유지한다. API 계약과 인증은 `services`와 `stores`에 있다. 프론트는 Compose의 nginx 서비스로 8080 포트에서 제공한다.

스타일은 `style.css → home-design.css → white-theme.css → events.css` 순으로 중첩됐다. 마지막 화이트 테마가 이전 색상을 덮어쓰고, 상품 상세 레이아웃도 함께 정의한다. 기존 Apple SD Gothic 폴백을 우선 유지한다.

## Unslop 적용
[공식 저장소](https://github.com/heydamir/unslop)의 `skills/unslop`을 `docs/design/skills/unslop`에 설치했다. 설치된 SKILL.md, signs, tokens 및 체크리스트를 읽었다. 작성자는 Damir Sokolovsky, 라이선스는 CC BY 4.0이다. 이번 세션에서는 문서를 직접 읽어 적용했으며, 자동 스킬 검색에는 다음 세션부터 반영될 수 있다.

명세가 실제 구현과 검증까지 승인하고 디자인 방향도 지정하므로 별도 방향 승인 대기 없이 진행한다. 스킬의 이미지 생성 제안보다 실제 상품 이미지를 사용하라는 사용자 요구가 우선한다.

## 디자인 방향
- 제품: 피규어와 서브컬처 행사를 찾고 개인 컬렉션을 관리하는 서비스.
- 성격: 차분함, 선명함, 수집의 밀도.
- 공간: 어두운 전시 공간과 밝은 상품 촬영 배경.
- 시각적 중심: 대표 상품 사진과 행사 포스터.
- 서명: O_DOCK의 밑줄과 선택 표시를 잇는 작은 오렌지.

## 페이지별 발견 사항
| 우선순위 | 대상·파일 | 문제 / 심각도 | 개선 방향 | 기능 위험 |
|---|---|---|---|---|
| P0 | App.vue / 공통 CSS | 헤더 브랜드 부재, 모바일 메뉴 밀집 / 높음 | 워드마크, 접이식 메뉴, 본문 건너뛰기 | 낮음: 라우트 유지 |
| P0 | style.css, home-design.css, white-theme.css | 중복 색상과 서로 다른 테마 / 높음 | 재사용 토큰, 색상 선언 통합 | 중간: 모든 페이지 확인 |
| P1 | HomeView.vue | 획일적인 제조사 카드, 실제 로그인과 어긋나는 예정 문구 / 중간 | 선으로 구분한 목록, 실제 기능 문구 | 낮음 |
| P1 | FigureCard.vue, HomeProductCard.vue | 작은 메타 글씨, multiply 혼합, 오류 이미지 상태 미흡 / 높음 | 실제 색 보존, 오류 안내, 제목 위계 | 낮음: 클릭·관심 액션 유지 |
| P1 | FigureListView.vue | 좁은 필터, 모바일 필터 길이 / 중간 | 반응형 필터와 일정한 카드 그리드 | 중간: 쿼리 동작 유지 |
| P1 | FigureDetailView.vue, DomesticPrices.vue | 사진과 텍스트 균형, 가격 표의 작은 글씨 / 높음 | 넓은 사진, 가격 위계, 표 대비 | 중간: 가격 계산 유지 |
| P1 | EventsView.vue, events.css | 별도 파란 테마, 작은 날짜·장소, 장식 회전 / 중간 | 공통 테마, 읽기 쉬운 메타, 포스터 우선 | 중간: 필터·대화상자 유지 |
| P2 | 계정·검색·관심·구매·AI·상태·가격 화면 | 패널과 입력의 테마 불일치 / 중간 | 공통 표면·입력·포커스 | 낮음: 서비스 로직 불변 |

변경 전 화면은 `screenshots/before-*`, 구조 점검은 `before-checks.json`에 보관한다. 브라우저 연결 도구가 응답하지 않아 별도 Playwright/Chromium 테스트 환경을 사용했다. 사용자의 데이터가 바뀌지 않도록 브라우저 검증 중 API 쓰기 요청을 차단한다.
