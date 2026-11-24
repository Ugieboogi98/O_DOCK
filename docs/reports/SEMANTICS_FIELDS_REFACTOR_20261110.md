> 이 문서는 작업 당시의 이력입니다. 이후 변경된 경로는 [현재 프로젝트 구조](../PROJECT_STRUCTURE.md)를 확인하세요.

# 필드별 게시 및 목록 조회 리팩터링 — 2026-11-10

## 변경된 동작

한 형태 오류로 상품의 번역·작품·캐릭터까지 모두 숨기던 정책을 필드 단위로 바꿨다.

- `field_status`: name_ko / franchise_ko / character_ko / figure_form 각각 ready, missing, review.
- `field_issues`: 필드별 보류 사유. 기존 issues도 유지한다.
- 보류 필드는 값·연관 목록·근거를 게시 필드에서 제거한다. 원래 모델 제안은 원본 보고서에 남는다.
- 캐릭터 목록 일부가 잘못됐거나 누락됐다면 캐릭터 필드 전체를 보류한다. 일부 목록을 완전한 목록처럼 게시하지 않는다.
- 한 개 이상 게시 가능한 필드가 있으면 상품 상태 partial. 모두 불확실하거나 응답 구조 자체가 잘못되면 review.
- classification_status는 분류 오류가 남으면 review일 수 있다. 상품 partial과 분류 review는 다른 의미다.
- 기존 비어 있지 않은 Figure.name_ko, 원문·출처·개인 기록을 덮어쓰지 않는다.
- 저장명과 새 번역이 다르면 API의 `semantic_name_ko` 및 상세 화면에서 새 번역을 별도로 제공한다. 사용자가 입력란에 가져온 뒤 이름 저장을 선택할 수 있다. 추가 모델 호출은 없다.

현재 의미 레코드가 있는 상품의 예전 KoreanProfile은 검색과 상세 화면에서 그 결정을 덮어쓰지 않는다. 목록·상세·작품 집계·형태 필터는 동일하게 정제된 필드를 사용한다. 기존 원문 검색은 계속 지원한다.

검증 규칙 버전은 `ja-ko-semantics-v4-fields`. 예전 해시의 의미 결과는 새 규칙으로 재검증하기 전까지 사용하지 않는다. CLI의 recheck는 기존 응답을 재사용하며 모델을 호출하지 않는다.

## 실제 응답 재사용과 DB 반영

원본: `/app/media/semantic_reports/furyu_first5_v3.json` (호스트 보존본: `backups/semantics_fields_20261110/furyu_first5_v3.json`).

새 보고서: `migration_backup/furyu_first5_v4_fields_20261110_1532.json` 및 Docker `/app/media/semantic_reports/`의 같은 파일명.

| ID | 상태 | 결과 |
|---|---|---|
| 48–50 | ready | 기존 근거 기반 번역/작품/캐릭터/미니 형태 유지 |
| 51 | partial | 프리렌, 장송의 프리렌 사용. 형태 missing |
| 52 | partial | 페른, 장송의 프리렌 사용. 잘못된 소프비만 review |

- 유료 API 호출 0회. 위 5건만 recheck → 검토 → apply했다.
- 운영 PostgreSQL 상태: 상품 6,158개, 의미 레코드 ready 3 / partial 2.
- 52번 상세·캐릭터 검색에서 페른 확인. soft_vinyl 형태 검색에서는 52번 제외 확인.
- 52번의 기존 저장명 `TENITOL TALL 펀 클래식 원피스ver.`는 보존한다. 새 번역은 `TENITOL TALL 페른 클래식 원피스ver.`로 별도 노출한다. 저장명과 수동 편집의 과거 이력을 구분할 근거가 없으므로 자동 덮어쓰지 않았다.
- 48–50의 한국어 이름은 모델 번역이다. 공식 한국어 명칭을 새로 조사·인증한 것은 아니다.
- 나머지 6,153개 상품을 이번 작업에서 새로 번역하지 않았다.

## 책임 분리와 조회 구조

