> 이 문서는 작업 당시의 이력입니다. 이후 변경된 경로는 [현재 프로젝트 구조](../PROJECT_STRUCTURE.md)를 확인하세요.

# 수집과 의미 검증 대기열 연결 — 2026-11-10

## 변경 결과

`catalog_ingest.collect_one()`의 신규 상품은 상품·기존 인덱싱 작업·의미 검증 대기 작업을 같은 트랜잭션으로 저장한다. 검증 대기 작업 저장에 실패하면 신규 상품 저장도 되돌아간다.

기존 `CollectionJob`을 재사용하며 collector는 `catalog_semantics:<상품ID>`다. payload에는 상품 ID, 공식 URL, source hash를 저장한다. 대기 중인 동일 상품은 작업을 추가하지 않고 최신 원문 해시로 갱신한다. PostgreSQL에서는 상품별 transaction advisory lock으로 중복 생성을 직렬화한다.

상세 설명 보강 후 같은 대기 작업을 갱신한다. 이미지 보강이 일부만 저장되고 실패한 경우에도 현재 저장된 원문 해시가 반영된다. 상품을 다시 발견하면 빠진 대기 작업을 복구하되 상세 페이지를 다시 요청하지 않는다. 유효한 의미 결과가 이미 있으면 새 작업을 만들지 않는다.

## 호출과 게시 정책

- 자동 수집에서 옛 `translate_name()` 호출을 제거했다. 기존 `auto_translate_names`가 켜져 있어도 이 수집 경로는 유료 상품명 번역을 직접 호출하지 않는다.
- 수집 시에는 원문 메타데이터와 대기 작업만 저장한다. 한국어 의미 정보는 기존 CLI preview → 검토 → apply 경로에서 필드별 검증 후 게시한다.
- `run --queued`는 대기 상품만 선택하며 기존 `--limit`과 제조사/상품 ID 필터를 함께 적용한다. 명시적인 run은 유료 호출을 할 수 있다.
- preview는 작업을 소비하지 않는다. apply에서 검증 결과 저장과 해당 source hash의 작업 완료를 함께 커밋한다.
- 결과가 review이면 작업도 review로 남고, pending 목록에서 자동 재시도하지 않는다. ready/partial은 completed로 기록한다.
- 다른 source hash의 작업은 완료 처리하지 않는다. 원문 변경 시 예전 보고서 apply는 기존 SOURCE_CHANGED_RETRY 검사로 차단된다.
- 기존 명시적 번역 API/다른 오프라인 importer는 이번 변경 대상이 아니다. 모든 importer와 관리자 인증이 통합 완료됐다는 의미는 아니다.

## 운영 명령

읽기 전용이며 유료 호출 없는 확인:

```powershell
docker compose -p figure-archive-ai exec -T backend python -m scripts.product_semantics status
docker compose -p figure-archive-ai exec -T backend python -m scripts.product_semantics pending --limit 5
```

아래 run은 유료 호출을 할 수 있으므로 이번 작업에서는 운영 DB 대상으로 실행하지 않았다. 보고서 이름은 새 이름을 사용한다.

```powershell
docker compose -p figure-archive-ai exec -T backend python -m scripts.product_semantics run --queued --limit 5 --report /app/media/semantic_reports/queued_preview_NEW.json
# 보고서 검토 후:
docker compose -p figure-archive-ai exec -T backend python -m scripts.product_semantics apply --report /app/media/semantic_reports/queued_preview_NEW.json
```

## 검증과 실제 상태

- 관련 백엔드 테스트 **112개 통과**. 상품/작업의 원자적 저장, 반복 수집 시 작업 재사용, 원문 변경, 부분 보강 실패, 유료 함수 호출 금지, queued preview/apply/재개, 대기하지 않은 상품 제외를 추가 검증했다.
- 테스트의 신규 데이터와 모델 응답은 격리 SQLite와 모의 응답을 사용했다. 동시 PostgreSQL 쓰기 경합은 이번에 실험하지 않았다.
- backend만 `up -d --build --no-deps backend`로 반영. DB 스키마 변경, 기존 데이터 전수 등록, 수집 실행, 유료 API 호출 없음.
- 반영 후 실제 PostgreSQL에서 pending 조회와 queued 선택 SQL 실행 성공. 대기 0건, 상품 6,158개, 의미 레코드 ready 3 / partial 2, 이미지 duplicate_hidden 1,555건 유지. health 정상.
- 대기 0건은 기존 전체 상품을 처리했다는 뜻이 아니다. 이번에는 기존 상품 전체를 대기열에 넣지 않았다. 이후 이 수집 경로로 신규 저장되거나 재발견되는 상품부터 적용된다.

## 변경 파일과 되돌리기

- 새 `backend/app/services/semantic_queue.py`: 대기 작업 수명·원문 버전 관리.
- `seed_import.seed(..., commit=False)` 추가: 호출자가 원자적 저장 경계를 관리할 수 있도록 했다. 기존 호출은 기본 commit=True로 유지한다.
- `catalog_ingest.py`: 수집/보강과 대기열 연결, 자동 구번역 호출 제거.
- `product_semantics.py`: 검증 저장 시 일치하는 작업 완료.
- `scripts/product_semantics.py`: pending, --queued, status의 queued 집계.
- 변경 전 소스: `backups/semantic_queue_20261110/`. 해당 4개 파일을 원래 위치에 복원하고 backend를 재빌드하면 이전 동작으로 돌아간다. 대기 작업은 DB에 남으며 삭제하지 않는다.

## 계속 남은 작업

후속 진행: [공용 카탈로그 관리자 권한 경계](ADMIN_BOUNDARY_20261110.md)를 반영했다. 아래 과제 중 공용 카탈로그 쓰기 인증을 구현했으며, 개인 사용자별 소유권과 계정 인증은 아직 남아 있다.

관리자 인증/일반 사용자 권한 분리, 다른 importer의 공통 저장 경로 연결, 한국어 alias 출처 확장, 이름 편집 이력 분리, 실제 이미지 표본 육안 검사와 URL 변경 시 유사 중복 방지, 검색 SQL 지연 시간 최적화는 후속 과제다.
