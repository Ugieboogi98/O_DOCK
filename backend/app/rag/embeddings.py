import hashlib, math, re
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from app.core.config import get_settings


class HashEmbeddings(Embeddings):
    """Keyless reproducible lexical baseline. NOT a multilingual semantic model."""

    dimensions = 384

    def embed_query(self, text):
        text = text.casefold()
        v = [0.0] * self.dimensions
        tokens = re.findall(r"\w+", text) + [
            text[i : i + 3] for i in range(max(0, len(text) - 2))
        ]
        for t in tokens:
            h = hashlib.sha256(t.encode()).digest()
            v[int.from_bytes(h[:4], "big") % self.dimensions] += 1 if h[4] % 2 else -1
        length = math.sqrt(sum(x * x for x in v)) or 1
        return [x / length for x in v]

    def embed_documents(self, texts):
        return [self.embed_query(x) for x in texts]


def embedding():
    s = get_settings()
    if s.embedding_provider == "hash":
        return HashEmbeddings()
    if not s.embedding_api_key:
        raise ValueError("EMBEDDING_KEY_MISSING")
    return OpenAIEmbeddings(
        api_key=s.embedding_api_key,
        base_url=s.embedding_base_url,
        model=s.embedding_model,
    )


def signature():
    s = get_settings()
    return (
        "hash-v1-384"
        if s.embedding_provider == "hash"
        else "openai:" + s.embedding_model
    )
