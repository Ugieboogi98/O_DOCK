# 운영 안내

업데이트와 수집 명령은 ../README.md를 기준으로 합니다.

PostgreSQL 데이터는 postgres_data, 실제 이미지는 media_data 볼륨에 저장됩니다. 이 둘을 함께 백업하세요. `data/database.sql`은 최초 메타데이터 스냅샷이며 사용자 PC의 수집·구매·관심상품 데이터를 담지 않습니다. 기존 DB에 이 SQL을 덮어쓰지 마세요.

기존 사용자에게는 scripts/update.ps1만 실행하면 됩니다. `.env`는 유지하고 `.env.example`은 새 설치에만 사용합니다.

개인 사용 모드의 이미지는 personal_local 상태로 DB에 기록합니다. 이는 외부 재배포 허가를 의미하지 않습니다. 런타임 이미지와 실제 .env는 제공 ZIP에서 제외됩니다.