- `services/semantic_policy.py`: 필드별 게시·제거·전체 상태 결정. 제공자 호출이나 DB 저장 없음.
- `services/product_semantics.py`: 기존 근거 검사 유지. 필드별 오류를 정책에 전달하고 `current_many()`로 한 페이지의 의미 레코드와 상위 설명을 일괄 검증.
- 설명은 상품별 official_detail 우선, ID 역순, 최대 3개라는 기존 규칙 유지. 윈도 함수로 필요한 문서만 가져온다.
- `services/image_order.py`: `ordered_images_many()` 추가. 단건 조회도 같은 함수를 사용해 가시성·품질·ID 순서를 유지.
- `repositories/figures.py`: 목록에서 의미 결과·이미지·관심상품을 일괄 읽고 카드에 전달. 단건 카드와 반환 내용 일치 검증.
- `frontend/src/services/semantics.js`: 보류 필드의 구번역 fallback 차단과 안내 문구 생성.

운영 DB에서 동일한 `q=TENITOL, page_size=24`와 동일한 상품 ID 목록으로 측정한 SQL 실행 횟수: **81 → 9**. 응답시간은 단발 측정에서 약 2초로 비슷했다. SQL 횟수 감소를 응답시간 향상으로 주장하지 않는다. 복잡한 검색 SQL과 파일 크기 판독 비용은 별도 측정 대상이다.

## 검증과 배포

- 백엔드: asset_repair, product_semantics, semantics_context, semantics_migration, refactor, catalog_pipeline, quality **107개 통과**.
- 프런트엔드 **19개 통과**, 최종 Docker production build 성공.
- 잘못된 필드의 검색/작품 집계 제외, 모든 필드 오류 시 review, 수동 이름 보존, 문서 변경 시 캐시 무효화, 문서 순서 동일성, 일괄 조회 2회, 단건/목록 카드 일치, 숨김 이미지 제외, 관심상품 유지 등을 검증했다.
- backend와 frontend만 `up -d --build --no-deps`로 반영했다. init/seed/worker 재실행 없음.
- Nginx를 경유한 실제 상세 API와 health 정상. 이미지 duplicate_hidden 1,555건 유지 확인.
- 브라우저 렌더링 육안 검증은 수행하지 않았다. 기존 onMounted 갱신 요청을 실행하지 않도록 API와 빌드 결과로 검증했다.

## 백업 및 되돌리기

- 적용 전 전체 DB 백업: `migration_backup/before_semantics_v4_20261110_1532.dump`. pg_restore --list 성공 확인.
- 변경 전 소스 보존본: `backups/semantics_fields_20261110/` (product_semantics.py, figures.py, image_order.py, FigureDetailView.vue, KoreanName.vue 및 수정 전 테스트).
- DB 스키마 변경 없음. 소스만 되돌릴 때는 보존본의 각 파일을 원래 위치에 복원하고 backend/frontend를 다시 빌드한다. 새로 추가한 파일은 구버전에서 사용하지 않는다.
- v4 적용으로 바뀐 파생 데이터는 새 source hash 때문에 구버전에서 게시되지 않는다. 원본 v3 응답을 구버전 CLI apply로 재검증해 이전 파생 상태로 되돌릴 수 있다. 기존 상품명은 이번 5건에서 덮어쓰지 않았다.
- 전체 DB 복원은 이후 데이터까지 되돌릴 수 있으므로 자동 수행하지 않는다.
- Git 저장소가 아니므로 커밋은 하지 않았다.

## 남은 후속 과제

추가 진행: [수집과 의미 검증 대기열 연결](SEMANTIC_QUEUE_20261110.md). catalog_ingest 경로는 대기열과 필드별 검증 CLI에 연결했다. 관리자 인증과 다른 importer 통합은 남아 있다.

1. 이미지 실제 표본 육안 검사와 다른 URL로 재등록되는 유사 이미지 방지.
2. 여러 제조사/굿즈/다인 캐릭터의 실제 응답 평가 및 출처 있는 한국어 alias 사전 확장. 단순 규칙 통과를 번역 정확도로 해석하지 않는다.
3. 수동 이름과 자동 번역의 출처/편집 이력 분리. 현재는 저장명 보존 + 새 번역 별도 표시 정책이다.
4. 수집→의미 검증→게시의 공통 저장 흐름과 관리자 권한. 실행 시 갱신 정책을 유지하되 일반 사용자 권한과 분리해야 한다.
5. 검색 SQL 실행 계획 및 지연 시간 측정 후 추가 최적화. 이번 단계는 정책 분리와 목록 N+1 제거까지다.
