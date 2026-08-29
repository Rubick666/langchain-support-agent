from langchain_chroma import Chroma

from app.core.chroma import chroma_client
from app.core.embeddings import embeddings
from app.core.config import settings

def get_retriever(collection_name: str = "support_docs", k: int = 4):
    """
    Return a retriever that fetches k most relevant chunks.
    """
    vectorstore = Chroma(
        client=chroma_client,
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=settings.chroma_persist_dir,
    )
    return vectorstore.as_retriever(search_kwargs={"k": k})