# 전 상품 로컬 번역·분류 실행

2026-11-11 16:20 KST에 **6,161개 전 상품**을 대상으로 처리를 시작했다. 이 문서는 시작 기록이며 완료 보고서가 아니다. 실행 상태는 아래 진행 파일을 확인한다.

- [실시간 진행 상태](../../O_DOCK_LOCAL_SEMANTICS/reports/full_catalog_20261111_1620/progress.json)
- [실행 설정·코드 해시·DB 백업 해시](../../O_DOCK_LOCAL_SEMANTICS/reports/full_catalog_20261111_1620/run_manifest.json)
- 상품별 원문·모델 결과·검증·이전 결과·저장 성공 여부: 같은 폴더의 `<상품ID>.json`
- 실행 전 DB 백업: `backups/semantics_full_20261111/database.dump` (6,924,777 bytes)
- 실행 코드 고정본: `backups/semantics_full_20261111/source/`

로컬 `odock-qwen3:8b-v2-experimental`을 GPU 한 개에서 순차 실행한다. 유료 API를 호출하지 않는다. 기존에 처리된 상품도 다시 검사한다. 기존 한국어 이름과 동일 원문의 수동 검수 override는 보존한다. 사전에 없는 이름이나 검증 실패 값을 추측으로 공개하지 않으며, 원시 모델 번역은 상품별 보고서에서 확인할 수 있다. 모든 상품을 시도하는 것과 모든 필드를 확정 번역·분류하는 것은 다르다.

`ready`는 모든 필드의 기계 검증 통과, `partial`은 일부 필드만 확인, `review`는 검수 필요 상태다. 모두 사람의 정확도 인증을 의미하지 않는다. 상품 단위 처리 오류는 `failed`로 보고서에 남는다. 공급자 연결 등 차단 오류에서는 작업이 중단될 수 있다.

Docker 작업 컨테이너 `odock-full-semantics-20261111`이 대화 종료와 독립적으로 계속 처리한다. 초반 22건의 DB 저장 성공과 GPU 모델 실행을 확인했다. 완료 전까지 수 시간이 필요할 수 있다. 처리 종료 시 `progress.json`의 `state`와 `counts.failed`를 함께 확인한다.

```powershell
Get-Content O_DOCK_LOCAL_SEMANTICS/reports/full_catalog_20261111_1620/progress.json
docker logs --tail 5 odock-full-semantics-20261111
docker inspect odock-full-semantics-20261111 --format '{{.State.Status}} {{.State.ExitCode}}'
```

작업이 중단된 경우 먼저 로그와 진행 파일을 확인한다. 종료된 컨테이너는 `docker start odock-full-semantics-20261111`로 같은 코드·설정·보고서에서 재개할 수 있다. 이미 같은 source·model로 저장된 상품은 보고서의 `committed`를 확인해 재추론하지 않는다. 실행 중인 컨테이너를 중복 실행하지 않는다.

실행 준비에서 전체 DB 백업과 재개·이전 결과 보존 회귀 테스트 4건을 통과했다. 새로운 공급자나 모델로 재처리하려면 별도 보고서 폴더를 사용해야 한다.
