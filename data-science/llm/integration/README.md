# Integration

This module covers the practical layer between a model idea and a working development workflow.

Key point: In real projects, most effort is not spent "calling an LLM." It is spent choosing the right abstraction, preparing data, shaping inputs, evaluating outputs, and deciding when adaptation is worth the cost.

## Notes in This Module

| Note | Focus |
| --- | --- |
| [Choosing LLM Providers and Model Families](choosing-llm-providers-and-model-families.md) | provider differences, model tiers, long-context fit, selection tradeoffs, managed multi-provider platforms |
| [LLM API Patterns](llm-api-patterns.md) | messages and roles, conversation state, parameters, structured output, tool calling, retries, moderation, tokenization |
| [Hugging Face Hub and Pipelines](hugging-face-hub-and-pipelines.md) | model discovery, dataset access, and task-oriented inference workflows |
| [LangChain Application Orchestration](langchain-application-orchestration.md) | prompt composition, LCEL chaining, reusable runnables, and framework-level workflow design |
| [Multimodal Models](multimodal.md) | image / document / audio / video workflows with Hugging Face processors and API-based speech pipelines |
| [Fine-Tuning LLMs](fine-tuning.md) | prompt vs RAG vs fine-tune decision, training workflow, LoRA / QLoRA / PEFT, task-specific evaluation |

Tip: Frameworks such as LangChain are most useful when a workflow has several moving parts to compose. If the task is a single clean request, a direct API call is often simpler.

Tip: Prefer the simplest workable interface first. Move from high-level pipelines to lower-level customization only when you actually need more control.

[Back to LLM](../README.md)
