# 기존 제품 사진·한국어 제품명 누락 보강 · 2026-10-22

## 확인한 문제

사용자 보고: 처음 114개 제품에는 사진이 있으나 약 1,290개까지 확장했을 때 추가 제품 사진이 없고, 일본어 제품명 번역이 되지 않았다. 실행 중 서버에는 직접 접근하지 않았으므로 이번 작업에서 누락 건수 자체를 다시 측정하지는 않았다. 이전의 1,387개 수집 이력과 이번 보고의 약 1,290개를 임의로 같은 시점의 수치라고 간주하지 않는다.

소스에서는 다음 경로를 확인했다.

- `scripts.collect`의 이미지 다운로드는 `--images` 옵션이 필요하다. `collect_catalogs`와 앞선 통합 수집 패치는 메타데이터 수집용이다. 따라서 DB 제품 증가가 사진·번역 완료를 의미하지 않는다. 사용자 PC에서 실제 실행한 모든 명령을 확인한 것은 아니므로 추가 사진 누락의 유일한 원인이라고 단정하지 않는다.
- 메가하우스의 `.item_main img`, `a.colorbox` 갤러리 선택자가 누락되어 있었다. JSON-LD 및 og:image로 대표 사진을 얻을 수 있는 페이지도 있으므로, 선택자 누락만으로 모든 사진 누락을 설명하지는 않는다.
- 번역은 `name_ko`를 채우는 별도 API 작업이다. 기존 배치는 `RateLimitError`가 발생해도 다음 제품에 계속 요청했다. 이 예외명만으로 속도 제한인지 잔액/할당량 부족인지는 확정할 수 없다.

## 수정 내용

- 메가하우스 대표 이미지와 갤러리 선택자 추가. 추천 상품 이미지·로고를 무조건 전부 가져오는 방식은 사용하지 않는다. 빈 경로의 잘못된 og:image는 제외한다.
- `scripts.repair_assets` 추가: 기존 제품 조회, 누락 이미지만 보강, 한국어 제품명 없는 항목만 번역, 제품별 상태/실패 사유 저장, 작업 잠금, 실패 항목 명시적 재시도.
- 기본 사진 보강은 제품당 대표 사진 1장을 목표로 한다. 원문 설명은 이 경로에서 저장하지 않는다. 기존 사진 파일과 DB 제품 행을 삭제하지 않는다.
- DB에 사진 경로만 있고 실제 media 파일이 없으면 누락으로 판정한다. 같은 이미지 출처의 깨진 기존 경로는 다시 내려받아 복구한다.
- 번역의 SDK 자동 재시도 대신 최대 3회 재시도(최초 요청 포함 최대 4회), Retry-After 및 2초 기본 간격 적용. 공급자가 30초 초과 대기를 요구하면 다음 실행으로 넘긴다.
- 잔액/할당량 부족, 인증/권한, 모델/주소 오류는 즉시 번역 배치를 멈춘다. 429 반복이나 공급자 장애도 재시도 소진 후 중단한다. `both` 모드에서는 번역만 중지하고 이미지 작업은 계속할 수 있다.
- 번역 응답이 일본어이거나 한국어가 포함되지 않으면 저장하지 않는다. 기존 `name_ko`는 덮어쓰지 않는다.
- 번역 저장 시 RAG 재색인 outbox도 함께 기록한다. 기본 실행은 미완료 색인을 복구하고, 실패하면 DB의 한국어명은 유지한 채 pending 작업을 남긴다.
- 기존 `scripts.enrich --translation-only` 명령도 공급자 오류에서 중단하도록 수정했다. 상세 화면 번역 오류 메시지도 잔액·요청 제한·키·모델 문제를 구분한다.
- `scripts.audit_catalog`에 한국어명과 사진 누락 수를 추가했다.

사진 보강은 사용자가 명시적으로 실행하는 로컬 보강 작업이다. 기존 `personal_local` 표시를 유지하며 재배포 허가를 주장하지 않는다. 페이지의 도메인·경로·robots 검사는 그대로 적용한다. 비활성 출처나 차단을 해제하지 않았다. 사진 권리·실제 서비스 공개 범위 검토는 별개이며, 이번 변경으로 모든 제조사 사진 수집을 자동 활성화하지 않는다.

## 적용

이번 압축은 앞선 수집기 수정까지 포함하는 누적 버전이다. `patch/`의 내용물을 **기존** `figure-archive-ai` 폴더에 덮어쓴다. `.env`와 기존 Docker 볼륨은 유지한다. `docs/HANDOVER.md`의 PostgreSQL 백업 절차도 참고한다.

```bash
cd ~/Desktop/figure-archive-ai
export MSYS_NO_PATHCONV=1
docker compose config --quiet
docker compose up -d --build --no-deps backend
```

## 1. 실제 누락 수 확인

```bash
docker compose exec backend python -m scripts.audit_catalog
```

제조사별 `missing.name_ko`, `missing.product_images`를 본다. 사진은 DB에 경로가 있어도 해당 로컬 파일이 없으면 누락으로 계산한다. 권한 확인된 외부 이미지 URL은 가용 후보로 세지만 원격 서버의 실제 응답까지 검사하지는 않는다.

## 2. 사진 2개만 먼저 확인

```bash
docker compose exec backend python -m scripts.repair_assets \
  --mode images --only-missing --manufacturer MegaHouse --limit 2
```

`images_ready`가 증가하면 `http://localhost:8080/figures`를 새로고침해 제품 상세를 확인한다. CLI는 열려 있는 브라우저를 자동 갱신시키지 않는다.

성공한 뒤 메가하우스 누락분 전체를 보강한다.

```bash
docker compose exec backend python -m scripts.repair_assets \
  --mode images --only-missing --manufacturer MegaHouse
```

