import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File
from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_pages
from app.ingestion.store import add_chunks, search
from app.schemas import AskRequest
from app.rag.answers import answer_question

app = FastAPI(title="RAG Q&A Project")

@app.get("/health")
def health():
    return {"status": "ok"}
@app.post("/documents")
def documents(file: UploadFile = File(...)):
    doc_id = uuid.uuid4().hex[:8]
    os.makedirs("data", exist_ok=True)
    path = f"data/{doc_id}.pdf"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    pages = load_pdf(path)
    chunks = chunk_pages(pages, doc_id)
    add_chunks(chunks)
    return {"doc_id": doc_id, "pages": len(pages), "chunks": len(chunks)}


@app.get("/search")
def search_documents(q: str, k: int = 4, doc_id: str | None = None):
    return search(q, k, doc_id)
@app.post("/ask")
def ask(req: AskRequest):
    return answer_question(req.question, req.doc_id)