# 위키백과 작품명 참조 자료

한국어 위키백과의 일본 TV 애니메이션 목록 15개 하위 문서를 수집했다.
`catalog.json`에는 제목 632개와 명시적인 일본어 언어 연결 504개가 들어 있다.
숫자는 제목 기준이며, 시리즈·후속 시즌·표기 차이는 임의로 합치지 않는다.
목록 원문 자체에 영화·OVA 등이 섞여 있어 TV 방영 여부를 보증하는 자료로 사용하지 않는다.

- `00.html`~`14.html`: API에서 받은 목록 본문 스냅샷.
- `catalog.json`: 중복 제거 제목, 일본어 별칭, 고정 버전 출처와 SHA-256.
- 실행 사본: `backend/app/services/classification_wikipedia_anime.json`.
- 기존 검증 사전을 우선하고 겹치는 작품·별칭은 새 자동 규칙으로 덮어쓰지 않는다.
- 완전한 제목을 입력한 검색은 확인된 별칭으로 확장한다. 부분 제목은 기존 검색을 유지한다.
- 분류 워커의 참조 사전에 연결되며 기존 상품 DB의 분류값을 일괄 변경하지 않는다.

프로젝트 루트에서 `python scripts/import_wikipedia_anime.py`로 스냅샷을 재사용해 구성한다.
현재 위키 문서로 갱신하려면 `python scripts/import_wikipedia_anime.py --refresh`를 사용한다.
표준 라이브러리만 사용하며 DB 또는 모델 API에 접근하지 않는다.

출처와 이용 조건은 루트 `THIRD_PARTY_NOTICES.md` 참고. 원문 및 가공 자료: CC BY-SA 4.0.
