from langchain_ollama import OllamaEmbeddings

# Use default base URL from OLLAMA_HOST env var (set in docker-compose)
embeddings = OllamaEmbeddings(model="nomic-embed-text")