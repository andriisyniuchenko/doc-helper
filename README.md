# doc-helper

A local **2-Step RAG** documentation assistant that answers questions about LangChain. Built with LangChain, OpenSearch, Ollama, and Streamlit — everything runs locally, no OpenAI required.

The system crawls LangChain documentation, indexes it into a vector store, and uses a local LLM to generate answers based on retrieved context. Out-of-scope questions are correctly refused.

## Screenshots

**What is LangChain?**
![LangChain](assets/LangChain.png)

**What are deep agents?**
![Deep Agents](assets/DeepAgents.png)

**What is the weather in Tokyo?** *(out-of-scope — correctly refused)*
![Tokyo](assets/Tokyo.png)

## How it works

```
Ingestion (one-time):
  Tavily crawls python.langchain.com
      → RecursiveCharacterTextSplitter chunks the text
      → Ollama (nomic-embed-text) generates embeddings
      → Vectors + text stored in OpenSearch

Query (each request):
  User question
      → embedded with nomic-embed-text
      → OpenSearch kNN search returns top-5 relevant chunks
      → chunks + question passed to Ollama LLM (llama3.2:3b)
      → answer streamed to Streamlit UI
```

## Stack

| Layer | Technology |
|---|---|
| Orchestration | LangChain (LCEL) |
| Crawling | Tavily |
| Vector store | OpenSearch 3.6 |
| Embeddings | Ollama — nomic-embed-text |
| LLM | Ollama — llama3.2:3b |
| UI | Streamlit |
| Observability | LangSmith |
| Infrastructure | Docker, Docker Compose |

## Project structure

```
doc-helper/
├── app/
│   ├── main.py          # Streamlit UI
│   ├── retriever.py     # OpenSearch vector search
│   └── llm.py           # Ollama LLM chain
├── ingestion/
│   └── ingest.py        # Crawl → chunk → embed → store
├── docker-compose.yml
├── Dockerfile
├── Makefile
└── .env.example
```

## Requirements

- Docker
- [Ollama](https://ollama.com) installed natively (required for Apple Silicon GPU acceleration)
- Tavily API key — free at https://app.tavily.com
- LangSmith API key — free at https://smith.langchain.com

## Setup

1. Clone the repo and create `.env` from `.env.example`:

```bash
cp .env.example .env
```

2. Fill in the API keys in `.env`.

3. Pull the required Ollama models:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

4. Build and start the services:

```bash
make build && make up
```

5. Run ingestion to crawl and index LangChain docs:

```bash
make ingest
```

6. Open the app at http://localhost:8501

## Makefile commands

| Command | Description |
|---|---|
| `make build` | Build the app Docker image |
| `make up` | Start all services |
| `make down` | Stop all services |
| `make ingest` | Crawl and index LangChain docs |
| `make restart` | Restart the app container |
| `make logs` | Follow logs |
| `make clean` | Stop services and remove volumes |
| `make nuke` | Remove everything including Docker images |

## Configuration

| Variable | Description |
|---|---|
| `TAVILY_API_KEY` | Tavily API key |
| `LANGCHAIN_API_KEY` | LangSmith API key |
| `LANGCHAIN_PROJECT` | LangSmith project name |
| `OPENSEARCH_URL` | OpenSearch connection URL |
| `OPENSEARCH_INDEX_NAME` | Name of the vector index |
| `OLLAMA_BASE_URL` | Ollama server URL (`http://host.docker.internal:11434` for native Ollama) |
| `LLM_MODEL` | Model used for answer generation |
| `EMBED_MODEL` | Model used for embeddings |