# Third-party notices

## Wikipedia anime reference supplement

`data/reference/wikipedia_anime/` 및
`backend/app/services/classification_wikipedia_anime.json`은 한국어 위키백과
[일본의 텔레비전 애니메이션 목록](https://ko.wikipedia.org/wiki/일본의_텔레비전_애니메이션_목록)과
그 하위 목록의 기여자들이 작성한 자료를 추출·중복 정리하고 언어 연결을 추가한 것입니다.
원문 HTML과 각 문서의 고정 버전 링크는 같은 디렉터리와 catalog.json에 보관합니다.
해당 자료와 변경분은 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 조건을 따릅니다.
일본어 별칭은 위키백과의 명시적인 언어 연결을 사용합니다.

프로젝트 구현은 Python/JavaScript 오픈소스 라이브러리를 사용합니다. 각 라이브러리의 라이선스는 해당 배포 패키지/저장소를 확인하세요.

- Vue / Vite / Pinia / Vue Router / Tailwind CSS / Lucide: 각 공식 저장소 및 설치 패키지
- FastAPI / SQLAlchemy / Alembic / LangChain / LangGraph / Chroma / psycopg / pypdf: 각 공식 저장소 및 설치 패키지
- PostgreSQL / Nginx: 컨테이너 이미지 내 고지
- SUIT Variable: [sun-typeface/SUIT](https://github.com/sun-typeface/SUIT), SIL Open Font License 1.1. 자체 제공 파일은 `frontend/public/fonts/SUIT-Variable.woff2`, 라이선스 전문은 `frontend/public/fonts/SUIT-LICENSE.txt`에 포함됩니다.

공식 제조사의 상호·제품명·원문 링크는 식별과 출처 표시 목적으로 포함되었습니다.
제품 사진과 원본 사이트 설명 전문은 재배포하지 않습니다.
사용자가 제공한 원본 요구사항 PDF는 해당 사용자의 프로젝트 자료이며 재배포 라이선스를 새로 부여하지 않습니다.
초기 데이터 스냅샷이 외부 사이트의 대량 수집·이미지 재사용 허가를 의미하지 않습니다.
