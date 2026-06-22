# LLM Applications and Systems

This section focuses on how large language models are used in practice: prompting, retrieval, tool use, agents, evaluation, and the system design choices around them.

Key point: Training a language model and building a useful LLM product are different problems. This section emphasizes workflows, components, and failure modes in real applications.

## Recommended Learning Path

If you are learning these topics in sequence, this order usually works well:

1. model foundations: learn what an LLM is, how tokens, embeddings, transformers, and training stages fit together
2. prompting fundamentals: learn how task definition, context, examples, and output constraints shape model behavior
3. agent foundations: understand what makes an agent different from a plain chatbot, and when tool use matters
4. retrieval and grounding: learn how to connect an LLM to external knowledge through retrieval
5. operations and evaluation: learn how to version, test, deploy, monitor, and improve LLM applications
6. product integration: connect prompts, tools, state, and business workflows into a complete system

Tip: Many LLM application errors are really system errors. The model may be fine, but the retrieval, tool design, prompt structure, or approval flow is weak.

## Modules

| Module | Core Topics | Main Questions |
| --- | --- | --- |
| [Foundations](./foundations/README.md) | tokens, embeddings, transformers, training, and model limits | What is an LLM actually doing under the hood, and why does it fail in predictable ways? |
| [Prompting](./prompting/README.md) | task framing, examples, formatting, and prompt iteration | How do you make the model understand the job clearly enough to answer reliably? |
| [Agents](./agents/README.md) | tool use, delegation, guardrails, and multi-agent patterns | When should an LLM act, call tools, or hand work to another agent? |
| [RAG](./rag/README.md) | retrieval, grounding, and external knowledge access | How can an LLM answer from documents instead of memory alone? |
| [Operations](./operations/README.md) | evaluation, deployment, monitoring, and feedback loops | How do you keep an LLM application reliable after it leaves the prototype stage? |
| [Integration](./integration/README.md) | Python tooling, model interfaces, fine-tuning workflows, and evaluation choices | How do you turn model access into a usable development workflow? |

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
