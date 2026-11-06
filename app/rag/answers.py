from pathlib import Path
from app.config import settings
from app.ingestion.store import search
from app.llm import chat

PROMPT_PATH=Path(__file__).parent.parent / "prompts" / "qa_system.txt"
SYSTEM_PROMPT=PROMPT_PATH.read_text(encoding="utf-8")

def build_context(hits: list[dict]) -> str:
    return "\n\n".join(
        f"[{i}] (page {h['page']}) {h['text']}"
        for i, h in enumerate(hits, start=1)
    )

def answer_question(question: str, doc_id: str | None = None) -> dict:
    hits = search(question, k=settings.top_k, doc_id=doc_id)
    if not hits:
        return {"answer": "No documents have been uploaded yet.", "sources": []}

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",
         "content": f"Context:\n{build_context(hits)}\n\nQuestion: {question}"},
    ]
    answer = chat(messages)

    sources = [
        {"id": i, "page": h["page"], "text": h["text"]}
        for i, h in enumerate(hits, start=1)
    ]
    return {"answer": answer, "sources": sources}