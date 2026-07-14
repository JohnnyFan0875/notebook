# Integration

This module covers the practical layer between a model idea and a working development workflow.

Key point: In real projects, most effort is not spent "calling an LLM." It is spent choosing the right abstraction, preparing data, shaping inputs, evaluating outputs, and deciding when adaptation is worth the cost.

## Notes in This Module

| Note | Focus |
| --- | --- |
| [Choosing LLM Providers and Model Families](choosing-llm-providers-and-model-families.md) | provider differences, model tiers, long-context fit, and selection tradeoffs |
| [Hugging Face Hub and Pipelines](hugging-face-hub-and-pipelines.md) | model discovery, dataset access, and task-oriented inference workflows |
| [Multimodal Models with Hugging Face](multimodal-models-with-hugging-face.md) | multimodal task discovery, processors, pipelines, and image-audio-video workflows in the HF ecosystem |
| [LangChain Application Orchestration](langchain-application-orchestration.md) | prompt composition, LCEL chaining, reusable runnables, and framework-level workflow design |
| [LLM Business Workflows](llm-business-workflows.md) | workflow-fit thinking, high-value use cases, and business augmentation patterns |
| [LLM Application Patterns](llm-application-patterns.md) | structured outputs, tool use, retries, moderation, and production-safe request handling |
| [LLM Workflows in Python](llm-workflows-in-python.md) | model interfaces, tokenization, fine-tuning workflow, and evaluation metrics |
| [Managed LLM Platforms](managed-llm-platforms.md) | multi-provider access, model onboarding, response handling, and runtime safeguards |
| [Microsoft Copilot Productivity Workflows](microsoft-copilot-productivity-workflows.md) | Microsoft 365 copilots, email and meeting summaries, prompt gallery, and enterprise governance concerns |
| [Multimodal OpenAI Workflows](multimodal-openai-workflows.md) | speech-to-text, translation, moderation, text-to-speech, and multi-step audio application design |
| [OpenAI API Workflows](openai-api-workflows.md) | request structure, conversation state, parameter choices, and API-oriented prompt patterns |

Tip: Frameworks such as LangChain are most useful when a workflow has several moving parts to compose. If the task is a single clean request, a direct API call is often simpler.

Tip: Prefer the simplest workable interface first. Move from high-level pipelines to lower-level customization only when you actually need more control.
