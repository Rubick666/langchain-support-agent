from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from app.core.chroma import chroma_client
from app.core.embeddings import embeddings
from app.core.config import settings

def ingest_document(file_path: str, collection_name: str = "support_docs"):
    """
    Load a text file, split it into chunks, embed them, and store in Chroma.
    """
    # 1. Load document
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()

    # 2. Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = text_splitter.split_documents(documents)

    # 3. Create/get Chroma collection
    # We use LangChain's Chroma wrapper which handles embeddings and storage
    vectorstore = Chroma(
        client=chroma_client,  # our persistent client
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=settings.chroma_persist_dir,
    )

    # 4. Add chunks to the collection
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    vectorstore.add_documents(documents=chunks, ids=ids)

    print(f"Ingested {len(chunks)} chunks from {file_path} into collection '{collection_name}'.")