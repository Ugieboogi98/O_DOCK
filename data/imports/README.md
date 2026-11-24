# 제조사별 원본 수집 묶음

외부에서 받은 입력 스냅샷을 제조사/수집일 기준으로 보관합니다. 애플리케이션 실행 코드는 `backend/`, 실행 진입점은 `scripts/`입니다.

| 제조사/제품군 | 현재 입력 묶음 |
|---|---|
| FuRyu | `furyu/20261110/` |
| SEGA / S-FIRE | `sega/s_fire/20261028/` |
| TAITO | `taito/20261028/` |

메가하우스·반다이 등의 온라인 수집 결과는 PostgreSQL과 Docker 이미지 저장소에 저장됩니다. 별도의 외부 묶음을 받았을 때만 이 디렉터리에 실제 입력을 추가합니다. 데이터가 없는 제조사의 빈 폴더를 만들지는 않습니다.

묶음 내부의 Python·Shell·README·체크섬은 수집 당시의 원본 자료로 보존합니다. 현재 실행 경로로 사용하지 않습니다. **현재 가져오기는 프로젝트 루트의 단일 진입점을 사용하세요.**

```powershell
python scripts/import_bundle.py furyu validate
python scripts/import_bundle.py s_fire validate
python scripts/import_bundle.py taito validate
```

기본 동작도 validate입니다. DB 조회 미리보기는 `preview`, 실제 저장은 명시적으로 `commit`을 선택합니다. `commit-missing`은 후류에만 지원합니다. commit 전에 현재 DB 백업과 덤프 검증을 수행하며, 로그·백업·보고서는 `backups/imports/<묶음>/`에 저장됩니다.

이 입력 디렉터리는 Docker `/data/imports`로 읽기 전용 공유됩니다. 새 이미지를 처음 사용할 때는 먼저 backend를 빌드해야 합니다. 검증은 상품 원문·이미지 해시를 읽으며 모델 호출이나 웹 재수집을 하지 않습니다.

현재 묶음 위치와 실행 모듈은 `registry.json` 한 곳에서 등록합니다. 공통 실행기와 backend 가져오기 모듈이 이 파일을 함께 읽으므로 날짜별 경로를 여러 코드 파일에 중복 정의하지 않습니다.

commit 시 원문 저장과 의미 검증 대기 작업을 같은 DB 트랜잭션에 기록합니다. 보고서의 `semantic_pending`은 검증 대기 상품 수(기존 대기 작업 재사용 포함), `semantic_cached`는 유효한 저장 결과를 재사용한 상품 수입니다. 자동 모델 호출은 하지 않으며, 한국어 파생 정보는 기존 preview → 검토 → apply 절차로 게시합니다. 원본 메타데이터와 기존 저장명은 보존합니다.
