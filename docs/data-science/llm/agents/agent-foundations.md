# Agent Foundations

An LLM agent is a language-model-based system that can decide what to do next, use external tools or resources, and continue a task beyond a single response.

Key point: A chatbot only answers. An agent can answer, retrieve, filter, delegate, and act within a workflow.

## A Simple Definition

One useful working definition is that an AI agent can reason, plan, and act by interacting with its environment.

| Capability | Why It Matters |
| --- | --- |
| Reasoning | helps the system interpret the task and decide what information is missing |
| Planning | helps the system break work into steps rather than answering impulsively |
| Acting | lets the system call tools, retrieve data, or trigger workflow steps |

Tip: The strongest difference between a model and an agent is not "intelligence level." It is whether the system can keep moving through a task with state, decisions, and external interaction.

## From Chatbot to Agent

The most useful shift is not the framework name. It is the change in responsibilities.

| System Type | Typical Behavior |
| --- | --- |
| Plain chatbot | responds from prompt and built-in knowledge |
| Tool-using assistant | answers and calls external resources when needed |
| Agent | manages a task flow, uses tools, applies guardrails, and may collaborate with other agents |

One useful progression is:

1. welcome the user
2. answer common questions
3. follow safety guardrails
4. collaborate with other agents when tasks should be split

## Core Components of an Agent

Many agent designs can be reduced to a small set of building blocks.

| Component | Role |
| --- | --- |
| Model | interprets instructions, reasons about the task, and chooses the next step |
| Tools | connect the agent to external information or actions |
| Orchestration | manages sequencing, routing, state, and coordination across steps |

Key point: If one of these three components is weak, the overall agent becomes unreliable even if the language model itself is strong.

## Thought-Action-Observation Cycle

A common mental model for agents is a repeated cycle:

1. thought: decide what needs to happen next
2. action: call a tool or perform a step
3. observation: inspect the result and update the next decision

| Stage | Example in Support Workflow |
| --- | --- |
| Thought | "I need to understand this customer's situation." |
| Action | access the customer database and retrieve subscription history |
| Observation | see that the customer renewed a premium plan three days ago |

Tip: This cycle is useful because it separates planning from acting. That makes failures easier to debug and workflows easier to evaluate.

## Why Agents Need Tools

Language models are flexible, but they are not all-knowing.

| Limitation | Why a Tool Helps |
| --- | --- |
| Stale or missing facts | retrieval or search can access newer information |
| Private business knowledge | internal FAQs or databases can provide controlled context |
| Exact calculation | calculators or code tools reduce arithmetic mistakes |
| Workflow actions | APIs let the system do more than generate text |

Key point: Tool use extends capability beyond built-in model knowledge and usually improves reliability for task-specific work.

## Common Tool Types

A practical agent often connects to a small set of external resources.

| Tool Type | Typical Example |
| --- | --- |
| Knowledge lookup | company FAQ database |
| Open-web information | web search |
| Deterministic computation | calculator |
| Domain action | internal business API or workflow system |

Tip: Tools should be added because they solve a concrete reliability or action gap, not just because the framework supports them.

## Common Types of Agent Thoughts

Agent behavior often includes several recurring reasoning patterns.

| Thought Type | Practical Use |
| --- | --- |
| Memory integration | reuse earlier user context when making the next decision |
| Self-reflection | revise an answer or approach after noticing a weakness |
| Goal-setting | identify missing information before acting |
| Prioritization | decide which step should happen first |

Warning: Exposing full chain-of-thought is not required for useful agent design. The main engineering goal is reliable behavior, traceability, and controllable workflow structure.

## Choosing the Right Tools

Tool choice should match the use case.

| Use Case | Likely Tool Needs |
| --- | --- |
| Customer support | FAQs, policy lookup, account or ticket systems |
| Financial assistance | calculators, rules, structured records, auditability |
| News agent | web retrieval, freshness checks, source selection |
| AI-assisted coding | code context, execution, file access, or documentation lookup |

Warning: More tools do not automatically make a better agent. Each added tool also adds failure modes, routing complexity, and evaluation burden.

## Reliable Answers with Tools

Tools matter most when answers should come from trusted resources instead of model memory alone.

| Support Task | Better Pattern |
| --- | --- |
| Greeting users | simple prompt behavior is usually enough |
| Answering company questions | retrieve from company data rather than relying only on the model |
| Following policy | combine prompts with explicit rules or safe lookup layers |

Key point: For support workflows, the main value of tools is not just capability. It is grounding.

## What Agents Are Good At

Agents are most useful when a task has multiple steps, context changes over time, or external information is required.

| Good Fit | Why It Fits |
| --- | --- |
| Multi-step support flows | the system may need lookup, response shaping, and escalation logic |
| Structured operational workflows | the agent can coordinate reasoning and actions across tools |
| Role-based decomposition | specialized agents can split planning, retrieval, and execution |

Agents are less compelling when:

1. the task is a single straightforward response
2. no external information or action is needed
3. the added orchestration cost outweighs the benefit

## Do You Really Need an Agent?

Not every AI workflow should become agentic.

| Good Criterion | Why It Points Toward an Agent |
| --- | --- |
| Complex decision-making | the workflow cannot be captured as one simple prompt |
| Heavy reliance on unstructured data | the system must interpret text, documents, or mixed context |
| Hard-to-maintain rules | static branching logic becomes brittle or expensive |
| Adaptive problem solving | the next step depends on what was discovered earlier |

Typical strong-fit examples include:

1. autonomous customer support systems
2. coding assistants that inspect codebases and propose or implement changes
3. deep research assistants that synthesize many sources

Key point: If the task is deterministic, narrow, and stable, traditional automation is often simpler and safer than an agent.

## The Power of Teamwork

Some workflows benefit from multiple agents with narrower responsibilities.

| Pattern | Benefit |
| --- | --- |
| Specialist agents | each agent can focus on one type of task or policy domain |
| Delegation | complex work can be broken into smaller subproblems |
| Coordination | one agent can route or supervise the work of others |

Tip: Use multi-agent designs only when specialization improves clarity, control, or maintainability. Otherwise, a single well-scoped agent is often simpler and safer.

## Guardrails and Human Intervention

Agents need explicit safety boundaries because they do more than generate text.

| Control | Example |
| --- | --- |
| Input relevance guardrail | redirect requests that do not belong to the agent's domain |
| Output PII filter | remove personal addresses or SSNs before sending a response |
| Output validation | check tone, format, or policy compliance before final delivery |
| Human intervention | require approval, escalation, or override for sensitive actions |

Warning: Always design for human intervention in high-impact workflows. Autonomy without escalation paths is usually a governance failure, not a product feature.

## Where a Toolkit Fits

Frameworks such as Google ADK are helpful because they reduce infrastructure work around defining agents and composing tool-using or multi-agent behavior.

| Framework Value | Practical Meaning |
| --- | --- |
| Agent definition | easier ways to declare agents and their roles |
| Tool integration | simpler connection to external functions |
| Multi-agent composition | support for collaboration patterns across agents |
| Infrastructure handling | less boilerplate for orchestration plumbing |

Warning: A toolkit can speed up implementation, but it does not choose the right workflow, tools, or governance model for you.

## Minimum Design Checklist

Before building an agent, you should be able to explain:

1. what task the agent is responsible for
2. which tool gaps exist in model-only behavior
3. what sources the agent is allowed to consult
4. when the agent should escalate, refuse, or delegate
5. whether a single agent is enough or specialization is justified
