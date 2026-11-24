# Instagram 공식 API 가용성 POC

## 이미지 포함 검수 — 2026-11-12 추가

사용자의 이미지 수집 요청으로 공식 API가 반환한 이미지·캐러셀·영상 썸네일을 내부 검수용 파일로 저장하는 후속 CLI를 추가했다. 현재 최신 검수 목록은 `data/private/instagram/20261112_1354_images/review.html`이며 30개 게시물에 이미지 93장(43,926,652 bytes)을 연결했다. 기존 ‘이미지 다운로드 없음’ 설명은 이 기능 도입 전의 본문 수집 단계에 해당한다.

다음부터는 **본문 수집 → 이미지 보강**의 두 단계로 실행한다. 기존 본문 검수 파일만 있어도 이미지 보강 단계를 실행할 수 있다. 매번 새 output-dir를 사용하고 현재 유효한 토큰이 필요하다.

```powershell
docker compose run --rm --no-deps -v "${PWD}/backend:/tmp/odock_instagram:ro" -v "${PWD}/.env:/run/odock-instagram.env:ro" -v "${PWD}/data/private/instagram:/private-instagram" -w /tmp/odock_instagram backend python -m scripts.collect_instagram_images --env-file /run/odock-instagram.env --input /private-instagram/20261112_1342_review/posts.json --output-dir /private-instagram/images_next
```

게시물 ID가 기존 원문과 일치한 경우에만 연결한다. 이미지 요청은 계정별 최근 10건·첫 페이지이며 캐러셀 자식은 최대 20개다. 첫 페이지에서 밀려난 기존 게시물은 `NOT_IN_CURRENT_API_RESPONSE`, API 이미지 URL이 없으면 `API_IMAGE_NOT_PROVIDED`로 남긴다. 필드 지원·권한 오류를 스크래핑이나 다른 미디어 API로 우회하지 않는다. 동영상 본체는 다운로드하지 않고 API가 주는 thumbnail만 수집한다.

`media/`의 SHA256 파일명으로 사본을 보관하고 `posts.json`에는 출처 게시물·계정·이미지 ID·역할·다운로드 시각·파일 hash·크기·상태를 연결한다. CDN 서명 URL·토큰을 보고서에 출력하지 않는다. 이미지 metadata는 현재 비공개 JSON에 저장하며 PostgreSQL 행사 테이블을 변경하지 않는다. 이미지 단계가 기존 행사 후보·승인 정보를 변경하지 않는다.

Meta CDN의 HTTPS URL만 허용하고 사설/루프백 주소·인증 정보 포함 URL·Graph 토큰 쿼리·리디렉션을 차단한다. CDN 요청에는 API bearer를 보내지 않는다. JPEG/PNG/WebP 서명·Content-Type을 확인하며 SVG/HTML/영상은 거절한다. 개별 10MiB·1회 총 150MiB 제한이다. 검수 HTML은 hash 기반 로컬 상대경로만 이미지로 사용하며 외부 CDN을 직접 로드하지 않는다. 원본 파일을 변형하지 않았고 실제 파일 1장을 열어 확인했다. 렌더된 브라우저 화면 자체를 자동 검증한 것은 아니다.

파일은 내부 검수 목적으로만 저장했다. 공식 API의 반환이 별도 사이트 공개·재배포 권한을 뜻한다고 간주하지 않는다. 공개 허가·보존·삭제 동기화는 별도 확인 대상이며 자동 게시·스케줄러는 계속 비활성이다. 관련 이미지·행사·인증 테스트 63건을 통과했다.

기존 FastAPI 프로젝트 안의 독립 CLI 모듈이다. 앱 라우터, 상품 테이블, 번역·분류·RAG, Docker 서비스와 큐는 변경하지 않는다. 2026-11-12 실제 API 선행 검증 성공 이후 수동 1회 수집, 행사 전용 테이블, 후보 추출과 비공개 HTML 검수 목록까지 추가했다. 자동 스케줄러·공개 행사 API·관리자 승인 UI는 아직 없다.

## 현재 상태

2026-11-12 13:32에 토큰·자체 계정·3개 공식 계정의 Business Discovery가 모두 HTTP 200으로 성공했다. 13:40 수동 수집에서 30개 게시물을 저장했고, 규칙 보완 후 검수 대기 18건·행사 아님 10건·비관련 2건으로 분류됐다. 후보 18건은 게시물 단위이며 중복 공지를 포함한다. 독립적인 사람 정확도 검수나 전체 POC 성공 인증을 의미하지 않는다. 토큰 만료는 2026-11-12 15:00 KST로 확인됐으므로 지속 운영에는 재인증·토큰 수명 대응이 필요하다.

