# Multi-Agent Patterns

Multi-agent systems split work across several specialized agents instead of forcing one agent to do everything.

Key point: A multi-agent design is useful when coordination and specialization improve the workflow more than the extra orchestration complexity hurts it.

## Why a Graph Mental Model Helps

Frameworks such as LangGraph popularize an important design idea: agent workflows are often easier to reason about as graphs.

| Graph Piece | Workflow Meaning |
| --- | --- |
| Node | a step such as an agent, tool call, or transformation |
| Edge | the path from one step to the next |
| Conditional edge | branching based on model output, tool need, or workflow state |
| State | the shared information carried across steps |

Tip: You do not need a graph framework to use graph thinking. The value is in making transitions and branching explicit.

## From Linear Flows to Conditional Flows

A simple agent pipeline can be too rigid.

| Pattern | Strength | Limitation |
| --- | --- | --- |
| Linear agent | easy to build and debug | every request follows the same path even when it should not |
| Conditional workflow | allows different branches by situation | needs clearer routing logic and state handling |

Example: A finance assistant should not call a stock tool for every question. Some requests only need explanation, while others need external data or computation.

## Tool Use as a Routing Decision

Many agent workflows become cleaner when tool usage is treated as a branch instead of a default action.

| Question | Design Implication |
| --- | --- |
| Does this request need external data? | route to a retrieval or API tool only when necessary |
| Does it require computation? | route to a code or calculator tool |
| Is plain explanation enough? | answer directly without extra steps |

Key point: Not every user query should trigger a tool call. Good orchestration often starts by deciding whether a tool is needed at all.

## Swarm Pattern

In a swarm-style system, multiple peer agents collaborate and can hand work across one another.

| Strength | Trade-off |
| --- | --- |
| flexible collaboration | harder to control the starting point and handoff logic |
| natural specialization | harder to predict who acts next |
| useful for open-ended tasks | debugging can become messy |

This pattern is attractive when several agents have distinct expertise, but it introduces two practical questions:

1. which agent should start
2. how agents coordinate without looping or duplicating work

## Supervisor Pattern

A supervisor design adds one coordinating layer that decides which specialist agent should act.

| Supervisor Role | Why It Helps |
| --- | --- |
| choose the next agent | makes routing explicit |
| hold shared task state | reduces scattered coordination |
| decide when to stop | avoids endless handoffs |
| enforce policy or escalation | improves control and safety |

Tip: If swarm collaboration feels too loose, a supervisor is often the simplest way to restore clarity.

## Comparing Swarm and Supervisor Designs

| Pattern | Better When | Main Risk |
| --- | --- | --- |
| Swarm | task ownership can shift naturally across specialists | coordination becomes implicit and unstable |
| Supervisor | routing needs to be explainable and controlled | the supervisor can become a bottleneck or single point of failure |

## State Matters More Than It First Appears

Multi-agent systems usually fail because the team cannot maintain a coherent shared state.

| State Need | Why It Matters |
| --- | --- |
| current objective | keeps all agents aligned on the same task |
| prior results | prevents repeated work |
| tool outputs | carries external evidence forward |
| stop conditions | prevents useless loops |

Warning: If agents share tools but do not share enough state, the system can look collaborative while actually behaving redundantly.

## When Multi-Agent Design Is Worth It

Multi-agent architecture is more justified when:

1. tasks divide naturally into distinct roles
2. different tools or policies apply to different subproblems
3. routing decisions must be explicit and inspectable
4. one generalist agent has become too hard to debug or extend

It is less justified when a single agent with good tools and clear branching can already solve the workflow.

## Minimum Checklist

Before adopting a multi-agent system, check:

1. which agents exist and why each one is separate
2. what state is shared across the workflow
3. how routing decisions are made
4. when tool use is triggered versus skipped
5. who decides the workflow is complete
