"""RAG over knowledge/*.md: chunked by section, embedded, and searchable."""

import os
from pathlib import Path
from typing import Optional

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

CHROMA_PATH = os.environ.get("CHROMA_PATH", ".chroma")
KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"
EMBEDDING_FN = DefaultEmbeddingFunction()  # swap this line for BGE or any other EF
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection("plan_knowledge", embedding_function=EMBEDDING_FN)


def _parse(path: Path) -> tuple[dict, str]:
    _, front, body = path.read_text().split("---", 2)
    meta = dict(line.split(":", 1) for line in front.strip().splitlines())
    return {k.strip(): v.strip().strip('"') for k, v in meta.items()}, body.strip()


def _chunks() -> list[dict]:
    out = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        meta, body = _parse(path)
        title, *sections = body.split("\n## ")
        title = title.lstrip("# ").strip()
        for i, section in enumerate(sections):
            heading, _, text = section.partition("\n")
            heading = heading.strip()
            metadata = {**meta, "source": path.name, "section": heading}
            out.append({"id": f"{path.name}#{i}", "text": f"{title} - {heading}\n{text.strip()}", "metadata": metadata})
    return out


def ingest() -> int:
    global collection
    client.delete_collection("plan_knowledge")
    collection = client.get_or_create_collection("plan_knowledge", embedding_function=EMBEDDING_FN)
    chunks = _chunks()
    collection.add(ids=[c["id"] for c in chunks], documents=[c["text"] for c in chunks], metadatas=[c["metadata"] for c in chunks])
    return len(chunks)


if collection.count() == 0:
    ingest()


def search_plan_knowledge(query: str, plan_type: Optional[str] = None) -> list[dict]:
    """Search the plan-knowledge base: plan types, required fields, business
    rules, numeric limits, policies. Never use this to look up existing or
    created plans -- use the plan search/get tools for that.

    Args:
        query: The natural-language question to search for.
        plan_type: Narrow to DATA, VOICE, COMBO, or UNLIMITED if known.
    """
    where = {"status": "active"}
    if plan_type:
        where = {"$and": [where, {"plan_type": {"$in": [plan_type, "ALL"]}}]}
    result = collection.query(query_texts=[query], n_results=3, where=where)
    return [
        {"source": m["source"], "section": m["section"], "text": doc}
        for doc, m in zip(result["documents"][0], result["metadatas"][0])
    ]


if __name__ == "__main__":
    print(f"Ingested {ingest()} chunks into {CHROMA_PATH}")
