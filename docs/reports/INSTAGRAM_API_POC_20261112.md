# Instagram 공식 API 가용성 POC 구현 결과

## 후속 수집 단계 진행 안내

13:32 공식 조회 성공 후 사용자 요청에 따라 팝업·전시·콜라보 카페 원문 수집과 비공개 후보 저장을 진행했다. 현재 결과는 [행사 수집 실행 보고서](INSTAGRAM_EVENT_COLLECTION_20261112.md)를 참고한다. 아래의 ‘저장 미구현’ 문구는 각 검사 당시의 이력이며 최신 저장 상태가 아니다.

## 13:32 KST 재검사 — 3개 대상 공식 API 조회 성공

권한을 포함해 새로 발급한 USER 토큰으로 [세 번째 실제 검사](../evidence/instagram_20261112/live_user_config_03.json)를 수행했다. 토큰 검사·자체 계정 조회와 `duex.official`, `anique.jp`, `akplaza_hongdae` Business Discovery가 모두 HTTP 200으로 성공했고 계정별 최근 10건, 총 30건의 게시물 필드가 반환됐다. 요청은 총 5회이며 토큰·시크릿·게시물 본문은 보고서에 출력하지 않았다.

실제로 확인된 scopes는 `pages_show_list`, `business_management`, `instagram_basic`, `instagram_manage_insights`, `pages_read_engagement`, `public_profile`이다. 이전 SYSTEM_USER 토큰과 달리 USER 타입이며, 권한·토큰 종류가 함께 변경됐으므로 성공 원인을 특정 scope 하나에만 귀속하지 않는다. `expires_at=1794463200`이 반환돼 단기 토큰 만료 대응이 필요하다. 장기 자동 운영 가능 상태로 간주하지 않는다.

현재 판정은 **GO_NEXT_PHASE_ONLY**다. 이는 공식 API 조회 가능성 확인이며, 게시물 DB 저장·행사 분류·중복 처리·관리자 검수까지 완료된 `POC_SUCCESS`가 아니다. 이번 실행은 읽기 전용으로 DB 쓰기·자동 스케줄러·유료 외부 API 호출이 없었다. 아래는 이전 실패 진단 이력이다.

## 13:25 KST 재검사 — 본인 계정 성공, 타사 조회 권한 거절

사용자 설정 수정 후 [두 번째 실제 검사](../evidence/instagram_20261112/live_user_config_02.json)에서 토큰 debug와 자체 Instagram `id,username` 조회가 모두 HTTP 200으로 성공했다. 이전 계정 ID 문제는 해결됐다. 다만 `duex.official` Business Discovery 요청은 HTTP 400, code 10으로 거절됐다. 추가 진단 1회에서도 `Application does not have permission for this action`이 반환됐다. [비밀값 없는 진단](../evidence/instagram_20261112/live_user_config_02_diagnosis.json)을 보존했다.

현재 토큰 scopes는 `instagram_basic`, `instagram_manage_messages`, `public_profile`이며, 오류 응답은 정확한 누락 scope나 App Review 요건을 특정하지 않았다. 따라서 특정 권한 하나를 추가하면 해결된다고 단정하지 않는다. Meta 콘솔에서 실제 Unified Login 구성의 Business Discovery 지원, 관련 Permissions and Features/Advanced Access, 시스템 사용자의 자산 권한을 확인해야 한다. 구성이 지원하지 않는 경우 무단으로 다른 로그인 경로나 스크래핑으로 우회하지 않는다.

이번 검사에는 초기 3회와 추가 진단 1회, 총 4회 읽기 요청을 사용했다. 권한 거절 이후 `anique.jp`, `akplaza_hongdae` 조회를 중단했으며 게시물 수집·DB 저장·자동 수집은 수행하지 않았다. 최종 판정은 **NO-GO — 타사 Discovery 권한 미확보**다. 아래 기록은 이전 단계별 검사 이력이다.

## 11:30 KST 실제 인증 테스트 추가 결과

사용자가 자격 증명을 입력한 뒤 [실제 API 검사](../evidence/instagram_20261112/live_user_config_01.json)를 실행했다. 토큰 debug HTTP 200, `is_valid=true`, 앱 일치, SYSTEM_USER 타입이며 `instagram_basic`, `instagram_manage_messages`, `public_profile` scope가 반환됐다. 토큰·데이터 접근 만료 필드는 0이다. 토큰 유효성은 확인됐지만 수집 권한 전체가 충족됐다는 뜻은 아니다.

자체 계정 `id,username` 조회는 HTTP 400 / Meta code 12로 실패했다. 추가 읽기 2건으로 오류 설명과 `/me?fields=id`를 확인했다. **설정된 META_IG_USER_ID가 SYSTEM_USER 토큰 소유자 ID와 동일**했다. 따라서 현재 값은 검증된 Instagram 프로페셔널 계정 ID가 아니라 시스템 사용자 식별자다. 올바른 연결 Instagram Graph 계정 ID 확인이 필요하다. API 버전을 임의로 낮추거나 username 필드를 제거해서 성공으로 간주하지 않았다.

