# O_DOCK 작업 이력 요약 (2026-10-21 ~ 2026-11-26)

PC 이전 전에 지금까지의 작업 보고서를 시간 순서로 한 문서에 정리했다. 날짜별 상세는 각 링크의 원본 보고서에 있다. `data/private/`의 실행 산출물(재처리 항목 JSON, 행사 수집 원본 등)은 git에 올리지 않으며, 그 내용은 아래 요약과 각 보고서로 대신한다.

## 2026-10-21 ~ 10-22 · 초기 버전과 첫 확장

- 8개 제조사 피규어 통합 검색·가격 비교·RAG 안내 서비스로 기획([원본 설계서](../reference/original-design.md)). Vue 3 → FastAPI → PostgreSQL / ChromaDB 구조([아키텍처](../ARCHITECTURE.md)).
- 초기 스냅샷 114개 상품([데이터 출처](../DATA_SOURCES.md)). v2에서 구매·관심상품 기능과 백엔드 테스트 39개([v2 검증](../VERIFICATION_V2.md)).
- FuRyu 공식 스케일 카탈로그 수집 활성화, 사진·한국어 상품명 누락 보강 경로 정리([후속 개발](../HANDOVER.md), [사진·이름 보강](../ASSET_REPAIR.md), [수집기 수정](../COLLECTOR_FIX.md)).

## 2026-11-10 · 구조 정리와 사용자 계정

- 제조사별 입력·코드·산출물 위치를 통일([디렉터리 통일](PROJECT_LAYOUT_20261110.md)), 구버전 패치 폴더 등 59개 파일 정리([코드 정리](CODE_CLEANUP_20261110.md)).
- 관리자 경로에 ADMIN_TOKEN 적용([관리자 경계](ADMIN_BOUNDARY_20261110.md)), 회원가입·로그인과 계정별 관심상품·구매 기록([사용자 소유](USER_OWNERSHIP_20261110.md)).
- 후류·S-FIRE·타이토 가져오기와 반다이 한국몰을 공통 의미 검증 대기열에 연결([가져오기 파이프라인](IMPORT_PIPELINE_20261110.md), [의미 대기열](SEMANTIC_QUEUE_20261110.md)).
- 번역·분류 상태를 상품 단위가 아닌 필드 단위(`field_status`)로 변경([필드 단위 정책](SEMANTICS_FIELDS_REFACTOR_20261110.md)). 상품 6,158개([인수인계 진행](HANDOFF_PROGRESS_20261110.md), [작업 보고](WORK_REPORT_20261110.md)).

## 2026-11-11 · 로컬 모델 구축·학습, 전체 번역 시작

- RTX 5060 Ti 16GB + Docker Ollama에서 qwen3:8b 번역·분류 연결([로컬 번역·분류 구축](LOCAL_SEMANTICS_20261111.md)). 실제 표본 10건 시험에서 자동 게시 부적합 판정([표본 시험](LOCAL_MODEL_SAMPLE_EVALUATION_20261111.md)).
- Qwen3 8B QLoRA 2회 학습, 운영 승격 기준 미달([튜닝 보고서](LOCAL_MODEL_TUNING_20261111.md), [검수 대기열](LOCAL_MODEL_TUNING_REVIEW_QUEUE_20261111.md)). 요약: [모델 학습 기록](MODEL_TRAINING_RECORD_20261126.md).
- 전체 6,161개 번역·분류 실행: 2,638개 처리 후 중단, 이어서 전 상품 재실행 시작([전체 번역 보고서](TRANSLATION_CLASSIFICATION_20261111.md), [전 상품 로컬 실행](FULL_CATALOG_LOCAL_RUN_20261111.md)).
- 공식 사이트·위키 근거 분류를 DB에 반영(작품 4,781 / 캐릭터 3,426 / 형태 2,740개 ready), 미확정 6,356개 그룹을 검수 문서로 분리([웹 근거 분류](WEB_CLASSIFICATION_REVIEW_20261111.md), [확인 문서](../reviews/classification_20261111/README.md)). 한국어 위키백과 애니메이션 작품 587개를 사전에 추가([위키백과 사전](WIKIPEDIA_ANIME_REFERENCE_20261111.md)).

## 2026-11-12 · 번역 누락 수정, 행사 탭

- 이름 추출·검증기·재실행 캐시를 고쳐 한국어 상품명 25개, 캐릭터 97개 복구. 프로필 ready 666 → 1,057([누락 수정](LOCAL_MODEL_REPAIR_20261112.md)).
- Instagram 공식 API POC 성공 후 팝업·전시·콜라보 카페 게시물과 이미지 93장 수집([API POC](INSTAGRAM_API_POC_20261112.md), [행사 수집](INSTAGRAM_EVENT_COLLECTION_20261112.md), [행사 이미지](INSTAGRAM_EVENT_IMAGES_20261112.md)).
- 행사 탭 공개, 날짜 파싱·중복 통합·종료 처리, 공식 홈페이지 수집처 추가로 행사 6 → 25개([행사 탭](EVENTS_FRONTEND_20261112.md), [날짜 수정](EVENT_DATE_PARSING_FIX_20261112.md), [중복·종료](EVENT_DEDUP_AND_LIFECYCLE_20261112.md), [공식 수집처 확장](OFFICIAL_EVENT_SOURCES_EXPANSION_20261112.md)).

## 2026-11-16 · 번역 재개와 국내 유통 가격

