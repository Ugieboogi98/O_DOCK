# 2026-11-16 번역·분류 작업 재개

- Docker Desktop과 PostgreSQL·Chroma·Ollama·backend·frontend를 실행했다. DB와 기존 모델 볼륨을 유지했다.
- 이전 11월 13일 시험은 5건 중 번역 저장 2건, 검증 보류 3건이었다. 현재 미번역 제목 1,154건을 대상으로 작업을 시작했다.
- 로컬 `qwen3:8b`로 원문 전체를 번역하고 숫자·제품 코드·알려진 이름을 검사한 후 로컬 모델 대조를 통과한 제목만 저장한다. 대조는 동일 모델의 자기 점검이며 독립적인 사람 검수나 의미 정확도 인증은 아니다.
- 같은 작업에서 작품·캐릭터·형태의 빈 분류값을 보완한다. 기존 제목과 확정 분류는 덮어쓰지 않는다. 유료 API는 호출하지 않는다.
- 항목별 결과와 고정된 대상 목록을 보존해 중단 후 재실행할 수 있다. 완료된 한국어 제목은 건너뛰며, 검증 보류는 완료 번역과 별도 집계한다.

현재 작업은 `translation-worker` 서비스로 실행한다. 웹 서버용 healthcheck는 배치 작업에서 비활성화했다. 일반 사이트 실행만으로 자동 시작되지 않는 별도 프로필이다.

```powershell
docker compose --profile local-title-translation up -d --no-deps translation-worker
docker compose logs --tail 20 translation-worker
Get-Content data/private/semantics/20261116_remaining/progress.json -Encoding utf8
```

작업 컨테이너가 종료된 뒤 다시 시작하는 경우에도 같은 명령을 사용한다. Ollama·PostgreSQL이 먼저 실행 중이어야 한다. `progress.json`의 `state=completed`는 대상 전체 처리 시도가 끝났다는 뜻이며, `counts.translated`와 `counts.review`를 구분해 번역 완료 여부를 확인한다. 모델·서비스 장애 시 제한된 횟수만 자동 재시도하며 `blocked` 상태는 별도 확인이 필요하다.

새 수집 상품까지 새 배치를 실행하려면 `TITLE_TRANSLATION_REPORT_DIR`를 새로운 보고서 폴더로 지정하고 시작한다. 기존 배치는 대상 목록을 고정하므로 실행 도중 새 상품을 자동 추가하지 않는다.

핵심 저장·원문 누락·분류 보호 테스트 8개 통과. 작업 시작 후 실제 번역 저장도 확인했다. 이 보고서는 전체 번역 완료를 주장하지 않는다.