전체 진단에 공식 읽기 요청 4회(초기 2회, 추가 2회)를 수행했다. 타사 Business Discovery 요청 0회, DB 쓰기 0회, 자동 수집 비활성, 최종 NO-GO다. [비밀값·계정 ID 없는 진단 기록](../evidence/instagram_20261112/live_user_config_01_diagnosis.json)을 보존했다. 아래 내용은 자격 증명 입력 전 최초 구현 시점의 기록이다.

2026-11-12 KST. 사용자의 `O_DOCK_INSTAGRAM_API_DATA_COLLECTION_20261112.md` 실행 지시에 따라 선행 게이트를 구현했다. 현재 판정은 **NO-GO — 자격 증명 미설정, 실제 API 지원 미확인**이다. 구현 성공과 실제 서비스 연동 성공을 구분한다.

## 실제 실행 결과

[실행 원본 JSON](../evidence/instagram_20261112/availability_20261112.json)

```json
{
  "mode": "LIVE_READ_ONLY",
  "decision": "NO-GO",
  "reason": "CONFIGURATION_INCOMPLETE_NO_REQUEST_SENT",
  "api_requests": 0,
  "token_valid": "UNKNOWN",
  "self_account": {"status": "NOT_RUN"},
  "discovery_supported": "UNKNOWN",
  "poc_success": false,
  "db_written": false,
  "paid_api_called": false,
  "automatic_collection_started": false
}
```

위 JSON은 실제 로컬 명령의 발췌이며 **Meta HTTP 응답이 아니다**. Meta 토큰·앱 정보·계정 ID·API 버전이 없어 외부 요청이 발생하지 않았다. 실제 HTTP 응답을 위조하거나 Mock 응답을 실제 게시물 수집으로 보고하지 않았다.

| 판정 항목 | 현재 상태 |
|---|---|
| APP_CREATED | 사용자 진술로 생성됨, 콘솔 독립 확인 안 됨 |
| CONFIG_CREATED | 로컬 Configuration ID 없음, 구성 생성 여부 UNKNOWN |
| TOKEN_VALID | UNKNOWN |
| 자체 계정 조회 | NOT_RUN |
| DISCOVERY_SUPPORTED | UNKNOWN |
| duex.official | UNKNOWN / MANUAL_LINK_ONLY |
| anique.jp | UNKNOWN / MANUAL_LINK_ONLY |
| akplaza_hongdae | UNKNOWN / MANUAL_LINK_ONLY |
| 실제 게시물 저장·행사 분류 | 선행 게이트 미통과로 미구현 |
| 자동 운영 | NO-GO |

`MANUAL_LINK_ONLY`는 보고서 내 제안 운영 상태이며 새로운 DB 수집원 레코드를 만든 것은 아니다. 앱 생성이나 구성 ID만으로 인증·수집 성공이라고 판정하지 않는다.

## 구현 내용과 변경 파일

- `.env.example`: 값이 빈 Meta 앱·토큰·계정·버전 설정, 수집 비활성/드라이런 기본값.
- `backend/app/integrations/instagram/config.py`: 기존 앱 설정과 분리된 로컬 설정. 비밀 값은 `SecretStr`로 취급.
- `backend/app/integrations/instagram/client.py`: 공식 호스트·리소스·대상 계정 allowlist, GET 전용 HTTP, 토큰 debug·자체 조회·Discovery, 제한된 backoff, 응답 크기·timeout·리디렉션 제한, 안전 오류 코드.
- `backend/app/integrations/instagram/probe.py`: 인증·자체 계정·타사 계정 순차 게이트, 계정별 결과, 최소 필드·숫자 HTTP 상태 기록. 실제 게시물 반환도 다음 단계 진행 자격에 불과하며 POC_SUCCESS로 승격하지 않음.
- `backend/scripts/instagram_poc.py`: 기본 무통신 preflight, 명시적 `--live`, 기존 보고서 덮어쓰기 방지, 오류·로그 비밀값 차단.
- `backend/tests/test_instagram_poc.py`: 네트워크 없는 Mock 단위 테스트 28건.
- `backend/app/integrations/instagram/README.md`: 환경 설정·PowerShell 실행 명령·오류 대응·선행 게이트·후속 작업 설명.
- `README.md`, `docs/PROJECT_STRUCTURE.md`: 독립 POC 위치 안내.
- `docs/evidence/instagram_20261112/availability_20261112.json`: 실제 설정 검사 실행 결과.

기존 `app/core/config.py`, 앱 라우터, 모델·migration, 상품 수집·번역·분류·RAG 코드, Docker Compose와 운영 컨테이너 설정은 이 작업에서 변경하지 않았다. 실제 `.env` 값도 변경하지 않았다. POC 실행은 `docker compose run --rm --no-deps`의 별도 단발 컨테이너로 수행했으며 기존 백엔드를 재배포하지 않았다.

