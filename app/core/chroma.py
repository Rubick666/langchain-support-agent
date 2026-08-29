import chromadb
from app.core.config import settings
import os

os.environ["ANONYMIZED_TELEMETRY"] = "False"
# Persistent Chroma client (stores data on disk)
chroma_client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
