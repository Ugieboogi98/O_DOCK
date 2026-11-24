# 제조사 입력 및 프로젝트 디렉터리 통일 결과

작성일: 2026-11-10 (Asia/Seoul)

## 적용 원칙

제조사 폴더를 루트에 나열하지 않고, 모든 제조사에 역할별 위치를 적용했다.

- 애플리케이션·제조사별 실행 코드: `backend/`.
- 외부에서 받은 원본 묶음: `data/imports/<제조사>/<수집일>/`.
- 공통 운영 명령: `scripts/`.
- 독립 운영 도구: `tools/`.
- 보고서·검증 자료: `docs/reports/`, `docs/evidence/`.
- 소스·DB·이전 패치·가져오기 백업: `backups/`.

현재 경로의 기준은 [프로젝트 구조](../PROJECT_STRUCTURE.md)다.

## 제조사 입력 경로

| 제조사/제품군 | 현재 위치 |
|---|---|
| FuRyu | `data/imports/furyu/20261110/` |
| SEGA / S-FIRE | `data/imports/sega/s_fire/20261028/` |
| TAITO | `data/imports/taito/20261028/` |

세 폴더는 외부 수집 패키지였고 메가하우스·반다이는 공통 수집 경로로 DB와 Docker media에 직접 저장되어 왔다. 입력 방식이 다른 것을 제조사별 디렉터리 규칙의 차이로 남겨두지 않도록 정리했다. 실제 외부 묶음이 없는 제조사의 빈 폴더를 만들지는 않았다.

원본 묶음의 당시 코드·문서·체크섬은 출처 보존용으로 유지한다. 실행할 importer는 backend/scripts에 따로 관리한다. data/imports 안의 원본 패키지에 있던 오래된 설치·실행 명령은 현재 운영 진입점이 아니다.

## 함께 고친 구조

1. `backend/scripts/import_furyu_bundle.py`, `import_sfire_bundle.py`, `import_taito_bundle.py`를 같은 패키지에 배치했다.
2. `scripts/import_bundle.py`로 세 묶음의 validate / preview / commit 실행을 통일했다. 기본은 validate다.
3. `data/imports/registry.json` 한 곳에서 제조사·묶음 경로·실행 모듈을 등록한다. host와 backend가 함께 읽는다.
4. 모든 입력은 기존 `/data` 읽기 전용 마운트를 사용하고, 로그·보고서·DB 백업은 `backups/imports/<묶음>/`에 출력한다.
5. S-FIRE importer의 commit 보고서가 원본 입력 폴더에 기록되던 경로를 분리했다. 이번 작업에서 commit을 실행한 것은 아니다.
6. `O_DOCK_IMAGE_DEDUP`을 `tools/image_dedup`으로 옮기고 실행 루트·컨테이너 도구 위치·백업 출력·테스트 import 경로를 수정했다. requirements.txt에 Pillow 의존성을 명시했다.
7. `migration_backup`을 `backups/migrations`, `korean_patch_backups`를 `backups/legacy/korean_patch`로 통합했다.
8. 후류 입력 표본은 `data/samples`, 날짜별 보고서는 `docs/reports`, JSON/XML 증거는 `docs/evidence`로 옮겼다.
9. 기본 data/media/.env 위치를 현재 작업 디렉터리 대신 소스 기준으로 계산하도록 수정했다. Docker DATA_DIR/MEDIA_DIR는 그대로 우선한다.
10. Windows start는 update에 위임하고 POSIX start도 같은 서비스 순서를 사용하도록 맞췄다. 일반 시작은 seed나 catalog-worker를 자동 실행하지 않는다.
11. README와 문서 링크, 도구 체크섬, Git 제외 경로를 갱신했다. 원본 입력·백업 내용과 DB 이미지 URL은 변경하지 않았다.
12. `tools/check_structure.py`를 추가해 제조사 루트 폴더 재등장, 등록된 importer 누락, 잘못된 경로와 import·문서 링크를 검사한다.

## 이동 무결성

- 23개 이동 경로에 포함된 8,973개 파일 전체를 이동 전/직후 크기와 SHA-256으로 대조해 일치를 확인했다.
- 이후 문서·도구 경로를 의도적으로 수정한 뒤에도 원본 입력·백업·표본 8,951개 파일은 그대로인지 다시 확인했다.
- 파일을 다시 수집하거나 이미지 이름을 바꾸지 않았다. 큰 원본 묶음을 복제하지 않고 동일 작업공간 내부에서 이동했다.
- 이동 명세와 원래 파일 해시: `backups/layout_20261110/moves.json`.

## 검증

| 항목 | 결과 |
|---|---|
| 백엔드 전체 테스트 | **161개 통과**, 건너뜀 없음 |
| 이미지 중복 도구 테스트 | **12개 통과** |
| 호스트 공통 가져오기 명령 테스트 | **3개 통과** |
| 구조 검사 | 오류 0건 |
| Shell / PowerShell | 구문 검사 통과 |
| API 계약 | 최종 실행 이미지의 40개 경로 동일 |
| 운영 공개 조회·관리자 인증 확인 | 200 |
| 비관리자 공용 수정 | 403 유지 |

이동 후 실제 입력 검증:

- FuRyu: 이미지 파일 6,454개 확인. 기존 누락 파일 1,158개도 그대로 보고한다. 폴더 이동으로 누락을 복구한 것은 아니다.
- S-FIRE: 상품 81개, 이미지 항목 695개 검증. DB 접근 없음.
- TAITO: 상품 157개, 고유 이미지 파일 1,389개 검증. DB 접근 없음.
- 공통 진입점으로 S-FIRE validate 실행까지 확인했다. 실행 로그는 `backups/imports/s_fire/`에 저장됐다.
- registry 기반 컨테이너 기본 경로가 세 제조사 모두 `/data/imports/` 아래로 해석되는 것을 확인했다.

전체 SQL 테스트는 별도 테스트 PostgreSQL, 벡터는 임시 Chroma를 사용했다. 도구 테스트용 Pillow는 일회용 테스트 컨테이너의 임시 경로에 설치했다. 실제 운영의 중복 감사·apply·import commit, 웹 수집, 번역, 유료 모델 호출은 실행하지 않았다.

## 운영 반영과 보존

backend를 재빌드하고 `--no-deps`로 반영했다. DB 마이그레이션·초기 seed·worker 기동은 하지 않았다. 기존 PostgreSQL/media 볼륨과 컨테이너 `/app/media`는 유지한다.

운영 확인 시 상품 6,158개, duplicate_hidden 1,555건이 유지됐고 health·상세 조회·권한 검사는 정상이다. 사용자별 찜·구매 기록의 스키마와 식별자는 이번 작업에서 수정하지 않았다.

과거 보고서는 당시 경로를 담은 이력이다. 상단에 현재 구조 문서 링크를 추가했고, 현재 명령과 자료 위치는 새 구조 문서로 확인하도록 했다. 원본 입력 내부의 역사적 경로 문자열이나 백업 파일의 내용을 일괄 치환하지 않는다.

이번 변경을 되돌릴 때는 moves.json의 source/target을 기준으로 역방향 이동하고, 수정 전 운영 스크립트와 설정을 `backups/layout_20261110/`에서 확인한 뒤 코드를 다시 빌드한다. 이미 이동한 과거 백업을 지우거나 DB를 복원할 필요는 없다. 같은 목적지가 생겼다면 덮어쓰지 않고 먼저 대조해야 한다.