## 테스트와 실행 확인

- 전체 백엔드 회귀: **223 passed, 18 skipped**. PostgreSQL 전용 테스트 DB가 필요한 항목 등은 건너뛰었으므로 전체 DB 통합 검증 완료로 주장하지 않는다.
- 이후 추가한 토큰 철회·응답 형식 테스트를 포함한 최종 Instagram 전용: **28 passed**.
- 프로젝트 구조 검사: Python source 134개, frontend source 38개, 오류 0건.
- 테스트는 실제 Meta API를 호출하지 않았다. HTTP 401/403/429/5xx, 토큰 만료·앱 불일치·불명 권한·비정상 응답·일시 실패 backoff·리디렉션·비밀값 비노출·제어 흐름을 Mock으로 확인했다.
- 외부 조회 성공 이후에만 구현할 DB upsert·커서 수집·행사 필터·날짜 추출·관리자 검수 기능은 아직 없으므로 해당 DoD는 통과하지 않았다.
- 기존 번역 작업과 backend health는 별도 읽기 전용으로 확인했다. 번역 작업을 재시작하거나 변경하지 않았다.

## 사용자 설정 이후 재실행

기존 로컬 `.env`에 다음 값을 추가해야 한다. 토큰·secret은 채팅으로 보내지 않는다.

```dotenv
META_APP_ID=
META_APP_SECRET=
META_IG_LOGIN_CONFIG_ID=
META_ACCESS_TOKEN=
META_IG_USER_ID=
META_GRAPH_API_VERSION=
META_GRAPH_BASE_URL=https://graph.facebook.com
INSTAGRAM_COLLECTION_ENABLED=false
INSTAGRAM_DRY_RUN=true
```

API 버전은 Meta 앱에서 현재 지원되는 명시 버전을 사용한다. Configuration ID는 선택적 로그인 구성 정보이며 토큰을 대체하지 않는다. 앱 secret은 서버 파일에만 보관한다. OAuth/자산 권한 부여는 사용자의 실제 Meta 콘솔 Unified Login 절차로 수행해야 한다. 계정이 프로페셔널·비즈니스 자산에 연결됐는지, 요구 scope가 실제 구성 화면에서 제공되는지, Advanced Access/App Review가 필요한지 아직 확인하지 못했다.

프로젝트 루트 PowerShell에서 아래 명령을 실행한다. 새 보고서 파일명을 사용한다.

```powershell
docker compose run --rm --no-deps -v "${PWD}/backend:/tmp/odock_instagram:ro" -v "${PWD}/.env:/run/odock-instagram.env:ro" -v "${PWD}/docs/evidence/instagram_20261112:/evidence" -w /tmp/odock_instagram backend python -m scripts.instagram_poc --env-file /run/odock-instagram.env --live --report /evidence/live_01.json
```

자세한 설정·Mock 테스트 실행·오류 대응은 [모듈 운영 안내](../../backend/app/integrations/instagram/README.md)에 있다. `GO_NEXT_PHASE_ONLY`와 실제 1건 이상의 타사 게시물 확인 후에만 원본 최소 저장·후보 추출·중복 제거·관리자 검수 테이블의 구현을 진행한다.

## 한계와 대체 운영

현재 구현은 Facebook Graph의 문서화된 Business Discovery 경로를 검증하기 위한 것으로, 신규 Unified Login 또는 Instagram Login이 동일한 경로를 지원한다고 단정하지 않는다. `graph.instagram.com`을 지정하면 지원 불명으로 중단한다. 최신 scope나 API 버전을 임의 선택·요청하지 않는다. 사용자의 실제 콘솔 및 토큰 응답을 보고 필요한 경로를 확정해야 한다.

현재는 가용성 확인만 하므로 게시물 본문·이미지·영상·개인정보를 파일·DB에 수집하지 않는다. 이미지 다운로드·비공개 계정 접근·댓글·팔로워 수집·우회 스크래핑·X API·별도 웹사이트 크롤러·유료 AI 호출은 없다. 지원 불가 시 공식 Instagram 계정 링크를 관리자 수동 자료로 활용하고 행사 공개는 출처와 범위를 확인해 수동 검수하는 대안을 제안한다.

## 공식 문서 조사

- [Meta 공식 Instagram API Postman 컬렉션](https://www.postman.com/meta/instagram/collection/6yqw8pt/instagram-api)
- [Meta Business Discovery 문서](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/business-discovery)
- [Meta 공식 토큰 진단 가이드](https://github.com/meta/agentic-tools/blob/main/plugins/devtools/skills/debug-access-token/SKILL.md)
- [Meta Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)

2026-11-12 조회에서 Meta Developers 문서가 429로 응답하고 Postman 본문은 일부만 노출됐다. 문서 조사만으로 신규 Unified Login 지원을 확인했다고 하지 않았으며, 실제 사용자 구성과 읽기 응답 확인을 미완료 상태로 남긴다.