- 미번역 제목 1,154건을 대상으로 번역 재개([번역 재개](TRANSLATION_RESUME_20261116.md)). Instagram 수집은 Meta 토큰 오류(code 200 / subcode 5258005)로 미실행([수집 시도](INSTAGRAM_COLLECTION_ATTEMPT_20261116.md)).
- 국내 판매처 조사부터 매니아하우스·코믹스아트·피규어팜 수집, DB 저장, 전체 상품 수집까지 진행([현재 상태](../retail_price/00_CURRENT_STATE.md) ~ [전체 수집](../retail_price/10_FULL_CATALOG_20261116.md)).

## 2026-11-17 · 사전 우선 분리 파이프라인, 디자인

- 번역(qwen3:8b)과 분류(qwen3:1.7b)를 분리하고, 사전 일치 → 모델 → 원문 근거 검증 순서로 처리하는 split-semantics 도입([분리 파이프라인](SPLIT_SEMANTICS_20261117.md)).
- 제조사·국내 유통사 수집 회차, 핫토이 신규 수집 제외([수집 회차](COLLECTION_ROUND_20261117.md)). 구현 현황 정리([구현 현황](O_DOCK_IMPLEMENTATION_SUMMARY_20261117.md)).
- 화이트·스카이블루 디자인 시스템 적용([디자인 점검](../design/unslop-audit.md), [리팩터링 결과](../design/unslop-final-report.md)).

## 2026-11-24 · git 저장소 시작, dev 개선

- GitHub `Ugieboogi98/O_DOCK` 저장소에 기준 스냅샷을 올리고 `dev` 브랜치에서 작업 시작([시스템 구조](O_DOCK_SYSTEM_ARCHITECTURE_20261124.md)).
- 번역·분류 개선(용어집 복구, 학습 별칭, 명시 관계 이름 짓기), 인증·프록시 경계 강화, 가격 이력·국내 판매 매칭 검토 화면, CI 추가([dev 개선 보고](DEV_HARDENING_20261124.md)).
- 관리자 **원클릭 데이터 갱신**(카탈로그 수집 → 번역·분류 → 행사 수집 → 검증)과 `scripts/collect_all.ps1` 추가.
- 국내 판매 목록에서 작품·캐릭터 인식(국내 1,489건 중 78% 작품 인식). Wikidata 작품·캐릭터 라벨로 사전 보강.

## 2026-11-25 · 캐릭터 사전 대보충과 데이터 복구

- 라벨 오류 수정: 작품명과 같은 캐릭터(블랙 잭), 버전명을 캐릭터로 읽던 문제(初音ミク ヴァンパイア Ver.), 영문만 있는 제목 통과, 반복 단어 제목 용어 51개.
- 웹 검증값 오류 정리: `スケールフィギュア` 안의 `ルフィ`로 약 70개 상품이 몽키 D. 루피로 저장되어 있던 문제를 단어 경계 규칙으로 막고 74건 수정.
- Wikidata 캐릭터를 실제 제목 매칭에 사용(확정된 작품 안에서만, 기존 라벨은 바꾸지 않음), Wikidata의 조직·장소·아이템 2,178개 제외.
- 사용자 피드백 반영: 원신·명조·니케, 히소카×클로로 같은 세트 상품, 하츠네 미쿠 버전 통합, 일러스트레이터 오리지널 인식.
- 캐릭터가 비어 있는 작품 순서대로 사전 보충 4차(총 약 950개 캐릭터, 250개 이상 작품). 박스·세트·블라인드 라인은 작품만 매핑(캐릭터 해당 없음 303건). 하츠네 미쿠는 작품이자 캐릭터로 처리.
- **데이터 복구**: 약 50분마다 도는 공식 메타데이터 갱신이 원문 해시를 바꿔, 재처리할 때 검증값(web_verified)이 사라지던 문제를 발견. 근거가 새 원문에 남아 있으면 검증값을 유지하도록 고치고 1,806개 상품의 검증값을 아침 스냅샷에서 복원.
- 결과(전 상품 6,892개): ready **1,784 → 3,015**, 캐릭터 보유 3,962 → 5,314, 작품은 있는데 캐릭터가 없는 상품 1,947 → 284(이 중 88개는 번호 라인 `VOL.n`).

## 2026-11-26 · PC 이전 준비

- 남아 있던 옛 이름 "Figure Archive AI"·`FigureArchiveResearch`를 O_DOCK으로 변경. Docker 프로젝트명 `figure-archive-ai`, DB 이름 `figure_archive`, 브라우저 저장 키는 기존 데이터와 연결돼 있어 유지.
- 이전 묶음 3개를 Google Drive에 업로드: `O_DOCK_MOVE_1.zip`(코드·DB 덤프·검색 색인), `O_DOCK_MOVE_2.zip`(Ollama 번역 모델), `O_DOCK_MOVE_3.zip`(상품 이미지). 복원 방법은 각 zip의 `RESTORE_O_DOCK.md`.
- 모델 학습 산출물은 [학습 기록](MODEL_TRAINING_RECORD_20261126.md)만 남기고 보존하지 않음.

## git에 없는 작업 산출물 (`data/private/`, 보존 안 함)

| 위치 | 내용 |
|---|---|
| `semantics/split_queue_20261117`, `reprocess_2026112*` | 번역·분류 재처리 회차별 항목 JSON과 진행 기록. 결과는 DB에 반영되어 있다. |
| `semantics/20261112_*`, `20261113_pilot`, `20261116_*`, `recovery_v6_20261117` | 11-12 ~ 11-17 수정·재검증 회차의 미리보기와 감사 기록 |
| `instagram/`, `events/` | 행사 게시물·이미지 원본과 검수 HTML. 서비스용 행사 데이터는 DB에 있다. |
| `retail_price/`, `goodsmile_20261116`, `manufacturers_20261117` | 국내 유통·제조사 수집 실행 보고서 |
| `semantics/restore_20261125/` | 11-25 검증값 복원 직전의 필드 백업 |
