# 현재 프로젝트 구조

모든 제조사에 같은 기준을 적용한다. 실행 코드·입력 데이터·실행 중 생성되는 자료·백업을 구분하며, 제조사 이름의 폴더를 프로젝트 루트에 두지 않는다.

```text
Project_O_DOCK_V1/
├─ O_DOCK_LOCAL_SEMANTICS/  독립 로컬 모델 시험·학습·평가 프로젝트
├─ backend/                 API, 도메인 로직, 제조사 어댑터, 수집·가져오기 CLI
│  └─ app/integrations/instagram/  기존 상품 작업과 분리된 읽기 전용 공식 API 가용성 POC
├─ frontend/                Vue 화면과 상태 저장소
├─ data/                    설정, 초기 데이터, 읽기 전용 수집 입력
│  ├─ imports/
│  │  ├─ furyu/20261110/
│  │  ├─ sega/s_fire/20261028/
│  │  └─ taito/20261028/
│  └─ samples/              조사·번역 입력 표본
├─ scripts/                 프로젝트 루트에서 실행하는 공통 운영 진입점
│  ├─ import_bundle.py      제조사에 공통인 검증·미리보기·저장 실행
│  └─ tests/                호스트 운영 명령의 단위 테스트
├─ tools/
│  ├─ image_dedup/          이미지 중복 검사·숨김·복구 도구
│  └─ check_structure.py    경로·배치·import·문서 링크 검사
├─ docs/
│  ├─ reports/              날짜별 작업·인계 보고서
│  ├─ evidence/             JSON/XML 등 검증 산출물
│  └─ reference/            참고 원문
├─ backups/
│  ├─ imports/              현재 가져오기 로그·보고서·적용 전 DB 백업
│  ├─ migrations/           이전 migration_backup의 모든 자료
│  ├─ legacy/korean_patch/  이전 한국어 패치 백업
│  └─ ...                   단계별 소스·검증 복구 자료
├─ media/                   로컬 실행 시 기본 이미지 저장 위치
├─ .env                     로컬 설정·키, 소스 관리 제외
├─ docker-compose.yml
└─ README.md
```

## 제조사별로 상위 폴더가 달랐던 이유

후류·S-FIRE·타이토는 외부 수집 패키지를 받은 이력이 있어 입력 묶음이 존재했다. 메가하우스·반다이 등은 공통 수집기가 PostgreSQL과 Docker media 볼륨에 직접 저장하므로 같은 형태의 외부 입력 묶음이 없었다.

이제 외부 묶음의 유무와 관계없이 **제조사별 애플리케이션 실행 코드는 backend**, **외부 수집 묶음은 data/imports** 기준이다. 외부 묶음을 받지 않은 제조사의 빈 폴더는 만들지 않는다. S-FIRE는 SEGA의 제품군이므로 `sega/s_fire`에 배치했다.

원본 묶음에 들어 있던 당시의 Python/Shell 파일과 README는 체크섬·수집 이력을 위한 자료다. 현재 애플리케이션이 실행할 코드는 `backend/scripts/import_*_bundle.py`이며, 사용자는 공통 진입점 `scripts/import_bundle.py`를 사용한다. 원본 패키지를 실행 코드와 섞어 관리하지 않는다.

묶음별 제조사·날짜 경로·실행 모듈은 `data/imports/registry.json`에만 등록한다. 호스트 진입점과 backend 기본 입력 경로가 같은 등록 정보를 읽으며, 입력 경로가 data/imports 밖으로 벗어나면 거부한다.

## 공통 가져오기

```powershell
python scripts/import_bundle.py furyu validate
python scripts/import_bundle.py s_fire validate
python scripts/import_bundle.py taito validate
```