다른 제조사까지 보강하려면 `--manufacturer MegaHouse`를 빼면 된다. 비활성 정책의 출처는 실패 사유를 기록하며 차단을 우회하지 않는다. 여러 장이 필요하면 `--max-images 6`처럼 지정하되, `--only-missing`은 이미 사진이 1장이라도 있는 제품을 건너뛰므로 기존 제품의 갤러리 확장에는 이 옵션을 빼고 대상 제품/제조사를 제한한다.

## 3. 번역 2개만 먼저 확인

```bash
docker compose exec backend python -m scripts.repair_assets \
  --mode translations --only-missing --limit 2
```

이미 한국어명이 있는 제품은 API를 호출하지 않는다. 정상 저장을 확인하면 전체 누락 제품명을 번역한다.

```bash
docker compose exec backend python -m scripts.repair_assets \
  --mode translations --only-missing --request-interval 2
```

번역 대상은 **제품명**이다. 원문 상세 설명의 전문 번역 기능을 추가한 것은 아니다. ChatGPT 구독과 별개인 실제 사용 중 API 공급자의 계정·할당량을 확인해야 한다. API 키 자체를 채팅이나 로그에 붙이지 않는다.

| 출력 | 의미와 조치 |
|---|---|
| `QUOTA_EXHAUSTED` | 공급자 응답 코드가 잔액·할당량 부족을 나타냄. 공급자 대시보드의 잔액/할당량 확인. 대기·재시도 코드만으로 해결되지 않음 |
| `RATE_LIMIT_EXHAUSTED` | 429가 재시도 후에도 지속됨. 잠시 뒤 `--request-interval 5` 또는 10으로 재실행. 429만으로 일시 속도 제한인지 다른 공급자 제한인지는 확정 불가 |
| `RETRY_AFTER_REQUIRES_LATER_RUN` | 공급자가 긴 대기를 요구함. 안내된 제한이 풀린 뒤 재실행 |
| `LLM_API_KEY_REQUIRED` | backend의 LLM_API_KEY 설정 필요 |
| `AUTH_OR_PERMISSION_ERROR` | 키·계정·모델 접근 권한 확인 |
| `MODEL_OR_ENDPOINT_NOT_FOUND` | LLM_MODEL과 LLM_BASE_URL 확인 |
| `TRANSLATION_REQUEST_REJECTED` | 공급자 요청 형식/해당 모델의 JSON 응답 지원 여부 확인 |
| `INVALID_TRANSLATION_RESPONSE` / `TRANSLATION_NOT_KOREAN` | 개별 응답 파싱/언어 검증 실패. 기록된 제품 ID로 재시도하거나 수동 수정 |

설정을 바꾼 `.env`는 컨테이너를 재생성해야 반영된다.

```bash
docker compose up -d --no-deps --force-recreate backend
```

## 재개와 실패 확인

성공 여부는 현재 DB·실제 파일을 기준으로 판단한다. 같은 명령을 다시 실행해도 완료된 제품을 다시 번역하거나 중복 제품으로 등록하지 않는다. 기존 실패 항목을 다시 시도하려면 다음처럼 실행한다.

```bash
docker compose exec backend python -m scripts.repair_assets \
  --mode images --only-missing --manufacturer MegaHouse --retry-failed

docker compose exec backend python -m scripts.repair_assets \
  --mode translations --only-missing --retry-failed --request-interval 5
```

공급자 전역 오류는 해결 후 재실행하면 `--retry-failed` 없이도 다시 점검한다. 개별 파싱·다운로드 오류는 기본적으로 자동 반복하지 않는다. 상태 파일은 `/app/media/asset_repair/checkpoint.json`, 실행 요약은 같은 폴더의 `last_run.json`이다. `/data`에는 쓰지 않는다.

```bash
docker compose exec backend cat /app/media/asset_repair/last_run.json
docker compose exec backend python -m scripts.audit_catalog
```

이미지와 번역을 한 번에 처리하는 것도 가능하다.

```bash
docker compose exec backend python -m scripts.repair_assets --mode both --only-missing
```

실패가 있으면 종료 코드 1, 정상 완료는 0, Ctrl+C 중단은 130이다. `--limit`은 전체 DB의 처음 N개가 아니라, 보강이 필요한 제품 중 이번에 처리할 N개를 뜻한다. 실패 이력으로 건너뛰는 제품도 이 작업 한도에 포함된다. 대량 작업 전에 각각 소량 점검하는 절차를 권장한다.

번역 후 색인만 다시 복구하려면 기존 명령을 사용한다.

```bash
docker compose exec backend python -m scripts.collect_other_makers --retry-index-only
```

## 검증 범위

- 메가하우스 `https://megahobby.jp/products/item/6115/`의 실제 HTTP 200 HTML 응답에서 상품 이미지 후보를 추출했다. 실제 사용자 Docker에서 이미지 파일 다운로드까지 확인한 것은 아니다. 개발 환경의 직접 DNS 제한은 유지되고 있다.
- 신규 테스트에서 사진 저장·재실행 중복 방지·없는 로컬 파일 복구·상세 설명 미저장·429 재시도 한도·큰 Retry-After 중단·할당량 부족 시 다음 제품 요청 중단·일본어 응답 거부·번역 저장과 재색인 요청의 원자성을 확인했다.
- 실제 유료 번역 API 호출은 하지 않았다. 테스트는 모의 API 응답을 사용했다. 사용자 서버의 RateLimitError가 해결됐다고 주장하지 않는다.
- 최종 테스트 건수는 `test-results-assets.xml`에 기록했다. PostgreSQL 전용 18개는 서버가 없어 제외했다. 프론트엔드 파일은 이번 보강에서 변경하지 않았다.
