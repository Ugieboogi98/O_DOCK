# dev 브랜치 개선 보고 (2026-11-24)

| 항목 | 내용 |
| --- | --- |
| 브랜치 | `dev` (기준: `main`의 Initial commit) |
| 범위 | 번역·분류 성능, 운영 위험, 보안 경계, 가격 이력, 매칭 검토, CI |
| 검증 | Windows 로컬 pytest 377 통과 / 18 건너뜀(PostgreSQL 필요) / 3 실패(Linux 전용 `fcntl`·Windows 파일 권한, 변경 전과 동일), Vitest 38 통과, 프론트 빌드 성공 |
| 미검증 | Ollama·Docker가 꺼져 있어 실제 모델 호출과 컨테이너 실행은 확인하지 못함 |

## 1. 번역·분류 파이프라인 (`split-semantics-v7`)

### 현재 구조에 대한 정정
분류는 **임베딩 비교 방식이 아니다.** 현재 흐름은 `사전 일치 → qwen3:8b 번역 → 사전 근거 → qwen3:1.7b 생성형 분류 → 원문 근거 검증`이다. 임베딩(Chroma)은 검색에만 쓴다.

### 원인 분석 (`split_queue_20261117` 보고서 681건)
| 결과 | 건수 | 원인 |
| --- | --- | --- |
| 번역 실패 | 109 | 전부 `TRANSLATION_VALIDATION_FAILED`. 사전에 없는 인명이 한자·가나로 남음 (예: `夏目貴志&니ャン코`) |
| partial | 462 | 425건에서 캐릭터 누락. 258건은 설명문에 `『작품』の「캐릭터」`가 명시돼 있는데 사전에 한국어 표기가 없어 제외됨 |
| ready | 110 | |

### 변경
| 변경 | 파일 | 효과 |
| --- | --- | --- |
| 남은 일본어 구간 용어집 복구: 인명은 읽기(가나)만 모델에 묻고 한글 표기는 결정적으로 변환, 일반어는 뜻 번역 | `split_semantics.py`, `kana_hangul.py` | 번역 실패의 직접 원인 대응. 실패 시 기존 parts/review 단계로 이어짐 |
| 원문에 명시된 캐릭터·작품 명명: 가나 이름은 모델 없이 표기 | `split_semantics.py` (`name_explicit_relations`) | 캐릭터 누락 대응 |
| 검증 통과 결과에서 학습한 별칭(서로 다른 상품 2건 이상 일치, 충돌 없음) | `semantic_neighbors.py`, `build_semantic_dictionary.py` | 사전 범위 자동 확장. 근거는 여전히 원문 문자열 |
| 유사 상품 검색(문자 n-gram TF-IDF): 분류 모델에 검증된 예시 3건 제공 | `semantic_neighbors.py` | 임베딩 서버 없이 결정적으로 동작 |
| 작품명 안의 캐릭터명(`葬送のフリーレン`)은 캐릭터로 보지 않음 | `semantic_neighbors.py` | 오프라인 평가에서 발견한 회귀 수정 |

### 오프라인 측정 (모델 호출 없음, 하한값)
`python tools/eval_semantics.py --items data/private/semantics/split_queue_20261117/items`

| 분류 상태 | 이전 | 이후 |
| --- | --- | --- |
| ready | 110 | **196** |
| partial | 138 | 160 |
| review | 324 | **216** |

기존 라벨이 바뀐 상품은 없다(채워지기만 함, 캐릭터 128건). 모델이 필요한 단계(용어집 복구, 한자 인명)는 이 수치에 포함되지 않았다. Ollama를 켠 뒤 `--live --limit 20`으로 실패 건을 재측정한다.

### 실행 방법
```powershell
# 사전 재생성 (학습 별칭 포함)
docker compose -p figure-archive-ai exec -T backend python -m scripts.build_semantic_dictionary
# 이전 버전에서 실패 보류된 103건을 새 파이프라인으로 1회 재시도
.\.venv\Scripts\python.exe -u tools/run_split_semantics.py --watch --skip-failed --retry-stale-failures --limit 20 --report-dir data/private/semantics/split_queue_20261117
```

## 2. 운영 위험
- **소비자 중복 실행 방지**: PostgreSQL advisory lock(`worker_lock.py`)을 사용한다. 호스트와 Docker 소비자가 같은 DB를 쓰면 하나만 실행된다.
- **Compose `semantic-worker`**: 호스트와 같은 보고서 경로(`SEMANTIC_REPORT_DIR`)를 쓰고, `--skip-failed --retry-stale-failures`를 적용하며, 역할별 모델 환경변수를 받는다.
- **`POSTGRES_PASSWORD` 기본값 제거**: 값이 없으면 Compose가 시작을 거부한다. `.env.example`을 추가했다.
- **Git 관리**: `.gitignore`에 `cloud-backup*/`, 압축 백업, 토큰 파일을 추가했다. `.gitattributes`로 셸·Dockerfile 줄바꿈을 LF로 고정했다.

## 3. 보안
| 변경 | 이전 | 이후 |
| --- | --- | --- |
| 관리자 토큰과 개인 계정 분리 | 토큰이 유효하면 사용자 ID 1로 처리 | 개인 데이터는 로그인 세션만 허용 |
| 로그인·가입 IP 제한 | 계정별 5회 잠금만 있음 | IP당 로그인 20회/5분, 가입 10회/시간 추가 |
| 쓰기 요청 출처 | Origin이 없으면 통과 | `Sec-Fetch-Site: cross-site`이면 거부 |
| 관리자 토큰 | 길이 제한 없음, 기록 없음 | 24자 이상 필수, `odock.audit` 로그 |
| Nginx | 기본 헤더 | CSP, Permissions-Policy, `X-Real-IP`, 정적 자산 캐시 |

## 4. 가격 이력과 매칭 검토
- `retailer_offer_history` 테이블과 마이그레이션 `20261124_offer_history`를 추가했다. 기존 최신 관측을 첫 이력으로 옮긴다.
- `GET /api/figures/{fid}/price-history`를 추가하고, 상품 상세의 `PriceHistory.vue`에 판매처별 추이를 표시한다.
- 관리자 API `GET/POST/DELETE /api/admin/retail-matches`를 추가했다. 데이터 현황 화면의 `RetailMatchQueue.vue`에서 미연결 판매 기록에 JAN 일치·유사도 후보를 보여주고, 클릭하면 연결한다. 연결은 이후 관측에서도 유지된다.

## 5. CI
`.github/workflows/ci.yml`: 백엔드(PostgreSQL 16 서비스, Alembic 적용, pytest, 구조 검사), 프론트(Vitest, 빌드), 비밀값·백업 파일 커밋 차단. PostgreSQL 통합 테스트 18개는 로컬에서 실행하지 못했으므로 첫 CI 실행 결과로 확인한다.

## 6. 남은 과제
- 실제 Ollama로 실패 103건 재처리 및 `--live` 측정
- 일반 검색 임베딩 `hash` → 로컬 다국어 임베딩(bge-m3 등) 전환
- 행사 `events` 테이블 정식 사용(검수 단계), 구 가격 테이블 `retail_price_records` 정리
- 관심상품 가격 하락·재입고 알림 (가격 이력 기반)