옵션을 생략해도 validate이며 DB에 접근하지 않는다. `preview`는 DB 조회 미리보기, `commit`은 실제 저장이다. 후류만 `commit-missing`을 추가 지원한다. 저장 단계에서는 worker 중지와 PostgreSQL 백업·덤프 검증을 먼저 수행한다. 웹 재수집과 유료 모델 호출은 이 명령에 포함되지 않는다.

```powershell
python scripts/import_bundle.py furyu preview --dry-run
```

`--dry-run`은 실행할 명령만 출력한다. 실제 실행 전 새 backend 코드를 반영해야 한다. 입력은 기존 Compose의 `/data` 읽기 전용 마운트를 사용하며, 보고서는 `backups/imports/<묶음>/`으로 분리한다. S-FIRE 가져오기 보고서도 입력 폴더에 쓰지 않도록 수정했다.

## 온라인 수집과 이미지의 위치

- 제조사별 수집 파서: `backend/app/collectors/manufacturers/`.
- 메가하우스·반다이·다른 제조사의 온라인 수집 진입점: `backend/scripts/`, 공통 저장: `backend/app/services/catalog_ingest.py` 등.
- 실행 중 생성되는 수집 체크포인트: Docker media 볼륨의 `/app/media/maker_catalogs/` 등. 호스트의 외부 수집 묶음과 다른 종류의 자료다.
- 실제 DB·사용 이미지: 기존 PostgreSQL/media Docker 볼륨. 이번 폴더 이동으로 DB의 이미지 URL이나 컨테이너 media 경로를 바꾸지 않는다.
- 루트 `media/`는 Docker media 볼륨과 동일하다고 가정하지 않는다. 로컬 Python 실행용 기본 저장 경로이며, Docker는 Compose의 MEDIA_DIR=/app/media를 사용한다.

로컬 기본 data/media/환경 변수 파일 위치는 실행 당시 작업 디렉터리가 아니라 소스 위치에서 계산한다. Docker의 명시적인 DATA_DIR/MEDIA_DIR 환경 변수는 계속 우선한다.

Windows의 start.ps1은 update.ps1로 위임하고, start.sh도 같은 실행 순서를 사용한다. 일반 시작은 DB 서비스 준비 → 빌드 → 명시적인 마이그레이션 → backend/frontend이며, 최초 seed와 catalog-worker는 자동 실행하지 않는다. 최초 설치용 초기 데이터와 상시 worker는 별도의 명시적인 운영 작업이다.

## 이전 → 현재 경로

| 이전 | 현재 |
|---|---|
| FURYU_20261110/ | data/imports/furyu/20261110/ |
| S_FIRE_20261028/ | data/imports/sega/s_fire/20261028/ |
| TAITO_GOODS_20261028/ | data/imports/taito/20261028/ |
| O_DOCK_IMAGE_DEDUP/ | tools/image_dedup/ |
| migration_backup/ | backups/migrations/ |
| korean_patch_backups/ | backups/legacy/korean_patch/ |
| furyu_sample_sources.json | data/samples/furyu_sources.json |
| WORK_REPORT_20261110.md | docs/reports/WORK_REPORT_20261110.md |
| docs의 날짜별 보고서 | docs/reports/ |
| docs의 JSON/XML 검증 자료 | docs/evidence/ |

과거 보고서는 당시의 경로와 명령을 기록한 이력으로 보존한다. 현재 실행 명령은 이 문서와 루트 README를 따른다. 원본 입력의 체크섬과 백업 내부의 과거 경로 문자열을 일괄 치환하지 않는다.

## 구조 확인

```powershell
python tools/check_structure.py
python -m unittest discover -s scripts/tests -v
```

경로 이동 명세와 파일 해시는 `backups/layout_20261110/moves.json`에 있다. 최초 이동 직후 8,973개 파일 전체의 크기·SHA-256 일치를 확인했다. 문서와 도구의 경로를 의도적으로 수정한 뒤에도 원본 입력·백업·표본 8,951개 파일은 바이트가 동일한지 다시 확인했다.
