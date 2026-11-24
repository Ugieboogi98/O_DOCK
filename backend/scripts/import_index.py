import argparse, json
from app.rag.store import collection
from app.rag.embeddings import signature

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--file", default="../data/vector_export.json")
    a = p.parse_args()
    data = json.load(open(a.file, encoding="utf-8"))
    if data["embedding_signature"] != signature():
        raise SystemExit(
            "Embedding signature mismatch. Reindex using the selected model instead."
        )
    for name, rows in data["collections"].items():
        if name not in ["figure_metadata", "figure_documents"]:
            raise SystemExit("Unexpected collection")
        c = collection(name)
        for i in range(0, len(rows["ids"]), 64):
            c.upsert(**{key: vals[i : i + 64] for key, vals in rows.items()})
        print(name, c.count())
