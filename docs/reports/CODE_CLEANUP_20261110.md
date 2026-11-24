> 이 문서는 작업 당시의 이력입니다. 이후 변경된 경로는 [현재 프로젝트 구조](../PROJECT_STRUCTURE.md)를 확인하세요.

# 불필요한 파일 삭제와 코드 책임 정리 — 2026-11-10

## 실제 삭제

18개 경로에서 **59개 파일, 360,268바이트**를 삭제했다. 삭제 전 소스 ZIP의 내용과 각 파일의 SHA-256이 일치하는지 검증했다.

- 구버전 덮어쓰기 패치 폴더: `figure_archive_auto_refresh_patch`, `O_DOCK_JA_KO_PATCH`, `O_DOCK_JA_KO_PATCH_V2`, `O_DOCK_JA_KO_PATCH_V3`.
- 이미 적용된 구형 설치기 `install_korean_rag.py`.
- 더 이상 현재 실행 방식을 설명하지 않는 `START_HERE.md`, `REFACTOR_GUIDE.md`와 이미 무효인 `MANIFEST.sha256`. 현재 안내는 새 README로 통합했다.
- backend/frontend 실행 소스 안의 `.bak` 사본 5개.
- 실제 라우터가 사용하지 않는 이전 `LoginView.vue`.
- 책임 이동을 완료한 기존 서비스 파일 4개: personal.py, korea.py, ko_api.py, catalog_refresh_api.py. 호환용 빈 래퍼를 남기지 않고 사용처를 새 경로로 수정했다.

DB, Docker 볼륨, `.env`, 이미지, 제조사 수집 원본, 기존 복구 백업, 사용 중인 CLI, 독립 이미지 중복 복구 도구는 삭제하지 않았다. node_modules도 개발·빌드에 사용하므로 유지했다.

## 백엔드 구조

HTTP 라우터를 전부 `backend/app/api/`로 모았다. 현재 `services/`에는 APIRouter 선언과 라우트 데코레이터가 없다.

| 새 위치 | 책임 |
|---|---|
| api/accounts.py | 회원가입·로그인·로그아웃·현재 사용자 HTTP 처리 |
| services/accounts.py | 비밀번호 해시, 세션, 사용자 소유권 인증 |
| api/personal.py | 사용자별 관심상품·구매 CRUD HTTP 처리 |
| services/personal_records.py | 구매 입력 검증과 저장 |
| api/pricing.py | 환율과 저장된 지역 가격 조회·갱신 HTTP 처리 |
| services/exchange_rates.py | 환율 가져오기·검증·캐시 |
| api/product_text.py | 관리자 상품명 수정·번역과 원문 설명 조회 |
| api/korea_prices.py | 한국 공식 가격 미리보기·저장·삭제 |
| api/korean.py | 한국어 검색과 저장된 번역 조회 |
| api/catalog_refresh.py | 수집 상태·관리자 갱신 진입점 |

Origin 검사가 personal/account 경로에 중복되어 있던 부분은 `core/security.py`의 `require_same_origin`으로 통합했다. 기존 관리자 인증 및 개인 소유권 검사는 유지했다.

## 프런트엔드 구조와 수정

한 archive 저장소에 있던 책임을 분리했다.

- `stores/archive.js`: 카탈로그 상태·비교·관리자 연결을 조합한다. 기존 화면이 사용하는 인터페이스는 유지한다.
- `stores/favorites.js`: 사용자별 찜 상태와 비동기 요청·계정 전환 보호를 담당한다.
- `stores/chats.js`: 계정별 브라우저 대화 저장을 담당한다. AIChatView의 import를 새 경로로 수정했다.

찜 조회가 진행되는 동안 찜을 변경하면 오래된 조회 결과를 무시하되, 끝난 요청 자체는 반드시 해제하도록 고쳤다. 이전 구현은 변경 때문에 revision이 달라지면 완료된 Promise가 계속 남아 다음 갱신을 막을 수 있었다. 새 회귀 테스트로 조회→변경→이전 조회 종료→새 조회까지 검증했다.

## 검증과 운영 반영

- 기존 실행 이미지에서 40개 HTTP 경로의 메서드·입력 파라미터·본문 스키마·응답 명세를 캡처했다. 수정 후 소스와 최종 실행 이미지에서 모두 일치를 확인했다.
- 백엔드 전체 테스트: **159개 통과, 건너뜀 0개**.
- SQL 테스트는 새 전용 PostgreSQL DB `odock_cleanup_test_20261110_1640`에서 수행했다. 벡터 저장소는 임시 로컬 Chroma, 임베딩은 hash로 격리했다. 모델·검색·임베딩 API 키를 비운 테스트 프로세스를 사용했다. 운영 DB와 운영 Chroma를 테스트 저장소로 사용하지 않았다.
- 프런트엔드 **32개 통과**, production build 성공.
- backend/frontend만 `up -d --build --no-deps`로 반영했다. init, seed, worker, 수집, DB 마이그레이션을 실행하지 않았다.
- 운영 Nginx 경유 검사: 비관리자 공용 수정 403, 관리자 인증 확인 200, 공개 상세·수집 상태·health 200.
- 상품 6,158개와 duplicate_hidden 1,555건 유지 확인. 이번 정리는 운영 개인 기록·원문·출처·가격을 변경하는 작업이 아니다.
- 브라우저 육안 검증은 수행하지 않았다. Vue 빌드·저장소 회귀 테스트·실제 HTTP 검사를 수행했다.

## 복구 자료

- 삭제 전 소스: `backups/cleanup_20261110/source_before.zip` (약 380KB, `.env` 미포함).
- 삭제 파일별 경로·크기·해시: `backups/cleanup_20261110/deletions.json`.
- 수정 전 API 계약: `backups/cleanup_20261110/http_contract_before.json`.
- 기존 DB/이미지 복구 자료는 원래 위치에 유지했다. 이번 변경에는 DB 스키마 변경이 없어 소스 복구에 DB 복원이 필요하지 않다.
- 소스 복구 시에는 ZIP을 임시 위치에 풀어 필요한 파일을 원래 위치로 복원하고, 이번에 새로 분리한 API/서비스/저장소 파일을 함께 검토한 후 이미지를 다시 빌드한다. 구버전 patch installer를 재실행하지 않는다.
- `.gitignore`에 백업·덤프·구형 사본을, backend Docker ignore에 캐시·구형 사본을 추가했다. Git 저장소가 아니므로 커밋은 하지 않았다.

## 남은 구조 개선

제조사별 importer의 공통 저장·검증 경로 통합, product_semantics의 제공자 호출과 근거 규칙 분리, 큰 Vue 화면의 컴포넌트 분리, 검색 SQL 실행 계획 분석은 다음 독립 작업으로 남긴다. 실제 사용 중인 수집·복구 도구는 단순히 오래됐다는 이유로 삭제하지 않았다.
