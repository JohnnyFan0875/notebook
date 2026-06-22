# RAG

Retrieval-augmented generation (RAG) combines a language model with a retrieval step so the answer can use external knowledge instead of relying only on model parameters.

Key point: A useful RAG system is not just vector search plus an LLM. It is a pipeline that depends on document loading, chunking, embedding quality, retrieval strategy, and prompt grounding.

## Suggested Reading Order

1. [Embeddings and Semantic Search](embeddings-and-semantic-search.md): Start with what embeddings represent, how semantic search works, and where recommendations or zero-shot classification fit.
2. [Vector Databases for RAG](vector-databases.md): Then read indexes, metadata, querying, namespaces, batching, and the retrieval layer behind embeddings.
3. This page: Finish with the end-to-end RAG flow, prompt grounding, and vector-RAG limitations in one pass.

## Core Flow

```text
user question
↓
retrieve relevant context
↓
inject context into a prompt
↓
generate answer
↓
return grounded response or abstain
```

## Why Use It

| Goal | Why RAG Helps |
| --- | --- |
| Ground answers in documents | the model can use notes, policies, manuals, or knowledge bases |
| Reduce hallucination risk | answers depend less on parametric memory alone |
| Keep knowledge updatable | data can change without retraining the model |
| Improve domain fit | private or specialized content can be brought into the answer path |

## Main Components

| Component | Role |
| --- | --- |
| Document loader | reads source files such as PDFs, markdown, HTML, or code |
| Text splitter | breaks documents into retrievable chunks |
| Embedding model | turns chunks and queries into searchable vectors |
| Vector store or index | stores embeddings for retrieval |
| Retriever | fetches relevant chunks for a question |
| Prompt template | tells the LLM how to use context safely |
| Generator | produces the final answer |

## Loading and Splitting Documents

Good retrieval starts before embedding.

| Step | Why It Matters |
| --- | --- |
| Loading documents | preserves source content and metadata |
| Splitting text | keeps chunks small enough to retrieve precisely |
| Choosing split strategy | changes whether context is coherent or fragmented |
| Handling code separately | code often needs syntax-aware splitting instead of plain text splitting |

Tip: Chunking is a retrieval design decision, not a preprocessing detail. Bad chunk boundaries often lead to bad retrieval even when embeddings are good.

## Retriever Setup

A common practical pattern is:

1. load documents
2. split them into chunks
3. embed the chunks
4. store them in a vector index
5. expose a retriever with a search strategy such as similarity

Key point: Retrieval quality depends on more than `top_k`. It also depends on document coverage, metadata, chunk design, and whether similarity is the right search strategy.

## Prompt Grounding

Retrieved chunks only help if the generation prompt uses them well.

| Prompt Requirement | Why It Matters |
| --- | --- |
| Explicit use of context | keeps the model grounded in retrieved content |
| Clear answer constraints | reduces unsupported guessing |
| Behavior for missing evidence | lets the system say "I do not know" when needed |

Warning: If the prompt does not instruct the model to stay within retrieved context, a RAG system can still hallucinate confidently.

## Chain Construction

In orchestration frameworks such as LangChain, a RAG chain often maps:

1. question to retriever
2. retriever output to prompt context
3. prompt plus context to the model
4. model output to a final response parser

Tip: This chain structure is useful because each stage can be evaluated separately: retrieval quality, prompt behavior, and final answer quality.

## Typical Tooling Patterns

| Need | Common Choice |
| --- | --- |
| Local semantic retrieval | vector store such as `Chroma` |
| Prompt composition | prompt templates with explicit context slots |
| Lightweight chaining | declarative chain composition such as `LCEL` |
| Multi-format ingestion | document loaders for PDFs, code files, web pages, or markdown |

## Vector RAG Limitations

Vector search is powerful, but it is not universal.

| Limitation | Why It Happens |
| --- | --- |
| Weak long-range relationships | semantically similar chunks may miss structural dependencies |
| Fragmented context | relevant ideas may be split across chunks |
| Poor handling of graph-like relations | entity links and multi-hop reasoning may not surface from similarity alone |
| Overreliance on local similarity | the retriever may miss globally important context |

Key point: When retrieval requires relationships, workflows, or connected entities rather than isolated passages, plain vector RAG may be insufficient.

## When to Go Beyond Basic Vector RAG

You may need a richer design when:

1. answers depend on multi-hop reasoning across sources
2. entity relationships matter more than local semantic similarity
3. code or structured documents need type-aware splitting and retrieval
4. freshness, provenance, or ranking logic needs more control

## Minimum Checklist for a Healthy RAG System

Before calling a RAG system production-ready, you should be able to explain:

1. how documents are loaded and chunked
2. which embedding and retrieval strategy is used
3. how the prompt constrains generation to retrieved context
4. what the system does when evidence is weak or missing
5. where vector retrieval is likely to fail and how that risk is monitored
