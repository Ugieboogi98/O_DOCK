# 직접 확인할 미확정 분류

전체 6,161개 상품에서 미확정 필드를 6,356개 확인 그룹으로 묶었습니다.

| 문서 | 미확정 상품·필드 건수 |
|---|---:|
| [작품명](01_WORKS.md) | 1,380 |
| [캐릭터·대상](02_CHARACTERS.md) | 2,735 |
| [피규어 종류](03_FIGURE_TYPES.md) | 3,421 |

같은 그룹의 모든 상품에 해당하는 값만 승인하세요. 세트·복수 구성은 캐릭터를 배열로 적습니다.
원문과 근거가 바뀐 상품에는 이전 문서의 결정을 강제로 적용하지 않습니다.

작성 후 프로젝트 루트에서 검토용 패치를 만듭니다. 이 단계는 DB에 쓰지 않습니다.

```powershell
python O_DOCK_LOCAL_SEMANTICS/review_documents.py import --directory "docs/reviews/classification_20261111" --output O_DOCK_LOCAL_SEMANTICS/data/manual_classifications.json
```

생성한 패치는 아래 명령으로 미리 확인하고 반영합니다. 미리보기의 `failed`가 0인지 확인하세요. 재실행할 때는 보고서 파일명을 새 이름으로 바꿉니다.

```powershell
docker compose -p figure-archive-ai cp O_DOCK_LOCAL_SEMANTICS/data/manual_classifications.json backend:/tmp/manual_classifications.json
docker compose -p figure-archive-ai exec backend python -m scripts.apply_verified_classifications --input /tmp/manual_classifications.json --report /app/media/classification_research/manual_preview_01.json
docker compose -p figure-archive-ai exec backend python -m scripts.apply_verified_classifications --input /tmp/manual_classifications.json --report /app/media/classification_research/manual_commit_01.json --commit
```

같은 그룹에서도 서로 다른 답이 필요하면 일괄 승인하지 말고 상품 ID와 개별 답을 별도로 메모해 주세요. `manifest.json`의 상품 ID와 원문 해시는 변경하지 마세요. 문서를 재생성하여 직접 작성한 내용을 덮어쓰지 마세요.
