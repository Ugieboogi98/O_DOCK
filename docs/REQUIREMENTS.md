> 초기 버전 설명입니다. 개인 컬렉션 v2 변경 사항은 README.md와 ../README.md가 우선합니다.

# 요구사항 대응표

구현 존재, 자동 테스트 통과, 실제 외부 서비스 검증 완료를 구분합니다.

| ID | 대응 위치 | 상태 / 증거 |
|---|---|---|
| F2001 | data/figures.json, scripts.seed | 실제 제품 114건·8개 제조사, 중복 0 |
| F2002 | rag/store.py, embeddings.py | 두 컬렉션 색인·upsert·재색인 검증. hash는 검증용, 의미 임베딩 API 설정 필요 |
| F2003 | prompts.QUERY_PROMPT, services/discovery.py | JSON 검색어 추출 코드와 모의 모델 통합 테스트. 실제 키 미검증 |
| F2004 | SELECT_PROMPT, SafeFetcher, discovery | 공식 선택 문서 강제 포함·검색 캐시 검증. 실제 외부 본문 수집은 권한·키 필요 |
| F2005 | store.chunks/index_variant | 설정 청킹·출처 메타데이터·이전 청크 삭제 검증 |
| F2006 | store.retrieve | 선택 메타데이터 포함·제품별 문서 필터·중복 제거 |
| F2007 | rag/graph.py | LangGraph retrieve/generate. 키 없는 조회와 모의 LLM 테스트 |
| F2008 | citations.py, SourceList.vue | 실제 인용만 표시, 잘못된 번호 거절 테스트 |
| F2009 | AIChatView.vue, stores/archive.js | 제품/버전별 대화 저장 구현. 브라우저 수동 검증 대기 |
| F2010 | prices.py, matching.py, PriceCompareView.vue | 사양 비교·출처·신품/중고 분리, 상태/통화/최신성 테스트 |
| F2011 | natural_search.py, FigureListView.vue | 높이·연도·스케일·제조사 등 SQL 조건 탐색 테스트. 범용 의미 조건 선별은 확장 대상 |
| F2012 | status API, 각 Vue 화면 | 로딩·오류·키 누락·색인 없음·모드 안내 구현 |
| F2013 | frontend/src, FastAPI OpenAPI | Vue SFC 6개 화면·별도 API, 프로덕션 빌드 통과 |
| F2014 | store.mmr_indices | MMR 다양성 선택 및 동일 제품 필터 테스트. 실제 임베딩 비교 평가는 대기 |
| F2015 | scripts/evaluate.py | 질문 5개 평가 실행 코드 제공. 실제 응답/사람 평가 점수는 미생성 |
| F2016 | scripts/import_document.py | PDF 페이지/TXT 원문 출처 지원. 사용자 허용 자료로 추가 검증 필요 |

## 비기능 요구사항

| ID | 구현 / 검증 |
|---|---|
| NF2001 | 각 답변 elapsed_ms 기록; 키 없는 실제 API 응답 예시 저장. 유료 LLM 전체 지연 미측정 |
| NF2002 | SearchRun 검색 캐시, idempotent seed/index, 중복 관측 제외 |
| NF2003 | .env.example만 제공, 실키 미포함, 서버 환경 변수 |
| NF2004 | 일반 응답에서 키/스택/프롬프트 비노출, 프런트는 텍스트로 답변 출력 |
| NF2005 | API / repositories / services / collectors / search_agents / rag 모듈 분리 |
| NF2006 | 정책·robots 검사, 호스트/경로 제한, 요청 간격, 제한된 재시도, User-Agent |
| NF2007 | 원문 URL·수집 시각·상태·이용 조건 기록. 자동 수집 및 이미지 권한은 미확보로 표시 |

초기 과제 규모는 충족하지만 실제 API 키와 자료 이용 권한이 없으므로 F2003~F2007의 실제 외부 서비스 전체 흐름을 완료했다고 평가하지 않았습니다.
원본 명세가 요구한 실행 화면 캡처와 동료 상호평가는 이 ZIP에 임의로 만들어 넣지 않았습니다.
