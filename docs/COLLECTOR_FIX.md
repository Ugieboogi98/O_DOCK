# 수집기 오류 수정

- Shopify 이미지 {width} / %7Bwidth%7D를 1200으로 치환.
- 이미지 링크 판별 시 query 전체가 아닌 URL path 확장자 검사. Pinterest 공유 링크 제외.
- 가격은 DB 원자적 upsert로 저장하여 동시 실행/반복 offer 중복 방지.
- 이미지 임시 파일은 실행별 고유 이름으로 생성하고 원자적으로 교체.
- 같은 버전 수집은 Docker 내 파일 잠금으로 직렬화.
- 비활성 소스는 SKIPPED, 이미 저장된 이미지는 images_already_saved로 표시.

관련 테스트 9개 통과 (기존 기능 6개 + URL/가격/동시 파일 저장 회귀 테스트 3개). 네트워크 403 문제는 이 수정의 대상이 아닙니다. 사용자 로그의 FileNotFoundError는 상세 traceback이 없어 원인을 확정하지 않았지만 기존 고정 .part 경로의 동시 실행 충돌을 제거했습니다.

적용: 실행 중인 수집 창에서 Ctrl+C → ZIP 내용을 기존 폴더에 덮어쓰기 → docker compose up -d --build --no-deps backend → docker compose exec backend python -m scripts.enrich

기존 DB와 media_data 볼륨은 지우지 않습니다. Docker로 실행하세요 (수집 파일 잠금은 Linux fcntl 사용).
