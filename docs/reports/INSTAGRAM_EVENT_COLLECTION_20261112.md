# 팝업·전시·콜라보 카페 수집 실행 결과

이후 사용자 요청으로 이미지 93장을 추가 수집했다. 최신 목록은 `data/private/instagram/20261112_1354_images/review.html`, 상세는 [이미지 수집 보고서](INSTAGRAM_EVENT_IMAGES_20261112.md)에 있다. 아래 ‘이미지 미다운로드’는 최초 본문 수집 단계 기록이다.

2026-11-12 13:40 KST, 실제 공식 API 가용성 검증 성공 이후 수동 1회 수집을 실행했다. 사용자 요청에 따라 **팝업·팝업스토어·전시회·콜라보 카페**를 대상으로 한다. 기존 상품 수집·번역·분류 작업을 재실행하거나 변경하지 않았다.

## 실제 결과

| 항목 | 건수 |
|---|---:|
| duex.official 원문 | 10 |
| anique.jp 원문 | 10 |
| akplaza_hongdae 원문 | 10 |
| 저장된 원본 게시물 합계 | 30 |
| 행사 검수 후보 게시물 | 18 |
| 행사 아님 | 10 |
| 서브컬처 근거 없음 | 2 |
| 공개 행사 | 0 |

검수 후보는 전시 관련 8건·팝업 관련 10건이다. 콜라보 카페 판별 규칙과 테스트는 구현했지만 이번 최근 30건에서 명시적인 콜라보 카페 게시물은 발견하지 못했다. 전시의 음료 메뉴 공지를 별도 콜라보 카페 개최로 확대 해석하지 않았다.

18개는 **고유 행사 수가 아니라 게시물 수**다. 동일 전시·팝업의 카운트다운·굿즈·예매 안내 등이 포함돼 있다. 작품·기간·장소가 모두 있는 경우 가능한 중복 그룹 4개를 표시할 수 있지만 자동 병합·확정하지 않는다. 검수 후보 중 기간 전체를 추출한 것은 12건, 장소 후보가 있는 것은 13건이다. 여러 장소·기간 또는 연도 미상인 경우 추측하지 않고 검수 필요로 남긴다.

## 내용을 확인하는 방법

프로젝트의 다음 파일을 브라우저로 연다.

- `data/private/instagram/20261112_1342_review/review.html`: 원문·원본 링크·행사 유형·작품·일정·장소·판별 근거·제외 게시물을 함께 보여주는 최신 검수 목록
- `data/private/instagram/20261112_1342_review/posts.json`: 최신 분류 결과와 수집 원문
- `data/private/instagram/20261112_1340/posts.json`: 첫 수집 당시 원본 및 초기 규칙 결과

원문 파일은 Git 제외된 비공개 경로에 있고 웹 공개·외부 공유하지 않았다. 별도 사이트 관리 화면이 아니라 로컬 HTML 검수 목록이다. 이미지·동영상은 다운로드하지 않았으며 원본 Instagram 링크로 확인한다. HTML은 본문 escape·외부 리소스 차단을 적용했다.

## DB 저장과 분리

전체 PostgreSQL 백업 `backups/instagram_events_20261112/database.dump` 생성 후 신규 migration `20261112_instagram_events`를 적용했다. 이전 DB revision은 `20261110_users`였다. 신규 테이블은 `event_sources`, `source_posts`, `event_candidates`, `events`, `event_source_links`이며 기존 상품 테이블 변경은 없다. Alembic target metadata에 독립 행사 metadata를 추가해 향후 자동 생성에서 신규 테이블을 누락하지 않도록 했다.

실제 DB 조회 결과: 수집원 3, 게시물 30, 후보 판정 레코드 30, 공개 행사 0, 행사 연결 0. 동일 원문 재검사는 API 추가 호출 0회, 신규 삽입 0건, 기존 게시물 30건 재사용이었다. 게시물 고유키와 후보 post_id 유니크로 중복을 막는다. 변경 원문은 후보 재검수 및 연결 행사의 변경 이력 보존 대상으로 처리한다. 관리자의 승인·공개 UI는 아직 없으며 자동 공개·자동 병합하지 않는다.

## 코드와 테스트

- `backend/app/integrations/instagram/events.py`: 요청한 4종 행사 후보, IP 근거, 명시 기간·장소와 중복 키.
- `collector.py`: 공식 호스트로만 제한한 소량 cursor 수집·허용 원문 필드 검사.
- `store.py`: 상품과 독립된 행사 테이블·트랜잭션 저장·중복 방지·변경 시 재검수.
- `review.py`: 스크립트 없는 로컬 HTML 검수 목록.
- `backend/scripts/collect_instagram_events.py`: 실제 인증 게이트를 다시 통과한 계정만 수동 수집·저장.
- `backend/scripts/recheck_instagram_events.py`: 이미 저장된 원문 재분류, 추가 API 없음.
- `backend/alembic/versions/20261112_instagram_events.py`, `backend/alembic/env.py`: 독립 신규 테이블 및 metadata 등록.
- `backend/tests/test_instagram_events.py`, `test_instagram_poc.py`: 행사·일정·장소·콜라보 카페·제외·커서·HTML·중복·롤백·변경 시 검수 및 인증 테스트.

Instagram 관련 테스트 **48 passed**. 전체 백엔드 **249 passed, 18 skipped**. 프로젝트 구조 검사 오류 0건. PostgreSQL 실제 수집 저장 및 원문 재사용 검증도 성공했다. 전용 테스트 DB가 필요한 일부 통합 테스트는 건너뛰었으므로 전 항목 인증을 주장하지 않는다. 후보 정확도에 대한 독립적인 사람 검수 gold는 아직 없다.

## 운영 상태와 제한

자동 수집 플래그와 dry-run 기본 설정은 변경하지 않았다. 명시적인 `--commit` 수동 1회만 실행했다. 사이트 API·프런트엔드는 변경하지 않았다. 기존 백엔드 health HTTP 200을 확인했다. 유료 API·AI 호출·X 수집·웹사이트 크롤러·우회 스크래핑·이미지 다운로드는 없다.

토큰은 앞선 실제 검사에서 2026-11-12 15:00 KST 만료로 확인됐다. 이후 실행은 새 인증이 필요할 수 있다. 별도 게시물 보존·삭제 동기화 정책과 관리자 승인 UI·스케줄러·다국어 날짜 및 다중 개최지 지원은 미완료다. 작품 사전에서 빠진 IP를 놓칠 수 있고, 규칙 일치가 행사 개최 확정을 뜻하지 않는다. 따라서 제외 원문도 함께 검토하며 모든 후보는 관리자 검수 전 비공개로 유지한다.

실행 명령과 설정은 [모듈 운영 안내](../../backend/app/integrations/instagram/README.md)를 참고한다.
