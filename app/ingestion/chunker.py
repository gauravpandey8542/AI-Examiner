from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings

def chunk_pages(pages: list[dict], doc_id:str) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,chunk_overlap=settings.chunk_overlap
    )
    chunks = []
    for p in pages:
        for i, piece in enumerate(splitter.split_text(p["text"])):
            chunks.append({
                "id": f"{doc_id}-p{p['page']}-c{i}",
                "text": piece,
                "metadata": {"doc_id": doc_id,"page": p["page"]}
            })
    return chunks