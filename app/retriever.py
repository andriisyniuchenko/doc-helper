import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import OpenSearchVectorSearch

load_dotenv()

_store = OpenSearchVectorSearch(
    opensearch_url=os.getenv("OPENSEARCH_URL"),
    index_name=os.getenv("OPENSEARCH_INDEX_NAME"),
    embedding_function=OllamaEmbeddings(
        model=os.getenv("EMBED_MODEL"),
        base_url=os.getenv("OLLAMA_BASE_URL"),
    ),
)


def get_relevant_docs(question: str, k: int = 5) -> list[Document]:
    return _store.similarity_search(question, k=k)