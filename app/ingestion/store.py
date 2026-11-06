import chromadb
from chromadb.utils import embedding_functions
from app.config import settings

_client = chromadb.PersistentClient(path=settings.chroma_path)
_embedder = embedding_functions.DefaultEmbeddingFunction()
_collection = _client.get_or_create_collection(
    name="documents", embedding_function=_embedder
)
def add_chunks(chunks: list[dict])-> list[dict]:
    _collection.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks]
    )
def search(query: str, k: int = 4, doc_id: str | None = None) -> list[dict]:
    results=_collection.query(
        query_texts=[query],
        n_results=k,
        where={"doc_id": doc_id} if doc_id else None
    )
    hits=[]
    for text,meta,dist in zip(
        results["documents"][0],results["metadatas"][0],results["distances"][0]
    ):
        hits.append({"text": text, "page": meta["page"],
                     "doc_id": meta["doc_id"], "distance": dist})
    return hits
def count_chunks(doc_id: str) -> int:
    return len(_collection.get(where={"doc_id": doc_id})["ids"])

def delete_document(doc_id: str) -> None:
    _collection.delete(where={"doc_id": doc_id})