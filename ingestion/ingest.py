import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import OpenSearchVectorSearch

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENSEARCH_URL = os.getenv("OPENSEARCH_URL")
OPENSEARCH_INDEX_NAME = os.getenv("OPENSEARCH_INDEX_NAME")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
EMBED_MODEL = os.getenv("EMBED_MODEL")

CRAWL_URL = "https://python.langchain.com/docs/"
CRAWL_LIMIT = 50
CRAWL_MAX_DEPTH = 2


def crawl_docs():
    client = TavilyClient(api_key=TAVILY_API_KEY)
    response = client.crawl(
        CRAWL_URL,
        max_depth=CRAWL_MAX_DEPTH,
        limit=CRAWL_LIMIT,
        extract_depth="basic",
    )
    return response.get("results", [])


def to_documents(pages):
    docs = []
    for page in pages:
        content = page.get("raw_content") or page.get("content", "")
        if not content.strip():
            continue
        docs.append(Document(
            page_content=content,
            metadata={"source": page.get("url", ""), "title": page.get("title", "")},
        ))
    return docs


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs)


def store_in_opensearch(chunks):
    embeddings = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url=OLLAMA_BASE_URL,
    )
    OpenSearchVectorSearch.from_documents(
        chunks,
        embeddings,
        opensearch_url=OPENSEARCH_URL,
        index_name=OPENSEARCH_INDEX_NAME,
        engine="lucene",
        space_type="l2",
        bulk_size=500,
    )


if __name__ == "__main__":
    print("Crawling docs...")
    pages = crawl_docs()
    print(f"Crawled {len(pages)} pages")

    docs = to_documents(pages)
    print(f"Converted to {len(docs)} documents")

    chunks = split_documents(docs)
    print(f"Split into {len(chunks)} chunks")

    print("Storing in OpenSearch...")
    store_in_opensearch(chunks)
    print("Done")