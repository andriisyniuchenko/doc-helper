import os
from typing import Generator
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

load_dotenv()

_SYSTEM_PROMPT = """You are a LangChain documentation assistant.
Answer the user's question based solely on the provided context.
If the context does not contain enough information to answer, respond with:
"I don't have enough information in the documentation to answer this question."
Do not make up answers. Do not use any knowledge outside of the provided context."""

_prompt = ChatPromptTemplate.from_messages([
    ("system", _SYSTEM_PROMPT),
    ("human", "Context:\n{context}\n\nQuestion: {question}"),
])

_llm = ChatOllama(
    model=os.getenv("LLM_MODEL"),
    base_url=os.getenv("OLLAMA_BASE_URL"),
)

_chain = _prompt | _llm


def get_answer(question: str, docs: list[Document]) -> Generator:
    context = "\n\n".join(doc.page_content for doc in docs)
    return _chain.stream({"context": context, "question": question})