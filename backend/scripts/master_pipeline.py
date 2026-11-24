"""Run the one-click data pipeline from a shell (same steps as the admin page button).

  docker compose -p figure-archive-ai exec backend python -m scripts.master_pipeline
  docker compose -p figure-archive-ai exec backend python -m scripts.master_pipeline --steps semantics verify
"""
import argparse
import json
from app.services import master_pipeline


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--steps', nargs='+', choices=master_pipeline.STEPS)
    a = p.parse_args()
    result = master_pipeline.start(a.steps, background=False)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['state'] in ('completed', 'partial') else 1


if __name__ == '__main__':
    raise SystemExit(main())
