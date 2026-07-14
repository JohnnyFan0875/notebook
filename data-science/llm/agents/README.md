# Agent Foundations

This module covers the basic ideas behind LLM agents: when an LLM should use tools, how an agent differs from a plain assistant, and why some workflows benefit from multiple specialized agents.

Key point: An agent is not just a model with a fancy prompt. It is an LLM-based system that can decide, act, use external resources, and continue a workflow under constraints.

## Suggested Reading Order

1. [Agent Foundations](agent-foundations.md): Start with the mental model for tool use, agent progression, and when agents are justified.
2. [LangGraph Agent Workflows](langgraph-agent-workflows.md): Then learn how state, nodes, conditional tool routing, and event streaming turn a tool-using agent into an inspectable workflow.
3. [Multi-Agent Patterns](multi-agent-patterns.md): Finish with graph workflows, conditional routing, and the swarm versus supervisor trade-off across multiple specialists.

## Focus of This Module

| Topic | Why It Matters |
| --- | --- |
| Tool use | A model needs external resources when its built-in knowledge is not enough |
| Stateful orchestration | Nodes, edges, and message state make agent behavior traceable |
| Workflow design | Good agents combine greeting, reasoning, retrieval, and policy handling coherently |
| Guardrails | Real systems need safety boundaries, not just helpfulness |
| Delegation | Multi-agent setups help when work should be split by role or expertise |

Tip: A simple tool-using agent is often better than a complex multi-agent system unless task decomposition is genuinely necessary.
