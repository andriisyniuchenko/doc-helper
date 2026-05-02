# doc-helper

RAG-based assistant that answers questions about LangChain documentation.

## Stack

- **LangChain** — orchestration
- **Tavily** — documentation crawling
- **OpenSearch** — vector store
- **Ollama** — local LLM and embeddings
- **Streamlit** — chat UI
- **Docker** — containerized services

## Architecture

```
User question
    → embed with Ollama (nomic-embed-text)
    → search OpenSearch for relevant chunks
    → pass chunks + question to Ollama LLM
    → stream answer to Streamlit UI
```

## Setup

1. Clone the repo and create `.env` from `.env.example`:

```bash
cp .env.example .env
```

2. Add your Tavily API key to `.env` (get one at https://app.tavily.com):

```
TAVILY_API_KEY=your_key_here
```

3. Pull the required Ollama models:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

4. Start the services:

```bash
docker-compose up -d
```

5. Run ingestion to crawl and index LangChain docs:

```bash
python ingestion/ingest.py
```

6. Open the app at http://localhost:8501

## Configuration

All configuration is done via `.env`:

| Variable | Description |
|---|---|
| `TAVILY_API_KEY` | Tavily API key |
| `OPENSEARCH_URL` | OpenSearch connection URL |
| `OPENSEARCH_INDEX_NAME` | Name of the vector index |
| `OLLAMA_BASE_URL` | Ollama server URL |
| `LLM_MODEL` | Model used for answer generation |
| `EMBED_MODEL` | Model used for embeddings |