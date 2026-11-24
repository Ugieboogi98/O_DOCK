# O_DOCK 프로젝트 파일 구조 및 시스템 보고서

| 항목 | 내용 |
| --- | --- |
| 작성일 | 2026년 11월 24일, 한국 시간 |
| 프로젝트 | `Project_O_DOCK_V1` / O_DOCK |
| 보고 범위 | 서비스 아키텍처, 기술, 파일 구조, 데이터 모델, API, 운영·검증 |
| 확인 기준 | 현재 프로젝트 파일, 저장소 내 검증 자료, 마지막으로 저장된 처리 상태 |
| 기존 구현 보고 | [2026-11-17 구현 현황](O_DOCK_IMPLEMENTATION_SUMMARY_20261117.md) |

| 필요한 정보 | 찾아갈 항목 |
| --- | --- |
| 서비스 목적과 구성, 사용 기술 | [프로젝트 개요](#1-프로젝트-개요), [시스템 구성](#2-시스템-구성), [사용 기술](#3-사용-기술) |
| 폴더와 파일, API, DB | [루트 폴더와 파일](#4-루트-폴더와-파일), [백엔드 모듈과 API](#5-백엔드-모듈과-api), [데이터베이스 구성](#6-데이터베이스-구성) |
| 수집·번역·검색·행사 | [제조사 데이터 수집과 반영](#7-제조사-데이터-수집과-반영), [국내 유통사 가격과 환율](#8-국내-유통사-가격과-환율), [상품명 번역·분류](#9-상품명-번역분류-파이프라인), [검색과 AI 답변](#10-검색과-ai-답변), [행사·SNS](#11-행사sns-수집과-화면) |
| 화면과 계정 | [프론트엔드 상세 구조](#12-프론트엔드-상세-구조), [인증·권한 경계](#13-인증권한-경계) |
| 운영, 검증, 유지보수 | [Docker 배치](#14-docker-배치와-운영-파일), [운영 명령](#15-운영-명령과-문제-확인), [검증 결과](#16-검증-결과와-기준-시점), [유지보수 파일](#17-유지보수-시-확인할-파일) |

## 1. 프로젝트 개요

O_DOCK은 일본 공식 피규어·굿즈의 원문, 사양, 상품 이미지 및 발매 정보를 모아 한국어로 탐색할 수 있게 만든 카탈로그 서비스다. 국내 4개 유통사의 판매 정보를 같은 상품 판본에 연결해 비교하고, 계정별로 관심상품과 구매·배송 기록을 관리한다. 공식 홈페이지와 Instagram에서 확보한 서브컬처 행사도 별도 화면에 표시한다.

| 이용 주체 | 주요 흐름 |
| --- | --- |
| 일반 방문자 | 홈·신상품 탐색 → 제조사·작품·캐릭터 탐색 또는 검색 → 상품 상세·판본·가격 확인 → 원문·판매처 이동 |
| 로그인 사용자 | 가입·로그인 → 관심상품 등록 → 구매 금액·구매처·배송 상태 기록 → 개인 목록 관리 |
| 카탈로그 관리자 | 데이터 현황 → 관리자 토큰 확인 → 최신 정보 갱신 요청 → 수집 작업과 결과 확인 |
| 서버 운영자 | Docker 서비스·볼륨 관리 → 가져오기·모델 처리·재색인 실행 → DB 및 로그에서 상태 확인 |
| 행사 이용자 | 행사 탭 → 유형·지역·진행 상태 필터 → 일정·장소·이미지·원문·예약 정보 확인 |

## 2. 시스템 구성

```text
사용자 브라우저
  │
  └─ 127.0.0.1:8080 → Nginx / Vue SPA
        └─ /api/* → FastAPI (backend:8000)
              ├─ PostgreSQL (postgres:5432) → 상품, 가격, 계정, 작업, 행사
              ├─ Chroma (chroma:8000)      → 검색용 인덱스
              └─ /api/media/*             → 상품 이미지

운영 스크립트 / 수집 작업
  ├─ 공식 제조사 → 상품·이미지·원문 → PostgreSQL·media → 색인·의미 작업
  ├─ 국내 유통사 → 판매 관측 → 상품 판본 연결 → 가격 비교 API
  └─ 공식 홈페이지 / Meta Graph → 행사 원본·후보 → 행사 API

호스트 번역·분류 처리기
  ├─ PostgreSQL (127.0.0.1:5432) → 대기 작업 조회·결과 저장
  ├─ 참조 사전 → 일치 항목 재사용 및 분류 근거
  ├─ Ollama (127.0.0.1:11434) → 상품명 번역 모델 / 분류 모델
  └─ data/private/semantics/ → 단계 캐시, 진행 상태, 실패 사유
```

브라우저는 상대 경로 `/api`로 요청한다. 운영용 Nginx는 Vue 빌드 결과를 제공하고 `/api/`는 같은 Compose 네트워크의 FastAPI로 전달한다. 개발 중에는 Vite가 같은 경로를 프록시한다. 상세 URL을 직접 열거나 새로고침하면 Nginx가 SPA의 `index.html`을 제공하고 Vue Router가 화면을 선택한다.

PostgreSQL은 업무 데이터의 기준 저장소다. Chroma는 상품·판본·문서에서 파생된 검색 인덱스다. 상품 이미지 파일은 media 경로에 두고 이미지의 소속과 출처는 DB에 연결한다. 호스트 작업과 Docker 작업은 실행 방식에 따라 서로 다른 파일 경로와 보고서 위치를 사용한다.

구성 근거: [Compose 정의](../../docker-compose.yml), [FastAPI 진입점](../../backend/app/main.py), [Nginx 설정](../../frontend/nginx.conf), [Vite 설정](../../frontend/vite.config.js).

## 3. 사용 기술

버전은 Dockerfile, 패키지 선언 또는 의존성 고정 파일 기준이다. 프론트엔드의 `^` 표기는 패키지 허용 범위이며 Docker 빌드는 lockfile을 사용하는 `npm ci`로 설치한다.

| 계층 | 기술·선언 버전 | 사용 목적 |
| --- | --- | --- |
| 백엔드 실행 | Python 3.12 Slim, FastAPI 0.156.4, Uvicorn 0.54.0 | API 라우팅, 요청 검증, ASGI 서버 |
| 스키마·설정 | Pydantic 2.14.1, pydantic-settings 2.16.1, python-dotenv 1.2.4 | 입력 모델, 환경변수, 호스트 도구 설정 |
| DB | PostgreSQL 16 Alpine, SQLAlchemy 2.1.5, psycopg 3.3.6, Alembic 1.20.0 | 관계형 저장, ORM, DB 연결, 스키마 변경 이력 |
| 웹 수집 | HTTPX 0.28.1, Requests 2.34.2, Beautiful Soup 4.15.0 | HTTP 접근, HTML·정형 데이터 추출 |
| 검색·문서 | Chroma 1.5.9, LangGraph 1.2.16, langchain-openai 1.7.2, pypdf 6.21.1 | 벡터 인덱스, 근거 기반 답변 흐름, 설정형 모델 연결, PDF 입력 |
| 상품 의미 처리 | Ollama, Qwen3 8B / 1.7B | 로컬 상품명 번역 및 작품·캐릭터·형태 분류 |
| 프론트 앱 | Vue ^3.5.0, Vue Router ^4.5.0, Pinia ^3.0.0 | SPA 컴포넌트, 라우팅, 공유 상태 |
| UI·빌드 | Vite ^6.4.0, Tailwind CSS ^3.4.17, PostCSS ^8.5.0, Lucide Vue ^0.468.0 | 개발·번들링, 레이아웃과 공통 스타일, 아이콘 |
| 웹 배포 | Node.js 22 Alpine 빌드 단계, Nginx 1.28 Alpine 제공 단계 | 의존성 설치, 정적 파일 제공, API 리버스 프록시 |
| 테스트 | pytest 9.1.1, Vitest ^3.2.0, Playwright 도구 | 백엔드 테스트, 프론트 테스트, 실제 화면 점검 |
| 서비스 실행 | Docker Compose, Windows PowerShell, POSIX 셸 | 서비스·볼륨 연결, 업데이트·마이그레이션·작업 진입점 |

선언 위치: [백엔드 의존성](../../backend/requirements.txt), [백엔드 Dockerfile](../../backend/Dockerfile), [프론트 의존성](../../frontend/package.json), [프론트 lockfile](../../frontend/package-lock.json), [프론트 Dockerfile](../../frontend/Dockerfile).

## 4. 루트 폴더와 파일

```text
Project_O_DOCK_V1/
├─ backend/                 API, 서비스, 수집기, ORM, CLI, 마이그레이션
│  ├─ app/
│  │  ├─ api/                HTTP 인터페이스
│  │  ├─ core/               환경 설정, DB 세션, 권한
│  │  ├─ models/             SQLAlchemy 데이터 모델
│  │  ├─ schemas/            API 요청 모델
│  │  ├─ repositories/       상품 조회·응답 조립
│  │  ├─ services/           업무 규칙, 저장, 작업 상태
│  │  ├─ collectors/         제조사·유통사 등 외부 데이터 파서
│  │  ├─ integrations/       행사용 Instagram·공식 홈페이지 연동
│  │  ├─ rag/                인덱스·임베딩·근거 검색·답변
│  │  └─ search_agents/      외부 문서 발견·상품 일치 보조
│  ├─ alembic/               DB 버전 이력
│  ├─ scripts/               Python 모듈로 실행하는 운영 명령
│  └─ tests/                 백엔드 테스트
├─ frontend/
│  ├─ src/
│  │  ├─ views/              페이지
│  │  ├─ components/         반복 UI 요소
│  │  ├─ router/             URL과 페이지 연결
│  │  ├─ services/           API·상품·권한 관련 호출
│  │  └─ stores/             Pinia 상태
│  ├─ Dockerfile             Vue 빌드와 Nginx 이미지 구성
│  └─ nginx.conf             정적 파일, SPA fallback, API 프록시
├─ data/                    설정, 초기 데이터, 외부 입력, 사전, 실행 결과
├─ media/                   호스트 방식의 이미지·작업 파일 경로
├─ scripts/                 업데이트·가져오기 등 프로젝트 전체 진입점
├─ tools/                   호스트 작업, 구조 검사, 이미지·화면 도구
├─ O_DOCK_LOCAL_SEMANTICS/   독립 모델 실험·학습·평가 및 Ollama 구성
├─ docs/                    요구사항·설계·운영·보고·검증 문서
├─ backups/                 작업별 적용 전 스냅샷과 복구 자료
├─ cloud-backup/            별도 백업 자료
├─ cloud-backup;C/          현재 작업 폴더에 남아 있는 백업 산출물 경로
├─ .venv/                   호스트 Python 가상환경
├─ .env                     로컬 환경 설정
├─ .gitignore               비밀값·생성물·백업 등의 관리 제외 규칙
├─ docker-compose.yml       서비스 네트워크·볼륨·포트 정의
├─ exchange_meta_token.py   Meta 토큰 교환 보조 스크립트
├─ THIRD_PARTY_NOTICES.md    외부 데이터·자료 출처 고지
└─ README.md                실행 안내 및 문서 링크
```

| 경로 | 자료 성격과 용도 |
| --- | --- |
| `data/source_policy.json` | 외부 도메인·수집 출처 접근 정책 |
| `data/catalog_sources.json` | 제조사 목록 출처, 자동 수집 여부, 회차 한도 |
| `data/other_makers_sources.json`, `seed_urls.txt` | 추가 제조사 후보와 초기 URL 입력 |
| `data/figures.json`, `data/database.sql` | 초기 상품 묶음 및 SQL 자료 |
| `data/imports/registry.json` | 제조사 입력 묶음 이름, 실제 경로, 실행 모듈 연결 |
| `data/imports/furyu/20261110/`, `data/imports/sega/s_fire/20261028/`, `data/imports/taito/20261028/` | 원본 외부 수집 묶음과 수집 당시 기록 |
| `data/reference/wikipedia_anime/` | 작품 목록 원본·출처·버전·정규화 결과 |
| `data/reference/semantic_dictionary/` | 운영용 통합 사전 `catalog.json`과 지문별 `versions/` 스냅샷 |
| `data/samples/` | 확인·재현용 입력 표본 |
| `data/private/` | 상품·가격·SNS·행사·모델 실행 결과 및 체크포인트 |
| `backups/imports/`, `backups/migrations/`, `cloud-backup/` | 가져오기·마이그레이션 전후 및 백업 자료 |
| `docs/reports/`, `docs/evidence/` | 작업 보고서와 JSON/XML 등의 검증 증거 |
| `docs/retail_price/`, `docs/design/`, `docs/reviews/` | 가격 설계, 디자인 검증, 분류 검토 자료 |

업무 코드의 기준 위치는 `backend/`와 `frontend/`다. 제조사 패키지 내부의 원본 코드와 백업 폴더는 당시 자료를 보존한다. 호스트의 `media/`와 Docker의 `media_data`는 별도 저장 위치다. `.env`, 비공개 데이터, 백업은 `.gitignore` 기준으로 관리한다. [프로젝트 구조 기준](../PROJECT_STRUCTURE.md), [가져오기 묶음 안내](../../data/imports/README.md), [관리 제외 규칙](../../.gitignore).

## 5. 백엔드 모듈과 API

### 5.1 코드 진입점과 책임

| 파일 또는 경로 | 책임 |
| --- | --- |
| `backend/app/main.py` | FastAPI 생성, 라우터 등록, CORS, media 정적 경로, 예외 응답, API 캐시 정책 |
| `backend/app/core/config.py` | Pydantic 환경 설정, 로컬 경로 기본값, 모델·검색·수집 설정 |
| `backend/app/core/database.py` | SQLAlchemy 엔진, 세션 팩토리, 요청별 DB 세션 의존성 |
| `backend/app/core/security.py` | 관리자 토큰 검증, 쓰기 요청에서 사용하는 Origin 허용 규칙 |
| `backend/app/schemas/requests.py` | 채팅·비교·검색 등의 공용 입력 모델 |
| `backend/app/repositories/figures.py` | 상품 목록 SQL 필터, 판본 선택, 관계 일괄 로딩, 응답 조립 |
| `backend/app/services/product_semantics.py` | 원문 컨텍스트 작성, 해시·결과 검증, 게시 데이터 저장 |
| `backend/app/services/import_pipeline.py` | 제조사 묶음의 DB 저장과 후속 작업 등록 |
| `backend/app/services/accounts.py` | 비밀번호 해시, 사용자 세션 발급, 인증·소유권 의존성 |
| `backend/app/services/personal_records.py` | 구매 기록 유효성 검사 및 저장 |
| `backend/app/services/exchange_rates.py` | JPY/KRW 환율 캐시와 유효성 확인 |
| `backend/app/services/event_catalog.py` | 행사 후보 집계, 중복 통합, 한국 날짜 기준 일정 상태, 목록 필터 |

### 5.2 API 축약 목록

| 기능 | 대표 API | 구현 파일 |
| --- | --- | --- |
| 헬스·공용 데이터 상태 | `GET /api/health`, `GET /api/status` | `backend/app/api/catalog.py` |
| 카탈로그 브라우징 | `GET /api/manufacturers`, `/api/product-lines`, `/api/franchises`, `/api/figures` | `catalog.py` |
| 상품 상세·가격·출처 | `GET /api/figures/{fid}`, 하위 `/prices`, `/used-market`, `/sources`, `/semantics` | `catalog.py` |
| 자연어 조건 검색·비교·상품 채팅 | `POST /api/search/natural-language`, `/api/compare`, `/api/rag/chat` | `catalog.py` |
| 한국어 검색·번역 보기 | `POST /api/search/korean`, `GET /api/figures/{fid}/korean` | `korean.py` |
| 상품 설명·관리자 번역·이름 수정 | `GET /api/figures/{fid}/description`, 관리자 하위 `/translate`, `/korean-name` | `product_text.py` |
| 국내 가격 관측 | `GET /api/retail-offers`, 연결 상품 상세의 가격 API | `retail_offers.py`, `catalog.py` |
| 공식 현지 가격·환율 | `GET /api/exchange-rate`, `GET /api/figures/{fid}/local-prices` | `pricing.py` |
| 공식 한국 가격 관리 | 관리자 `POST /api/korea-prices/preview`, `POST /api/korea-prices`, `DELETE /api/korea-prices/{pid}` | `korea_prices.py` |
| 가입·로그인·로그아웃·내 계정 | `/api/auth/register`, `/login`, `/logout`, `/me` | `accounts.py` |
| 관심상품 | `GET /api/favorites`, `PUT / DELETE /api/favorites/{fid}` | `personal.py` |
| 구매 관리 | `GET / POST /api/purchases`, `PUT / DELETE /api/purchases/{pid}` | `personal.py` |
| 관리자 확인 | `GET /api/admin/session` | `admin.py` |
| 카탈로그 갱신 | `GET /api/catalog/status`, 관리자 `POST /api/catalog/refresh` | `catalog_refresh.py` |
| 수집 작업·재색인 | 관리자 `GET /api/admin/collection-jobs`, `POST /api/admin/reindex` | `catalog.py` |
| 행사·포스터 | `GET /api/events`, `GET /api/events/images/{post_id}/{image_index}` | `events.py` |
| 상품 파일 | `GET /api/media/{파일명}` | `main.py`의 StaticFiles |

파일명을 줄여 쓴 항목은 `backend/app/api/` 기준이다. API 세부 요청·응답은 서버를 실행한 뒤 `http://localhost:8000/docs`에서 확인할 수 있다. [API 소스](../../backend/app/api).

## 6. 데이터베이스 구성

상품 공통 정보는 `figures`에, 실제 판본·상품 식별자는 `figure_variants`에 둔다. 가격과 원문은 판본에 연결할 수 있어 같은 상품에 판본이 여럿인 경우를 표현한다. 검색 색인과 자동 분류 결과는 원문과 구분해 저장한다.

| 영역 | 주요 테이블 | 책임 및 관계 |
| --- | --- | --- |
| 카탈로그 | `manufacturers`, `product_lines`, `figures`, `figure_variants` | 제조사·라인·상품·판본, 공식 URL과 제목, JAN 등의 식별 정보 |
| 근거·자산 | `source_documents`, `product_images` | 판본에 연결된 자료 본문·URL과 상품 이미지 정보 |
| 공식 가격·환율 | `release_prices`, `exchange_rates` | 공식 엔화·국내 공식가와 환율 기준일·출처 |
| 판매처·기존 관측 | `retailers`, `seller_verifications`, `retail_price_records` | 판매처, 공식성 검증, 이전 방식 가격 관측 |
| 국내 판매 | `retailer_listings`, `retailer_offers` | 유통사 상품 식별·옵션·매칭 근거와 연결된 최신 가격·재고 |
| 중고 자료 | `used_marketplaces`, `used_listings` | 플랫폼·매물의 별도 모델 및 조회 경로 |
| 작업 이력 | `collection_jobs`, `search_runs` | 카탈로그·색인·의미 처리 작업의 상태와 검색 이력 |
| 분류 | `product_semantics` | 상품별 원문 해시, 추출 필드, 판정, 모델 및 검증 이슈 |
| 한국어 설명·문서 | `korean_profiles`, `korean_chunks` | 상품의 한국어 프로필, 분할 번역문과 현재 원문 일치 확인 |
| 계정·개인 저장 | `users`, `user_sessions`, `favorites`, `purchases` | 계정, 서버 세션, 사용자별 관심상품·구매 및 배송 상태 |
| 행사 연동 | `event_sources`, `source_posts`, `event_candidates`, `events`, `event_source_links` | 출처, 원본 공지, 구조화 후보, 보존용 행사 및 연결 모델 |

현재 공개 행사 API는 `event_candidates`와 `source_posts`를 조회하고 같은 행사 공지를 묶는다. `events`와 `event_source_links`도 스키마에 있으며, 공개 목록의 주 조회 경로는 후보 데이터 기반이다.

스키마 변경은 `backend/alembic/versions/`에서 관리한다. 소스상 최종 revision은 `20261116_retail_offers`다.

```text
cac17c89def2 (초기 카탈로그)
 → 20261021_personal (개인 기록·환율)
 → 20261023_korean (한국어 프로필·문서)
 → 20261110_semantics (원문과 분류 결과)
 → 20261110_users (계정·세션·소유권)
 → 20261112_instagram_events (행사 원본·후보)
 → 20261116_retail_offers (유통사 등록·가격)
```

모델 근거: [공통 엔터티](../../backend/app/models/entities.py), [국내 판매 모델](../../backend/app/models/retail.py), [의미 모델](../../backend/app/models/semantics.py), [한국어 모델](../../backend/app/models/korean.py), [행사 테이블](../../backend/app/integrations/instagram/store.py), [마이그레이션](../../backend/alembic/versions).

## 7. 제조사 데이터 수집과 반영

### 7.1 온라인 수집

1. `data/catalog_sources.json`에서 대상 목록과 허용된 회차 범위를 읽는다.
2. `backend/app/collectors/safe_http.py`에서 접근 정책·요청 간격·타임아웃 등을 확인하고 페이지를 받는다.
3. `backend/app/collectors/manufacturers/`의 어댑터가 상품명·제조사·판본·발매·가격·이미지·출처를 추출한다. 메가하우스·반다이·후류·세가·타이토·코토부키야·굿스마일·핫토이 어댑터가 있다.
4. `catalog_ingest.py`에서 기존 URL·상품 식별자·판본과 대조한 뒤 데이터와 후속 작업을 저장한다. 검색 인덱스 반영이나 추가 정보 보강의 미완료 작업은 후속 처리한다.
5. 의미 작업은 `semantic_queue.py`가 원문 버전으로 구분해 등록한다. 분류 결과를 저장할 때 현재 원문이 바뀌었으면 이전 결과로 새 작업을 종료하지 않는다.
6. 국내 유통사 단계가 활성화된 갱신 경로는 공식 수집 뒤 국내 4곳을 제한 범위로 확인한다.

`catalog_refresh.py`는 DB에 작업을 기록하고 중복 실행과 재요청 빈도를 관리한다. 현재 설정 파일에는 공통 페이지 한도 3개, 회차 신규 한도 60개, 국내 유통사별 한도 20개가 정의되어 있다. 출처 설정 및 개별 실행 명령에 따라 실제 처리량이 달라진다. 백엔드의 갱신 제한은 마지막 상태에 따라 성공 후 24시간, 그 외 1시간이다.

핫토이는 현재 수집 제외 정책이 적용된다. 어댑터와 과거 수집 자료는 이력에 남아 있다. 신규 제조사 일회성 수집 명령은 굿스마일도 범위에서 제외하며, 굿스마일 전용 수집 명령은 별도로 유지된다.

주요 코드: [수집·저장](../../backend/app/services/catalog_ingest.py), [카탈로그 갱신](../../backend/app/services/catalog_refresh.py), [제조사 어댑터](../../backend/app/collectors/manufacturers), [수집 정책](../../backend/app/services/collection_preferences.py), [신규 제조사 CLI](../../backend/scripts/collect_new_manufacturers.py), [굿스마일 CLI](../../backend/scripts/collect_goodsmile.py).

### 7.2 외부 파일 가져오기와 이미지

- 공통 진입점은 `scripts/import_bundle.py`다. `furyu`, `s_fire`, `taito`를 등록 정보에 따라 각 백엔드 모듈로 전달한다.
- `validate`는 입력 파일 구조를 검사하고, `preview`는 DB 대조 결과를 만들며, `commit`은 실제 저장과 후속 작업 등록을 수행한다.
- 수집 패키지와 결과 경로를 나눈다. 입력은 `data/imports/`, 가져오기 기록과 적용 전 백업은 `backups/imports/`에 둔다.
- 실제 상품 이미지와 카탈로그 이미지 URL을 연결한다. 이미지 정렬은 `backend/app/services/image_order.py`, 복원·재수집은 `backend/scripts/repair_assets.py`와 제조사별 도구가 담당한다.
- `tools/image_dedup/`은 이미지 중복 판별·숨김·복구를 지원한다. 이미지가 없거나 로드에 실패하면 프론트 컴포넌트가 빈 상태를 표시한다.

세부 처리: [공통 가져오기 구조](../PROJECT_STRUCTURE.md), [가져오기·대기열 통합](IMPORT_PIPELINE_20261110.md), [이미지 중복 도구](../../tools/image_dedup/README.md).

## 8. 국내 유통사 가격과 환율

| 유통사 코드 | 표시 이름 | 호스트 |
| --- | --- | --- |
| `maniahouse` | 매니아하우스 | maniahouse.co.kr |
| `herotime` | 히어로타임 | herotime.co.kr |
| `figurefarm` | 피규어팜 | figurefarm.net |
| `comics_art` | 코믹스아트 | comics-art.co.kr |

1. `backend/app/collectors/retailers/`에서 목록·상세의 상품 식별자와 URL, 옵션, 가격, 재고 상태를 추출한다. 전체 카탈로그 수집은 SQLite 체크포인트로 목록과 상세 처리 진행을 남긴다.
2. `retail_collection.py`가 유통사 상품을 `retailer_listings`, 최신 관측을 `retailer_offers`에 저장한다. 이전 관측이 나중에 도착했을 때 최신 값과 검증된 연결을 보호한다.
3. 유일한 유효 JAN과 제조사 일치, 스케일·판본 충돌 여부를 확인해 자동 연결한다. 특전·조건부 가격 등으로 확인이 부족한 기록은 미연결 관측으로 남긴다.
4. `domestic_prices.py`가 확인된 기존 관측과 새 판매 레코드를 모아 4개 유통사 행 및 대표 최저가를 계산한다. 기본 168시간 이내의 양수 원화 가격이며 판매 중·예약 가능 상태인 관측만 최저가 후보에 포함한다.
5. 화면은 최저가와 4개 행을 보여준다. 연결 가격이 없으면 `가격 없음`으로 표시한다. 품절·오래된 관측은 상태와 함께 표시할 수 있으며, 배송비는 별도로 확인한다.

공식 엔화 가격과 한국 공식가는 `release_prices`, 환율은 `exchange_rates`를 사용한다. 엔화 환산가는 JPY 가격에 환율을 곱한 참고 금액이다. 유통사 실판매가는 국내 가격 비교에서 따로 표시한다. 검토된 외부 판매 자료 가져오기 경로에서는 미등록 상품을 ETC로 추가한 이력이 있다.

주요 위치: [판매 저장·매칭](../../backend/app/services/retail_collection.py), [가격 집계](../../backend/app/services/domestic_prices.py), [호스트 수집 진입점](../../tools/collect_domestic_local.py), [전체 수집 CLI](../../backend/scripts/collect_domestic_catalog.py), [외부 수집 자료 가져오기](../../backend/scripts/import_direct_retail.py), [가격 컴포넌트](../../frontend/src/components/DomesticPrices.vue).

## 9. 상품명 번역·분류 파이프라인

```text
카탈로그 수집 또는 가져오기
  → CollectionJob에 상품 ID·원문 해시 등록
  → 대기 작업 읽기, 실패 보류 정책 적용
  → 사전 일치·한국어 원문·사전 조합 확인
  → 남은 상품명만 번역 모델에 전달
  → 사전으로 작품·캐릭터·형태 근거 확인
  → 미확인 필드만 분류 모델에 전달
  → 원문·필드 검증, 자동 게시 가능 필드 판정
  → 결과와 근거 저장, 해당 원문 버전의 작업 상태 갱신
```

| 구분 | 사용 구성 | 책임 |
| --- | --- | --- |
| 번역 | `qwen3:8b` | 상품명 한국어 변환, 고유명사·제품명·판본 보존 |
| 분류 | `qwen3:1.7b` | 작품·캐릭터·피규어 형태 등 분류 후보 작성 |
| 사전 | `data/reference/semantic_dictionary/catalog.json` | 정확한 제목 대응, 작품·캐릭터 별칭, 문맥 기준 |
| 검증 | `semantic_rules.py`, `semantic_policy.py` | 원문 인용, 허용 분류 값, 확인·보류 여부 검사 |
| 저장 | `product_semantics.py`, `semantic_queue.py` | 최신 원문 확인, 필드별 결과·상태 반영, 수동 값 보호 |
| 실행 | `split_semantics_worker.py`, `tools/run_split_semantics.py` | 상품을 배치로 선택하고 번역·분류 단계별 실행 |

분리 파이프라인 버전은 `split-semantics-v6`다. 기본 배치 20건에 대해 번역 단계 뒤 분류 단계를 실행해 모델 전환 횟수를 줄인다. 단계 결과는 원문, 모델 지문, 사전, 프롬프트, 파이프라인 버전으로 구분한다. 모델은 로컬 Ollama 연결을 사용한다.

11월 17일 사전 작성 보고의 집계는 제목 번역 4,655개, 작품 규칙 1,135행, 기본 캐릭터 규칙 252행이다. 위키 작품 목록, 기존 승인 번역 및 문맥 규칙을 결합한다. 값이 충돌하는 항목과 원문이 다른 번역은 재사용에서 제외한다. 제목에 캐릭터가 여럿 나오거나 같은 이름이 여러 작품에 나오는 경우 원문의 관계와 작품 문맥을 확인한다.

| 상태 | 해석 |
| --- | --- |
| `ready` | 해당 결과의 필수 항목이 검증됨 |
| `partial` | 일부 필드만 확인돼 저장됨 |
| `review` | 원문 근거나 판정 확인이 더 필요함 |
| `waiting_retry` | 재시도 모드에서 실패 건 유예 상태 |
| `paused_failed` | 실패 건 건너뛰기 모드에서 남은 대기 건이 모두 해당 정책에 따라 보류됨 |
| `idle` | 조회된 대기 작업이 없음 |

11월 17일 호스트 작업은 `--skip-failed`로 실행했다. 이 옵션은 실패 기록이 있는 대기 상품을 이후 자동 처리에서 제외한다. DB의 작업, 원문 및 실패 보고서는 보존한다. `--ids`로 지정한 상품은 명시적으로 다시 시도할 수 있다. 옵션 없이 실행하는 방식의 기본 재시도 유예는 1시간이다.

상품 설명과 출처 문서 전체의 한국어 번역은 `backend/app/services/ko_translation.py`, `backend/scripts/korean_pipeline.py`의 별도 흐름이다. `O_DOCK_LOCAL_SEMANTICS/`에는 PyTorch·Transformers·PEFT를 사용하는 QLoRA 학습 실험, 데이터셋 생성, 어댑터 병합 및 평가 도구가 있다. 과거 실험 모델과 현재 분리 처리기의 기본 Qwen3 모델은 적용 경로가 다르다.

상세 위치: [파이프라인](../../backend/app/services/split_semantics.py), [작업자](../../backend/scripts/split_semantics_worker.py), [사전 생성](../../backend/scripts/build_semantic_dictionary.py), [사전 기반 분류 복구](../../backend/scripts/recover_dictionary_classifications.py), [분리 처리 보고](SPLIT_SEMANTICS_20261117.md), [위키 목록 반영](WIKIPEDIA_ANIME_REFERENCE_20261111.md), [모델 실험 문서](../../O_DOCK_LOCAL_SEMANTICS/README.md).

## 10. 검색과 AI 답변

| 경로 | 동작 | 파일 |
| --- | --- | --- |
| 목록·필터 | 검색어, 제조사, 작품 및 출시 조건 등을 SQL에 적용하고 목록·페이지 정보를 반환 | `repositories/figures.py` |
| 구조화 자연어 검색 | 문장에서 지원하는 검색 조건을 추출해 상품 조회에 적용 | `services/natural_search.py` |
| 한국어 근거 검색 | 정형 정보·원문·한국어 문서의 별도 Chroma 인덱스 조회 | `rag/ko_rag.py` |
| 상품별 AI 채팅 | 선택한 판본 중심 근거 검색 → 답변 생성 → 인용 확인 | `rag/graph.py`, `rag/citations.py`, `rag/prompts.py` |
| 색인 생성·갱신 | 메타데이터와 문서 청크, 출처 URL·범위 연결 | `backend/app/rag/store.py`, `backend/scripts/index.py`, `backend/scripts/wait_and_index.py` |

일반 색인은 `figure_metadata`와 `figure_documents`를 사용한다. 앞쪽은 상품·판본의 정형 정보, 뒤쪽은 문서별 청크를 저장한다. 코드의 기본 청크는 1,000자, 겹침은 200자다. 현재 소스의 일반 임베딩 기본값은 `hash`다. 한국어 RAG는 `odock_ko_<설정 지문>` 컬렉션과 별도 공급자 설정을 사용한다. 한국어 RAG의 코드 기본값은 `openai`이며 설정에 따라 `hash`로 실행할 수 있다.

상품 답변의 LangGraph 흐름은 자료 조회 후 답변을 만드는 구조다. 답변에는 실제 인용된 원문 정보가 붙는다. 생성 모델 설정이 없는 경우 상품의 정형 사양에 대한 기본 응답 경로가 있다. 이 채팅·검색 구성을 로컬 상품명 번역 모델과 구분한다.

짧게 표기한 `repositories/`, `services/`, `rag/`는 `backend/app/` 기준이다. [검색 색인](../../backend/app/rag/store.py), [한국어 검색](../../backend/app/rag/ko_rag.py), [상품 채팅 그래프](../../backend/app/rag/graph.py), [자연어 조건 처리](../../backend/app/services/natural_search.py).

## 11. 행사·SNS 수집과 화면

| 단계 | 처리 내용 | 파일 |
| --- | --- | --- |
| Instagram 접근 | 토큰 확인, Business Discovery 가용성 확인, 제한된 읽기 및 계정별 조회 | `integrations/instagram/client.py`, `probe.py`, `collector.py` |
| 공식 홈페이지 | 등록 출처의 공개 페이지 또는 API를 읽어 일정·장소·예약·원문 링크 추출 | `integrations/event_web/sources.py`, `client.py`, `adapters.py` |
| 행사 구조화 | 팝업·전시·콜라보 카페 등 판별, 날짜 및 장소 정규화, 제외·중복 기준 적용 | `integrations/instagram/events.py`, `event_identity.py` |
| 저장 | 플랫폼과 외부 게시물 ID로 원본 및 후보 갱신, 최초 수집일·출처 보존 | `integrations/instagram/store.py` |
| 공개 목록 | 같은 행사 공지를 병합, 한국 날짜 기준 상태 및 장소·검색 필터 적용 | `services/event_catalog.py`, `api/events.py` |
| 이미지 | Instagram API 미디어를 저장한 뒤 게시물·본문 일치를 확인해 제공. 홈페이지는 허용 호스트의 포스터 URL 활용 | `integrations/instagram/images.py`, `integrations/event_web/images.py`, `api/events.py` |
| 사용자 화면 | 행사 카드, 일정 상태, 검색·필터, 상세·이미지·원문 링크 | `frontend/src/views/EventsView.vue`, `frontend/src/components/EventPoster.vue` |

최초 수집 전에 끝난 행사는 제외한다. 이후 종료된 행사는 기존 공지와 함께 보관하면서 조회 시 상태를 갱신한다. 제목에서 전시가 명확하면 전시 판정을 우선한다. 여러 원본이 한 행사를 가리킬 때 작품·유형·기간·장소로 묶고 출처를 보존한다. 공개 목록은 조건에 맞는 후보를 바로 사용한다. 내부에 남아 있는 `PENDING_REVIEW` 상태값과 실제 사용자 화면의 공개 표시 흐름은 구분한다.

공식 홈페이지 대상에는 DUEX, Space Galleria, 애니메이트 코리아, 애니플러스, 팝콘D플레이, 대원미디어, G-STAR, AGF Korea가 있다. 등록 상태와 실제 수집 성공 여부는 다르다. 확인된 공식 사이트 수집과 Instagram은 회차별로 실행한다. 최신 저장된 Instagram 재실행 보고는 11월 16일 Meta의 `API access blocked` 응답과 새 저장 0건을 기록했다.

실행 근거: [Instagram 운영 안내](../../backend/app/integrations/instagram/README.md), [공식 홈페이지 운영 안내](../../backend/app/integrations/event_web/README.md), [행사 중복·종료 처리](EVENT_DEDUP_AND_LIFECYCLE_20261112.md), [출처별 수집 결과](OFFICIAL_EVENT_SOURCES_EXPANSION_20261112.md), [Instagram 접근 결과](INSTAGRAM_COLLECTION_ATTEMPT_20261116.md).

## 12. 프론트엔드 상세 구조

`frontend/src/main.js`가 Vue 앱, Pinia, Router와 공통 스타일을 연결한다. `App.vue`는 헤더·모바일 메뉴와 페이지 영역을 구성한다. 라우트별 화면은 동적 import로 로드된다.

| 경로 | 화면 파일 | 책임 |
| --- | --- | --- |
| `/` | `HomeView.vue` | 홈, 탐색 진입, 상품과 제조사 요약 |
| `/search` | `KoreanSearchView.vue` | 한국어 검색, 결과·근거 표시 |
| `/new` | `NewFiguresView.vue` | 신상품 탐색 |
| `/makers` | `MakersView.vue` | 제조사 목록 |
| `/franchises` | `FranchisesView.vue` | 작품별 상품 탐색 |
| `/figures` | `FigureListView.vue` | 전체 상품, 필터·정렬·페이지 이동 |
| `/figures/:id` | `FigureDetailView.vue` | 큰 대표 이미지, 썸네일과 상세 사진, 메타데이터, 관심·구매, 가격·원문 |
| `/prices/:id` | `PriceCompareView.vue` | 상품별 가격 비교 |
| `/chat/:id?` | `AIChatView.vue` | 상품 관련 질문·응답과 근거 |
| `/events` | `EventsView.vue` | 행사 조건 검색과 상세 |
| `/login` | `AccountView.vue` | 회원가입·로그인·계정 표시 |
| `/favorites` | `FavoritesView.vue` | 관심상품 목록 |
| `/purchases` | `PurchasesView.vue` | 구매 금액·상점·날짜·배송 상태 관리 |
| `/status` | `DataStatusView.vue` | 카탈로그 상태 및 관리자 작업 진입 |

`frontend/src/` 내부의 주요 공용 모듈은 다음과 같다.

| 위치 | 역할 |
| --- | --- |
| `services/api.js` | 공통 fetch, 응답·오류·타임아웃, 금액·날짜·URL 처리 |
| `services/catalog.js` | 신상품 요청, 주요 제조사 구분, 공식 가격과 환산가 표시 보조 |
| `services/accounts.js`, `services/admin.js` | 일반 계정 상태와 관리자 연결 |
| `services/semantics.js`, `services/figure_forms.json` | 분류 상태와 형태 표시 |
| `stores/archive.js` | 상태·제조사 조회, 비교 선택, 개인 기록 상태 연결 |
| `stores/favorites.js` | 계정별 관심상품 API 동기화 |
| `stores/chats.js` | 브라우저 저장소에 계정 범위의 대화 이력 관리 |
| `components/FigureCard.vue`, `HomeProductCard.vue` | 상품 이미지·이름·상태·관심 액션 |
| `components/DomesticPrices.vue`, `LocalPrices.vue` | 국내 4개 유통사 가격과 공식가·환산가 |
| `components/ComparisonPanel.vue` | 비교 UI, 키보드 닫기와 포커스 순환 |
| `components/KoreanName.vue`, `SourceList.vue` | 한국어 제목과 근거 출처 표시 |
| `design-system.css`, `white-theme.css`, `events.css`, `home-design.css`, `style.css` | 흰 바탕·스카이블루 포인트, 글꼴, 상태·반응형 스타일 |

최근 디자인은 상품 사진을 중심에 두고, 모바일 접이식 메뉴, 키보드 포커스, 이미지 오류 상태를 제공한다. 상세 가격에는 국내 대표 최저가와 4개 판매처 행을 배치한다. [라우트 정의](../../frontend/src/router/index.js), [상품 상세 화면](../../frontend/src/views/FigureDetailView.vue), [디자인 토큰](../../frontend/src/design-system.css), [UI 검증 결과](../design/unslop-final-report.md).

## 13. 인증·권한 경계

- 일반 계정은 서버의 `users`와 `user_sessions`를 이용한다. 비밀번호는 salt를 포함한 scrypt 해시로 저장하며 무작위 세션 토큰은 DB에서 SHA-256 해시로 보관한다.
- 일반 세션 쿠키 `odock_session`은 기본 7일, `HttpOnly`, `SameSite=Lax`, 경로 `/api`를 사용한다. HTTPS 환경의 Secure 옵션은 `AUTH_COOKIE_SECURE`로 제어한다.
- 관심상품과 구매 기록의 조회·저장·수정·삭제는 사용자 ID 범위에서 처리한다. 중복 관심상품은 상품·사용자 키를 기준으로 제어한다.
- 공용 카탈로그 운영 명령은 `X-Admin-Token`으로 서버의 `ADMIN_TOKEN`과 대조한다. 관리자 세션 확인 API 및 브라우저 탭 단위 `sessionStorage`를 사용한다. 일반 사용자 세션과 별도 인증 경로다. 기존 개인 데이터 호환을 위해 관리자 토큰이 유효하면 사용자 ID 1로 해석하는 경로가 남아 있다.
- `require_same_origin`을 적용한 쓰기 API는 Origin이 있는 경우 허용 목록과 비교한다. `/api/media/`를 제외한 API 응답에는 `Cache-Control: no-store`가 설정된다.

관리자 화면의 현재 중심 기능은 공용 카탈로그 상태와 갱신이다. 사용자 계정을 관리하는 별도 종합 관리 화면은 기존 보고에서 미구현 범위로 기록했다. [계정 소유권](USER_OWNERSHIP_20261110.md), [관리자 경계](ADMIN_BOUNDARY_20261110.md), [권한 코드](../../backend/app/core/security.py).

## 14. Docker 배치와 운영 파일

### 14.1 서비스·포트·저장소

| 서비스 | 역할 | 포트 또는 실행 조건 |
| --- | --- | --- |
| `frontend` | Nginx와 빌드된 Vue 앱 | 호스트 `127.0.0.1:8080` → 컨테이너 80 |
| `backend` | FastAPI·Uvicorn | 호스트 `127.0.0.1:8000` → 컨테이너 8000 |
| `postgres` | PostgreSQL 16 | 호스트 `127.0.0.1:5432` → 컨테이너 5432 |
| `chroma` | Chroma HTTP 서버 | Compose 네트워크의 `chroma:8000` |
| `init` | 마이그레이션 → seed → 초기 검색 인덱스 | 최초 설치용 1회성 단계 |
| `catalog-worker` | 제조사 갱신 스케줄러 | Compose 정의상 확인 간격 3,600초. 갱신 실행 자체는 저장된 제한 조건 적용 |
| `semantic-worker` | 분리 번역·분류 소비자 | `local-semantics` 프로필, 호스트 Ollama 연결, 보고서 `/app/media/split_semantics` |
| `translation-worker` | 이전 잔여 제목 번역·분류 명령 | `local-title-translation` 프로필, `/batch_reports` |
| `domestic-price-worker` | 국내 4곳 전체 카탈로그 수집 명령 | `domestic-prices` 프로필, `/retail-reports` |
| Ollama | 로컬 모델 제공 | 루트 Compose 외 구성. 호스트 `127.0.0.1:11434`, 컨테이너에서 `host.docker.internal:11434` |

| 저장 위치 | 데이터 | 연결 위치 |
| --- | --- | --- |
| `postgres_data` | 카탈로그·계정·가격·행사·작업 DB | PostgreSQL의 `/var/lib/postgresql/data` |
| `chroma_data` | 검색 인덱스 | Chroma 컨테이너의 `/data` |
| `media_data` | 이미지·컨테이너 기반 작업 파일 | 백엔드의 `/app/media` |
| 호스트 `data/` | 초기 입력·사전·참조 파일 | 백엔드의 `/data` 읽기 전용 연결 |
| 호스트 `data/private/` | 호스트 운영 결과, 명시적으로 연결한 작업 로그 | 회차별 경로 또는 컨테이너의 보고서 마운트 |
| Ollama `model_cache` | 로컬 모델 파일 | Ollama의 `/root/.ollama` |

11월 17일에는 로컬 CPU Ollama 컨테이너 `odock-ollama-cpu-20261117`와 호스트 Python 소비자를 사용했다. `O_DOCK_LOCAL_SEMANTICS/compose.yaml`에는 별도로 NVIDIA GPU를 사용하는 Ollama 서비스도 정의되어 있다. 호스트 작업과 Compose 작업을 같은 대기열에서 운영할 때는 번역·분류 소비자를 하나만 실행한다. 호스트의 파일 잠금과 컨테이너 media 볼륨의 파일 잠금은 위치가 다르다.

작업 재개 시 11월 17일의 보류 정책을 유지하려면 호스트 실행 명령에 `--skip-failed`가 필요하다. 현재 루트 Compose에 정의된 `semantic-worker`의 명령에는 해당 옵션이 들어 있지 않으며 보고서 위치도 다르다. [루트 Compose](../../docker-compose.yml), [모델 서비스 Compose](../../O_DOCK_LOCAL_SEMANTICS/compose.yaml).

### 14.2 환경 설정

루트 `.env`와 실행 시 주입된 환경변수를 사용한다. 아래에는 설정 이름과 용도만 기록했다.

| 구분 | 주요 환경변수 이름 | 용도 |
| --- | --- | --- |
| DB | `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `DATABASE_URL` | PostgreSQL 초기 계정·DB와 백엔드 접속 |
| 경로·인덱스 | `DATA_DIR`, `MEDIA_DIR`, `CHROMA_HOST`, `CHROMA_PORT`, `CHROMA_PATH` | 데이터·이미지와 검색 인덱스 위치 |
| 세션·권한 | `ADMIN_TOKEN`, `AUTH_COOKIE_SECURE`, `CORS_ORIGINS` | 관리자 검증, 세션 쿠키, 요청 Origin |
| 분리 모델 | `SEMANTIC_PROVIDER`, `SEMANTIC_BASE_URL`, `SEMANTIC_TRANSLATION_MODEL`, `SEMANTIC_CLASSIFICATION_MODEL`, `SEMANTIC_TIMEOUT` | 로컬 모델 주소와 역할별 모델 이름 |
| 일반 RAG·한국어 RAG | `EMBEDDING_PROVIDER`, `EMBEDDING_MODEL`, `EMBEDDING_API_KEY`, `KOREAN_RAG_EMBEDDING_PROVIDER`, `KOREAN_RAG_EMBEDDING_MODEL` | 인덱스에 사용할 임베딩 공급자와 모델 |
| 답변·외부 검색 | `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL`, `LLM_API_MODE`, `SEARCH_API_KEY` | 구성한 생성·검색 서비스 |
| 가격·수집 | `PRICE_MAX_AGE_HOURS`, `PRICE_CACHE_MINUTES`, `COLLECTION_DELAY_SECONDS`, `REQUEST_TIMEOUT` | 유효 가격 범위, 캐시, 접근 간격과 시간 제한 |
| Instagram | `META_APP_ID`, `META_APP_SECRET`, `META_ACCESS_TOKEN`, `META_IG_USER_ID`, `META_GRAPH_API_VERSION` | Meta 앱과 Instagram 계정, 토큰 및 API 버전 |

호스트 명령은 `tools/run_split_semantics.py` 자체에서 로컬 DB와 Ollama 주소를 구성한다. Docker의 백엔드는 Compose에 명시된 컨테이너 내부 주소와 경로를 이용한다. [백엔드 설정 선언](../../backend/app/core/config.py), [Instagram 설정 선언](../../backend/app/integrations/instagram/config.py).

## 15. 운영 명령과 문제 확인

### 15.1 명령 요약

프로젝트 루트 PowerShell 기준이다.

```powershell
# 기존 환경의 새 코드 적용, DB 마이그레이션, 웹/API 실행
powershell -ExecutionPolicy Bypass -File scripts/update.ps1

# 서비스 상태 및 API 응답 확인
docker compose -p figure-archive-ai ps
Invoke-RestMethod 'http://localhost:8000/api/health'

# 상품 의미 처리 상태 및 소량의 대기 작업 조회
docker compose -p figure-archive-ai exec -T backend python -m scripts.product_semantics status
docker compose -p figure-archive-ai exec -T backend python -m scripts.product_semantics pending --limit 5

# 실패 보류를 유지하는 호스트 소비자 시작
.\.venv\Scripts\python.exe -u tools/run_split_semantics.py --watch --skip-failed --limit 20 --report-dir data/private/semantics/split_queue_20261117

# 제조사 입력 묶음 검사
python scripts/import_bundle.py furyu validate

# 프로젝트 경로·문서 구조 확인
python tools/check_structure.py
```

`scripts/update.ps1`은 기존 `.env`를 사용해 PostgreSQL·Chroma를 준비하고 웹/API를 빌드한 뒤 Alembic을 적용한다. 기존 환경에서 데이터와 Docker 볼륨을 이어 쓰는 실행 경로다. 일반 종료는 `docker compose down` 또는 `scripts/stop.sh`를 사용한다. `down -v`는 DB·검색·미디어 볼륨을 삭제하는 명령이다. 기존 설치의 백업·이관은 DB, 이미지 파일, 검색 인덱스, 입력·보고서 경로를 각각 다룬다. [업데이트 스크립트](../../scripts/update.ps1), [운영 문서](../OPERATIONS.md).

### 15.2 점검 위치

| 현상 | 확인할 위치 |
| --- | --- |
| 브라우저가 열리지 않음 | Docker 엔진과 `frontend` 상태, `localhost:8080`, Nginx 프록시 |
| API·DB 응답 실패 | `docker compose ps`, `docker compose logs backend postgres`, `/api/health`, Alembic 적용 상태 |
| 상품 이미지 오류 | 브라우저의 이미지 요청 URL, `/api/media` 응답, 상품 이미지 DB 연결, 맞는 media 경로 |
| 검색 결과가 비어 있음 | 카탈로그 DB, Chroma 연결, 일반·한국어 인덱스 분리, 색인 작업 |
| 번역·분류 진행 정체 | `progress.json`, 실패 로그, 호스트 소비자 상태, PostgreSQL·Ollama 연결 |
| 실패 상품만 남음 | `skipped_failures.json`, `failures.json`, `paused_failed`, 선택·보류 건수 |
| 가격 표 일부가 비어 있음 | 해당 판본 연결 여부, 판매처 관측 상태·시각, 조건부 가격 및 DB 매칭 근거 |
| 행사 목록·이미지가 비어 있음 | 행사 API, 원본·후보 상태, 최초 수집일과 일정, 포스터 출처 및 이미지 경로 |
| 외부 원본 수집 실패 | 회차별 보고서, API 접근 상태, 대상별 요청 제한·공개 정책 |

Docker 중단 시 진행 중인 DB 작업과 모델 요청은 영향을 받는다. 저장된 DB 값과 단계별 캐시는 동일한 볼륨과 같은 보고서 경로를 쓸 때 재개에 활용된다. 호스트 소비자가 함께 종료된 경우 위 호스트 명령으로 다시 시작한다.

## 16. 검증 결과와 기준 시점

### 16.1 작성 당시 직접 확인

- `python tools/check_structure.py` 실행 결과, Python 소스 182개와 프론트 소스 42개를 검사했고 오류는 0개였다.
- 소스 트리에서 백엔드 테스트 파일 42개, 프론트 `*.test.js` 파일 8개를 확인했다. 파일 수와 테스트 케이스 수는 집계 단위가 다르다.
- 11월 24일 Docker 상태 조회에서 Docker Desktop Linux 엔진의 파이프에 연결할 수 없었다. 이번 보고는 소스 정의를 확인했으며, 실시간 컨테이너 상태와 DB 건수는 확인이 제한됐다.

### 16.2 마지막으로 남아 있는 작업 결과

| 시점 | 항목 | 기록 |
| --- | --- | --- |
| 11월 16일 Good Smile 수집 | 신규 상품 | 요청 회차 500개 확보 |
| 11월 17일 공식 제조사 수집 | 신규 및 전체 | 신규 151개, 회차 반영 후 카탈로그 6,873개 |
| 11월 17일 국내 유통사 수집 | 가격 관측 및 연결 | 총 78건 관측, 기존 상품 연결 9건, 미연결 69건 |
| 11월 17일 15:38경 | 한글 상품명 값 있음 | 6,356개. 전체 카탈로그에서 한국어 값이 존재한 수치 |
| 11월 17일 17:02:21 KST | 분리 번역·분류 작업 파일 | 대기 103건 모두 실패 보류, 즉시 선택 0건, `paused_failed` |
| 11월 16일 Instagram 재실행 | 신규 SNS 원본·이미지 | API 접근 차단으로 신규 저장 0건 |

위 집계는 해당 회차의 원본 기록이다. 처리 보류나 부분 분류는 향후 재검사 대상이며, 전체 정확도는 독립 평가가 필요하다.

### 16.3 기존 회귀 검사 기록

| 범위 | 기록된 결과 | 자료 |
| --- | --- | --- |
| 분리 번역·분류 v6 | 관련 69개 통과 | [분리 번역·분류 보고](SPLIT_SEMANTICS_20261117.md) |
| 실패 보류 옵션 | 관련 테스트 21개 통과 | [실패 보류 변경 기록](SPLIT_SEMANTICS_20261117.md#실패-상품-자동-재시도-중지--1641) |
| 제조사·유통사 수집 | 관련 29개 통과 | [최근 수집 회차](COLLECTION_ROUND_20261117.md) |
| 최신 UI | Vitest 38개, 빌드 성공, 14개 화면에서 두 화면 폭 총 28조건 확인 | [UI 결과](../design/unslop-final-report.md) |
| 공식 행사 확장 | 당시 백엔드 294개 통과, 18개 건너뜀 | [행사 출처 확장](OFFICIAL_EVENT_SOURCES_EXPANSION_20261112.md) |

작성일에는 구조 검사와 파일·경로 확인을 수행했다. 위 회귀 검사는 각 기능 반영 당시 기록을 인용했다. PostgreSQL 통합 테스트의 별도 DB 설정 및 실행 명령은 루트 README를 참고한다. [테스트 안내](../../README.md#검증).

## 17. 유지보수 시 확인할 파일

| 변경하려는 부분 | 우선 확인할 위치 |
| --- | --- |
| 수집할 제조사·목록 | `data/catalog_sources.json`, `data/source_policy.json`, `collectors/manufacturers/` |
| 상품 메타데이터 수집·보강 | `catalog_ingest.py`, `enrichment.py`, 제조사 파서 |
| 새 제조사 파일 가져오기 | `data/imports/registry.json`, `scripts/import_bundle.py`, `backend/scripts/import_*_bundle.py` |
| 작품명·캐릭터·형태 | `backend/app/services/`의 기준 JSON·별칭·검증 파일, `build_semantic_dictionary.py` |
| 번역 모델·대기열·보류 처리 | `split_semantics.py`, `split_semantics_worker.py`, `semantic_queue.py`, `tools/run_split_semantics.py` |
| 가격 수집·최저가 | `collectors/retailers/`, `retail_collection.py`, `domestic_prices.py`, `DomesticPrices.vue` |
| 행사 출처·일정·이미지 | `integrations/event_web/`, `integrations/instagram/`, `event_catalog.py`, `EventsView.vue` |
| 로그인·개인 기록 | `api/accounts.py`, `api/personal.py`, `services/accounts.py`, `services/personal_records.py` |
| 디자인과 페이지 | `frontend/src/views/`, `components/`, `design-system.css` 및 라우터 |
| 설치·배포·마이그레이션 | `docker-compose.yml`, 두 Dockerfile, `scripts/update.ps1`, `backend/alembic/versions/` |

### 추가 자료

- 프로젝트의 실행과 문서 목차. [루트 README](../../README.md), [문서 폴더 안내](../README.md).
- 원본 수집·검증·저장 정책과 이전 폴더 이력. [데이터 출처](../DATA_SOURCES.md), [프로젝트 구조](../PROJECT_STRUCTURE.md), [외부 자료 출처 고지](../../THIRD_PARTY_NOTICES.md).
- 회차별 구현과 데이터 현황. [구현 현황 정리](O_DOCK_IMPLEMENTATION_SUMMARY_20261117.md), [분리 처리 보고](SPLIT_SEMANTICS_20261117.md), [최근 제조사·가격 수집](COLLECTION_ROUND_20261117.md).
- 현황 확인용 비공개 산출물. `data/private/semantics/split_queue_20261117/progress.json`, `data/private/manufacturers_20261117/final_verification.json`, `data/private/retail_price/20261117_round/verification.json`.
