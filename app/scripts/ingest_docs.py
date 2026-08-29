import asyncio
import sys
from pathlib import Path

from app.services.document_ingestion import ingest_document

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.ingest_docs <file_path>")
        sys.exit(1)
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)
    ingest_document(str(file_path))