"""Portable Chroma export. Reindexing from JSON/SQL is normally preferable."""

import json, argparse
from pathlib import Path
from app.rag.store import collection
from app.rag.embeddings import signature

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="../data/vector_export.json")
    a = p.parse_args()
    data = {"embedding_signature": signature(), "collections": {}}
    for name in ["figure_metadata", "figure_documents"]:
        result = collection(name).get(include=["documents", "metadatas", "embeddings"])
        data["collections"][name] = {
            k: result[k].tolist() if hasattr(result[k], "tolist") else result[k]
            for k in ["ids", "documents", "metadatas", "embeddings"]
        }
    Path(a.out).write_text(json.dumps(data, ensure_ascii=False))