팝업·팝업스토어·전시회·콜라보 카페를 탐지한다. 공식 원문, 게시물 ID·UTC 시각·본문·허용된 유형만 보관하며 이미지는 다운로드하지 않는다. 날짜는 명시된 연도를 기준으로 하고, 종료 연도를 시작 연도에서 이어받으면 근거를 기록한다. 연도가 전혀 없거나 여러 장소·기간이 섞이면 미확인으로 남긴다. 일반 패션·식음료 판촉은 서브컬처 근거가 없으면 제외한다. 작품 사전에 없는 IP를 누락할 수 있으므로 제외된 원문도 검수 파일에 함께 제공한다.

### 수동 수집과 검수 목록

신규 마이그레이션 `20261112_instagram_events`는 행사 전용 5개 테이블만 추가한다. 기존 상품 레코드나 번역 큐는 수정하지 않는다. 현재 DB에는 적용 완료했다. 게시물의 `(platform, external_id)`로 중복을 막고, 원문 변경 시 후보를 재검수 상태로 갱신한다. 행사 중복 키는 작품·명시 기간·장소가 모두 있는 경우에만 제안하며 자동 병합하지 않는다. 공개 `events` 테이블은 비어 있고 관리자 승인·공개 흐름은 후속 구현 대상이다.

```powershell
# 새 환경에서만, 백업 후 행사 전용 migration 적용
docker compose run --rm --no-deps -v "${PWD}/backend:/tmp/odock_instagram:ro" -w /tmp/odock_instagram backend alembic upgrade 20261112_instagram_events

# 현재 유효한 토큰으로 한 번 수집. report-dir는 매번 새 경로 사용.
docker compose run --rm --no-deps -v "${PWD}/backend:/tmp/odock_instagram:ro" -v "${PWD}/.env:/run/odock-instagram.env:ro" -v "${PWD}/data/private/instagram:/private-instagram" -w /tmp/odock_instagram backend python -m scripts.collect_instagram_events --env-file /run/odock-instagram.env --commit --report-dir /private-instagram/manual_next
```

`--commit`을 생략하면 비공개 파일 미리보기만 작성한다. 수집 전 매번 토큰·Discovery를 재확인하며, `--commit`은 이번 1회의 DB 저장만 허용한다. `INSTAGRAM_COLLECTION_ENABLED=false`와 `INSTAGRAM_DRY_RUN=true`는 유지하고 자동 작업은 시작하지 않는다. DB 저장은 계정 단위 트랜잭션이며 실패한 계정은 롤백한다. `posts.json`을 저장한 후 DB를 쓰므로 중단 시 보존된 원본에서 재검사가 가능하다. 커서는 원본 paging URL을 따라가지 않고 허용된 공식 호스트에서 재구성한다. 기본 계정별 10건·1페이지이며 설정 상한은 10건·3페이지다.

기존 원문을 새 API 호출 없이 재분류:

```powershell
docker compose run --rm --no-deps -v "${PWD}/backend:/tmp/odock_instagram:ro" -v "${PWD}/data/private/instagram:/private-instagram" -w /tmp/odock_instagram backend python -m scripts.recheck_instagram_events --input /private-instagram/20261112_1340/posts.json --output-dir /private-instagram/recheck_next --commit
```

각 폴더의 `review.html`을 브라우저에서 열면 원문·출처·카테고리·작품·기간·장소·근거를 확인할 수 있다. 현재 최신 파일은 `data/private/instagram/20261112_1342_review/review.html`이다. HTML은 스크립트·외부 이미지 없이 본문을 escape하고 원문 링크만 제공한다. 실제 게시물 본문은 Git 제외된 `data/private/`에만 저장한다. 임의 외부 공유나 웹 공개용 디렉터리 복사를 하지 않는다. 자동 보존 만료·삭제 동기화는 아직 없어 운영 전 보존 정책 확정이 필요하다.

아래는 가용성 CLI 설명과 초기 단계 기록이다. ‘아직 구현하지 않음’으로 쓰인 후속 항목 중 위에서 명시한 수동 수집·저장·추출만 이번에 구현됐고, 스케줄러·승인 UI·공개는 계속 비활성이다.

## 설정

사용자 요청으로 `.env.example`은 삭제됐다. **기존 로컬 `.env`의 `META_*`, `INSTAGRAM_*` 항목**을 설정한다. 기존 DB·번역 설정을 덮어쓰지 않는다. 실제 `.env`는 `.gitignore`로 제외되어 있다. 비밀 값을 채팅, CLI 인자, 화면 캡처, Git에 넣지 않는다.

