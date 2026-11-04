import chromadb
from chromadb.utils import embedding_functions
from app.config import settings

_client = chromadb.PersistentClient(path=settings.chroma_path)
_embedder = embedding_functions.DefaultEmbeddingFunction()
_collection = _client.get_or_create_collection(
    name="documents", embedding_function=_embedder
)