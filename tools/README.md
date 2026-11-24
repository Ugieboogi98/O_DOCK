# 독립 운영 도구

- `check_structure.py`: 현재 소스·문서·디렉터리 배치 검사. DB 접근 없음.
- `image_dedup/`: 이미지 중복 감사·숨김·복구. 사용법과 요구 패키지는 해당 디렉터리에 있다.

일상적인 앱 코드는 backend/frontend, 외부 입력은 data/imports, 실행 산출물과 백업은 backups에 둔다. 도구를 제조사별 최상위 폴더에 추가하지 않는다.
