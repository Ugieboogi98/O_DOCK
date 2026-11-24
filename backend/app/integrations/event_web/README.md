# 공식 홈페이지 행사 수집

`sources.py`의 공식 홈페이지 8곳을 대상으로 공개 HTML/공개 카페 목록 API에서 행사 사실과 원문 링크를 추출한다. 기존 Instagram 수집기와 같은 행사 테이블을 사용하며 상품 테이블에는 쓰지 않는다.

## 실행

프로젝트 루트 PowerShell에서 실행한다. `.env`는 Docker Compose가 전달한다.

```powershell
docker compose run --rm --no-deps -v "${PWD}/data/private/events:/event-reports" backend python -m scripts.collect_official_events --report-dir /event-reports/<새로운_실행명> --cache-dir /event-reports/http-cache --commit
```

`--commit`을 생략하면 DB를 변경하지 않는다. `--sources duex aniplus`처럼 일부만 실행할 수 있다. 보고서 경로는 실행마다 새로운 이름을 사용한다. 이 명령은 일회성 수집이며 스케줄러를 켜지 않는다.

## 동작

- 출처별 robots.txt 검사, 호스트별 최소 1초 간격, 최대 3회 재시도, Retry-After 상한, 5 MB 응답 상한을 적용한다. 허용 목록 밖 URL과 리디렉션은 차단한다.
- 본문은 비공개 HTTP 캐시에 한 시간 보관 후 ETag/Last-Modified 조건부 재검증에 사용한다. 캐시는 자동 삭제되지 않으며 공개 API에서 제공하지 않는다. 공개 목록에는 홈페이지 본문 전문·방문자 댓글·이미지를 제공하지 않는다.
- 실제 행사 영역의 제목·일정·장소·예약 링크만 구조화한다. 예약 기간, 관람 회차와 방문자 댓글을 행사 운영 기간으로 사용하지 않는다.
- 출처의 재사용 권한은 수집 가능성과 별도이며 `FACTS_AND_LINK_ONLY`로 기록한다. robots 허용은 이미지나 본문 재게시 허가를 뜻하지 않는다.
- 행사 종료일이 최초 수집일(한국 날짜)보다 이전이면 신규 게시물을 저장하지 않는다. 이후 날짜가 지나 종료되는 기존 행사는 보존한다.
- 플랫폼+원문 ID로 재수집을 갱신하고, 작품·유형·기간·정규화 장소로 SNS와 홈페이지를 한 카드에 묶는다. 장소가 확인되지 않으면 추정으로 병합하지 않는다.
- 홈페이지 일정·장소 등 변경 전후는 후보 데이터의 `change_history`에 최대 20개 보존한다. 취소·연기는 제목에 명시된 경우만 반영하며 일반적인 취소 유의사항으로 판정하지 않는다. 이미지에만 적힌 변경은 자동 감지하지 않는다.
- 새 홈페이지의 날짜가 불명확하면 사용자 목록에서 제외하고 보고서에 원인을 기록한다. 관리자 검수함은 만들지 않는다.

## 실제 검증 범위 (2026-11-12)

DUEX·Space Galleria·애니메이트·애니플러스·팝콘D플레이·AGF에서 노출 가능한 구조화 행사를 확보했다. 대원미디어는 뉴스 접근·파싱에 성공했지만 해당 뉴스의 명시적 종료 일정이 없어 목록에 추가하지 않았다. G-STAR 상세 페이지는 robots.txt가 금지하여 비활성 상태다. X 계정은 API 권한·요금 미구성으로 수집하지 않으며 Popga/Popply는 참고 링크로만 남긴다.

실제 계정별 요청/오류/추출 건수는 `data/private/events/<실행명>/events.json`, 통합 검증 결과는 `docs/reports/OFFICIAL_EVENT_SOURCES_EXPANSION_20261112.md`를 참고한다.