필수: `META_APP_ID`, `META_APP_SECRET`, `META_ACCESS_TOKEN`, `META_IG_USER_ID`, `META_GRAPH_API_VERSION`.

`META_IG_LOGIN_CONFIG_ID`는 로그인 구성 ID이며 토큰이 아니다. ID와 API 버전은 실제 Meta 화면/응답에서 확인한 값을 사용한다. 예제 버전을 운영 지원 버전으로 간주하지 않는다. `META_GRAPH_BASE_URL` 기본값은 `https://graph.facebook.com`이다. 현재 POC는 문서화된 Facebook Graph의 `debug_token`과 Business Discovery 경로만 구현한다. `graph.instagram.com` 등 다른 경로를 설정하면 `LOGIN_HOST_ROUTE_UNVERIFIED`로 멈춘다. Unified Login이 이 경로·토큰과 호환된다고 가정하지 않는다.

사용자는 Meta 콘솔의 실제 Unified Login/자산 권한 부여 절차를 완료하고, 프로페셔널 계정 ID·토큰 유형·부여 권한·만료·앱 검수 상태를 확인해야 한다. 리디렉션 URL은 실제 서버 주소로 등록한다. 이번 POC에 OAuth callback·토큰 교환·프런트엔드 로그인·권한 확장 기능은 없다. 확인되지 않은 scope를 임의 요청하지 않으며 다른 로그인 경로로 자동 전환하지 않는다.

기본값 `INSTAGRAM_COLLECTION_ENABLED=false`, `INSTAGRAM_DRY_RUN=true`는 유지한다. 가용성 CLI의 `--live`는 **소수 읽기 요청만** 허용하는 별도 명령이다. 두 플래그를 바꾸더라도 수집 작업은 존재하지 않아 자동으로 시작되지 않는다. 주기 12시간·page/media limit 설정은 향후 수집기용이며 현재 스케줄러는 없다.

## 실행 (프로젝트 루트 PowerShell)

기존 백엔드 이미지를 사용해 코드만 읽기 전용으로 마운트한다. 백엔드 재시작·DB migration·번역 재실행이 필요 없다. Docker 실행이 필요하다.

```powershell
New-Item -ItemType Directory -Force docs/evidence/instagram_20261112

# 자격 증명 존재·호스트·버전 형식만 확인. 네트워크 요청 없음.
docker compose run --rm --no-deps -v "${PWD}/backend:/tmp/odock_instagram:ro" -v "${PWD}/.env:/run/odock-instagram.env:ro" -v "${PWD}/docs/evidence/instagram_20261112:/evidence" -w /tmp/odock_instagram backend python -m scripts.instagram_poc --env-file /run/odock-instagram.env --report /evidence/preflight_01.json

# 실제 토큰을 로컬 파일에 설정한 뒤 명시적으로 읽기 전용 조회.
docker compose run --rm --no-deps -v "${PWD}/backend:/tmp/odock_instagram:ro" -v "${PWD}/.env:/run/odock-instagram.env:ro" -v "${PWD}/docs/evidence/instagram_20261112:/evidence" -w /tmp/odock_instagram backend python -m scripts.instagram_poc --env-file /run/odock-instagram.env --live --report /evidence/live_01.json
```

보고서는 덮어쓰지 않으므로 실행마다 새 파일명을 사용한다. CLI 종료 코드 0은 `GO_NEXT_PHASE_ONLY`, 2는 미검증/NO-GO다. Compose가 2를 오류로 표시해도 출력 JSON의 `reason`으로 원인을 구분한다. 현재 실제 실행 JSON은 [availability_20261112.json](../../../../docs/evidence/instagram_20261112/availability_20261112.json)에 있다.

## 검증 순서와 기록

1. 필수 설정·숫자 ID·API 버전 형식·공식 호스트 확인. 누락 시 요청 0건.
2. `debug_token`으로 `is_valid`, 토큰 유형(USER/PAGE/SYSTEM_USER), 앱 일치, scopes, 토큰·데이터 접근 만료 확인. 이 타입은 호환성의 보증이 아니며 후속 실제 조회가 필요하다. 만료 필드 0은 정해진 만료 시각이 없다는 의미로 취급하며 영구 접근을 보증하지 않는다.
3. 자기 계정 `id,username` 읽기 성공 확인. 계정 ID 일치 전에는 타사를 조회하지 않는다.
4. `duex.official`, `anique.jp`, `akplaza_hongdae` 순서로 대상별 한 번의 Discovery 조회. 계정별 HTTP 상태·오류 코드·필드명·게시물 수만 보고한다. permission/token/rate limit 오류는 남은 대상 조회를 중단한다.
5. 한 계정 이상에서 게시물이 반환돼도 `GO_NEXT_PHASE_ONLY`다. 저장·분류·검수 기능까지 검증하기 전에는 `POC_SUCCESS`가 아니다.

