# Vector Databases for RAG

Vector databases store embeddings so a system can retrieve semantically similar records efficiently at query time.

Key point: In a RAG system, the vector database is not just storage. It is the retrieval layer that turns embeddings, metadata, and search settings into usable context for generation.

## What a Vector Index Does

A vector index usually serves several responsibilities at once.

| Responsibility | Practical Meaning |
| --- | --- |
| Store vectors | keep embeddings available for later search |
| Store metadata | attach source, tenant, type, tags, or other filters to each record |
| Serve retrieval queries | return similar records for an input vector |
| Support vector operations | fetch, upsert, delete, and inspect records |

Tip: A useful index stores both vector values and enough metadata to make retrieval controllable.

## Core Record Shape

A typical vector record includes:

1. an identifier
2. an embedding vector
3. metadata such as source, title, tenant, or content type
4. sometimes raw text or a reference to the original content

Key point: Metadata is what lets semantic retrieval become operational rather than purely approximate.

## Index Design Choices

Before ingesting vectors, a few design decisions matter.

| Decision | Why It Matters |
| --- | --- |
| Vector dimension | must match the embedding model output |
| Distance metric | changes how similarity is computed |
| Deployment model | affects scaling, cost, and operational overhead |
| Namespace or partition strategy | affects isolation, latency, and tenant boundaries |

## Serverless vs. Provisioned Thinking

Different vector platforms expose different infrastructure models, but the trade-off is usually similar.

| Model | Typical Strength | Typical Trade-off |
| --- | --- | --- |
| Serverless | simpler scaling and lower ops overhead | less explicit control over underlying resources |
| Provisioned or pod-based | more predictable tuning and resource control | more management overhead and capacity planning |

Tip: If your main goal is to ship a retrieval workflow quickly, lower-ops infrastructure is often the better default until performance constraints say otherwise.

## Fetching vs. Querying

These operations solve different problems.

| Operation | What It Does |
| --- | --- |
| Fetch | retrieve vectors directly by known IDs |
| Query | retrieve similar vectors for an input embedding |

Key point: Fetching is exact lookup. Querying is semantic retrieval.

## Query Behavior

Vector search is usually configured around a few common ideas.

| Setting | Why It Matters |
| --- | --- |
| `top_k` | controls how many records are returned |
| Distance metric | changes which records count as most similar |
| Namespace | limits search to a subset of the index |
| Metadata filter | narrows the candidate set before or during retrieval |

## Distance Metrics

Similarity depends on the metric used by the index.

| Metric | Typical Interpretation |
| --- | --- |
| Cosine similarity | compare direction more than raw magnitude |
| Dot product | useful when magnitude carries signal or model assumptions support it |
| Euclidean distance | compare direct geometric distance in vector space |

Warning: The right metric should match the embedding model assumptions. Switching metrics casually can degrade retrieval even if nothing else changes.

## Metadata Filtering

Metadata filtering is one of the most practical retrieval controls.

| Benefit | Why It Helps |
| --- | --- |
| Smaller search space | improves efficiency and often latency |
| Better relevance | avoids mixing unrelated document groups |
| Safer retrieval | enforces dataset, tenant, or policy boundaries |
| Better debugging | makes it easier to explain why certain records were eligible |

Common metadata values include strings, numbers, booleans, and simple lists.

Tip: Metadata filtering often improves results more cheaply than increasing `top_k` or changing models.

## Namespaces and Partitioning

Many vector stores support namespaces or similar partitioning mechanisms.

| Use Case | Why a Namespace Helps |
| --- | --- |
| Separate datasets | avoid mixing unrelated corpora |
| Data versioning | compare old and new embeddings safely |
| Multi-tenant isolation | keep different customers' data separate |
| Scoped retrieval | reduce latency by limiting search to a smaller slice |

Key point: Namespaces are not just organizational labels. They are part of retrieval design.

## Multitenancy Strategies

When one system serves many users or customers, isolation matters.

| Strategy | Strength | Trade-off |
| --- | --- | --- |
| Shared index with tenant metadata | simpler setup and less index sprawl | harder cost attribution and stricter filter discipline required |
| Shared index with namespaces | clearer isolation and lower search scope | still shares some infrastructure resources |
| Separate indexes per tenant | strongest isolation and custom control | highest operational overhead and cost |

Warning: If tenant isolation is a real requirement, do not rely only on application-layer assumptions. Make the storage and retrieval boundary explicit.

## Ingestion and Upserts

Vectors usually enter the index through upserts.

| Ingestion Concern | Why It Matters |
| --- | --- |
| Request rate | high-volume inserts can hit service limits |
| Request size | oversized payloads can fail or slow down ingestion |
| Batch design | affects throughput, retry behavior, and system stability |

Two common batching patterns are:

1. sequential batching: simpler but slower
2. parallel batching: faster but needs more careful error handling and rate-limit awareness

Tip: Batching is an ingestion control, not only a performance trick.

## Read Units and Cost Thinking

Managed vector systems often meter retrieval work using service-specific resource units.

| Cost Driver | Why It Changes Retrieval Cost |
| --- | --- |
| Number of records searched | larger candidate sets require more work |
| Record size | more metadata or payload can increase cost |
| Vector dimensionality | higher-dimensional search is heavier |
| Namespace scope | broader search usually costs more than narrower search |

Key point: Retrieval quality and retrieval cost are linked. Better filtering and partitioning can improve both relevance and efficiency.

## Semantic Search Pattern

A basic semantic search system usually works like this:

1. embed the documents
2. upsert embeddings plus metadata into the vector store
3. embed the user query
4. query the index for similar records
5. collect the returned documents and sources
6. build a prompt with retrieved context

This is the bridge from vector search into RAG.

## Prompt Assembly After Retrieval

The retrieved documents usually need to be turned into a grounded prompt.

| Prompt Step | Purpose |
| --- | --- |
| join retrieved chunks | provide the model with evidence |
| delimit chunks clearly | reduce context confusion |
| append the question | keep generation anchored to the user task |
| require answer-from-context behavior | reduce unsupported invention |

Warning: A strong vector database cannot compensate for weak prompt grounding after retrieval.

## Minimum Checklist for Vector Retrieval Design

Before calling a vector retrieval setup healthy, you should be able to explain:

1. what each record stores besides the embedding itself
2. which distance metric the index uses and why
3. how namespaces or filters constrain retrieval
4. how ingestion is batched and rate-limited
5. how retrieved records become grounded prompt context
