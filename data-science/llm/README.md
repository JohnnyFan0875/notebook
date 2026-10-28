# LLM Applications and Systems

This section focuses on how large language models are used in practice: prompting, retrieval, tool use, agents, evaluation, and the system design choices around them.

Key point: Training a language model and building a useful LLM product are different problems. This section emphasizes workflows, components, and failure modes in real applications.

## Recommended Learning Path

1. [LLM Foundations](./llm-foundations.md): what an LLM is, how tokens, embeddings, transformers, and training stages fit together, plus generative-AI model families
2. [Prompt Engineering](./prompt-engineering.md): how task definition, context, examples, system prompts, and output constraints shape model behavior
3. [Integration](./integration/README.md): API patterns, structured output, tool calling, provider choice, multimodal workflows, and fine-tuning
4. [RAG](./rag/README.md): connect an LLM to external knowledge through retrieval
5. [Agents](./agents/README.md): what makes an agent different from a plain chatbot, and when tool use matters
6. [LLMOps](./llmops.md): version, test, deploy, monitor, and improve LLM applications and agent systems

Tip: Many LLM application errors are really system errors. The model may be fine, but the retrieval, tool design, prompt structure, or approval flow is weak.

## Modules

| Module | Core Topics | Main Questions |
| --- | --- | --- |
| [LLM Foundations](./llm-foundations.md) | tokens, embeddings, transformers, training, model families, and model limits | What is an LLM actually doing under the hood, and why does it fail in predictable ways? |
| [Prompt Engineering](./prompt-engineering.md) | task framing, examples, formatting, system prompts, reusable prompt setups | How do you make the model understand the job clearly enough to answer reliably? |
| [Integration](./integration/README.md) | API patterns, Hugging Face, LangChain, multimodal, fine-tuning | How do you turn model access into a usable development workflow? |
| [RAG](./rag/README.md) | embeddings, vector databases, retrieval, grounding | How can an LLM answer from documents instead of memory alone? |
| [Agents](./agents/README.md) | tool use, delegation, guardrails, and multi-agent patterns | When should an LLM act, call tools, or hand work to another agent? |
| [LLMOps](./llmops.md) | evaluation, deployment, monitoring, feedback loops, scaling agents | How do you keep an LLM application reliable after it leaves the prototype stage? |

## A Practical System Map

Useful LLM systems usually combine several layers:

| Layer | Typical Responsibility |
| --- | --- |
| Prompting | define the task, response shape, and constraints |
| Retrieval or tools | bring in external facts, APIs, or calculations |
| State | keep track of user context, workflow progress, or memory |
| Orchestration | decide which step, tool, or agent acts next |
| Guardrails | prevent unsafe, low-confidence, or off-policy behavior |
| Evaluation | check quality, reliability, latency, and business usefulness |

Warning: If you only evaluate model output quality and ignore latency, tool failure, stale context, or escalation behavior, the system can still fail in production.

[Back to Data Science](../README.md)