`api_requests`는 실제 HTTP 시도 횟수(재시도 포함)다. 정상 시 최대 5회이며 429/5xx/네트워크 오류는 호출당 최대 3회, 1·2초 기본 backoff다. Retry-After가 30초를 넘으면 `RETRY_LATER`로 종료한다. 401/403/영구 권한 오류는 재시도하지 않는다. 응답 최대 2MB, timeout 20초, 리디렉션 및 환경 프록시 사용 금지.

보고서에는 토큰·app secret·원문 오류 메시지·응답 본문·커서·페이징 URL을 넣지 않는다. `debug_token`의 input_token은 Meta 공식 API의 쿼리로만 전달되므로, 실행 시 HTTP 클라이언트 URL 로그를 비활성화한다. 요청 URL을 수집하는 외부 디버거·패킷 로그를 켜지 않는다. 게시물 caption은 가용성 검증 메모리에서만 처리하며 파일·DB·공개 API에 저장하지 않는다. 이미지·동영상 다운로드 및 followers/comments 조회는 없다. 커서 페이지네이션·중복 저장·행사 분류 테스트는 해당 기능이 아직 없으므로 구현·통과했다고 주장하지 않는다.

## 실패 대응

| reason | 조치 |
|---|---|
| CONFIGURATION_INCOMPLETE_NO_REQUEST_SENT | 누락 항목을 로컬 `.env`에 설정; config_id로 토큰 대체 금지 |
| TOKEN_INVALID_OR_WRONG_APP / TOKEN_EXPIRED | Meta에서 앱·토큰 유형·권한·만료를 확인하고 정식 인증 재수행 |
| TOKEN_TYPE/PERMISSIONS/EXPIRY_UNVERIFIED | Meta 토큰 디버거로 확인. 임의 성공 처리 금지 |
| PERMISSION_DENIED | 현재 로그인 구성에서 제공되는 권한과 App Review/Advanced Access 요구 확인 |
| DISCOVERY_FIELD_OR_OBJECT_UNAVAILABLE | 현재 API 호스트·버전·로그인 경로·계정 적격성 확인; 지원 불명으로 유지 |
| LOGIN_HOST_ROUTE_UNVERIFIED | 실제 Meta가 안내하는 호스트·토큰 절차 확인 후 별도 검토 |
| NETWORK_OR_TIMEOUT / RATE_LIMITED / RETRY_LATER | 네트워크/한도 회복 후 새 보고서로 제한 재실행 |

지원 불가 시 각 계정은 `MANUAL_LINK_ONLY`로 남기고 관리자에게 공식 원문 링크를 수동 전달하는 운영안을 사용한다. 우회 스크래핑·사설 API·자동 로그인은 사용하지 않는다. 현재 이 상태는 POC 보고서상의 제안 상태이며 DB 레코드를 새로 만든 것은 아니다.

## 후속 단계의 선행 조건

실제 조회 성공 응답을 확보한 뒤에만 분리 테이블/비파괴 migration, 허용 원본 최소 저장, IP·행사 관련성·일정·장소 추출, 중복 upsert, 변경 이력·관리자 검수 기능을 구현한다. 실제 게시물로 분류를 검증하고 성공한 계정만 허용한 뒤에 수동 단일 수집 → 별도 스케줄러 순서로 진행한다. 게시물 보존·삭제 정책과 매체 재사용 권한도 그때 확인한다.

## 공식 참고 자료

- [Meta Instagram API 공식 Postman 컬렉션](https://www.postman.com/meta/instagram/collection/6yqw8pt/instagram-api)
- [Business Discovery](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/business-discovery)
- [Meta 토큰 디버거](https://developers.facebook.com/tools/debug/accesstoken/)
- [Meta 공식 토큰 진단 가이드](https://github.com/meta/agentic-tools/blob/main/plugins/devtools/skills/debug-access-token/SKILL.md)

2026-11-12 웹 조회에서 Meta Developers 문서는 429, Postman 본문은 제한적으로만 노출됐다. 따라서 최신 Unified Login 지원·필수 scope·지원 버전을 확인했다고 주장하지 않는다. 실제 사용자 콘솔과 API 응답으로 최종 판정해야 한다.
