# RAG

Retrieval-augmented generation (RAG) combines a language model with a retrieval step so the answer can use external knowledge instead of relying only on model parameters.

## Core Flow

```text
user question
↓
embedding
↓
vector search
↓
similarity evaluation
↓
decision
├─ use retrieved context
├─ fallback to LLM only
└─ answer "unknown"
```

## Why Use It

- Ground answers in notes, documents, or knowledge bases.
- Reduce hallucination risk for domain-specific questions.
- Keep source data updatable without retraining the model.

## Main Components

- Embedding model
- Retriever
- Reranker or filter
- Generator
