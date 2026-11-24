# O_DOCK Qwen3 8B v2 experimental

Status: evaluated, **not approved for automatic catalog publication**.

Base: Qwen/Qwen3-8B revision `b968826d9c46dd6066d109eabc6255188de91218`.
Adapter: `models/qwen3-8b-odock-v2`; continued from v1, 40 + 80 QLoRA steps.
Runtime tag: `odock-qwen3:8b-v2-experimental`, merged Q4_K_M GGUF.

Training data: 216 + 374 agent-curated synthetic examples including validation/test partitions. Human-reviewed independent gold: zero. Split manifests preserve provenance and SHA256 hashes. `reviewed: true` in these synthetic files means agent review, not a human rating.

Intended use: local translation/classification experiments, suggestions with original Japanese evidence and review. Missing names and low title coverage remain substantial. Model-only character precision regressed in the paired real-product evaluation. Do not replace a production model based on low training loss or development replay scores.

The source dictionary and conservative abstention rules contribute substantially to hybrid performance. Their corrections must not be attributed to the neural weights. Original raw proposals, normalized values, source evidence, hashes and post-output label adjudications are recorded separately.

The app's default provider, existing original model and catalog records were not replaced. Current working-tree service changes were tested in isolated containers; they were not redeployed to production.

See the [full evaluation report](../docs/reports/LOCAL_MODEL_TUNING_20261111.md) and [human review queue](../docs/reports/LOCAL_MODEL_TUNING_REVIEW_QUEUE_20261111.md) before further training or use.
