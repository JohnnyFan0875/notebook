# LLMOps

LLM 應用上線後的營運面：prompt 版本管理、測試、部署、監控、feedback loop、成本控制；以及 agent 系統規模化時多出來的問題（routing、grounding、human-in-the-loop、tool failure、queueing）。一般 ML 的部署與監控見 [Deployment and Monitoring](../machine-learning/production/deployment-and-monitoring.md)。

## LLMOps Fundamentals

LLMOps is the operational practice of managing, testing, deploying, and improving LLM-based applications over time.

Key point: LLMOps extends MLOps, but it puts more emphasis on prompts, non-deterministic outputs, safety checks, feedback collection, and application-level observability.

### Why LLMOps Exists

LLM systems are difficult to operate because they combine model behavior with prompts, tools, retrieval, user context, and workflow state.

| Operational Challenge | Why It Matters |
| --- | --- |
| prompt changes alter behavior | small wording changes can cause large quality shifts |
| outputs are probabilistic | repeated runs may differ even with the same task |
| workflows are multi-component | failures can come from retrieval, tools, formatting, or orchestration |
| user input is open-ended | edge cases appear faster than in many traditional systems |

### LLMOps Versus MLOps

The two are related, but the center of gravity is different.

| Topic | LLMOps Emphasis | Traditional MLOps Emphasis |
| --- | --- | --- |
| behavior control | prompts, context assembly, retrieval, guardrails | feature pipelines and model weights |
| evaluation | output quality, factuality, safety, task completion | prediction metrics on labeled data |
| iteration unit | prompt, chain, tool policy, retrieval config | model retraining or feature updates |
| production risk | hallucination, prompt injection, tool misuse | drift, bias, calibration, service reliability |

### Prompt and Version Management

Operational discipline starts earlier than deployment.

| Practice | Why It Helps |
| --- | --- |
| version prompts | makes behavioral changes traceable |
| keep evaluation pairs | lets teams compare prompt revisions consistently |
| test in a playground first | speeds iteration before application rollout |
| separate dev and production configs | reduces accidental regressions |

Tip: Treat prompts as production assets, not informal text snippets copied between notebooks or chat windows.

### From Prompt to Application

A prompt can become an application once it is embedded in a larger workflow.

| Layer | Example |
| --- | --- |
| prompt logic | instructions, examples, output schema |
| augmentation | retrieval, examples, or tool outputs added at runtime |
| orchestration | chains, routing, retries, and fallbacks |
| interface | API, chat UI, or internal workflow integration |

Key point: Once an LLM is part of an application, the unit you test is the whole pipeline, not just the prompt text.

### Testing LLM Applications

LLM testing is less deterministic than traditional ML evaluation.

| Test Type | What It Checks |
| --- | --- |
| golden examples | whether core prompts still produce acceptable outputs |
| safety checks | whether the system refuses unsafe or off-policy requests |
| format checks | whether responses satisfy required schemas |
| workflow tests | whether retrieval, tools, and routing behave correctly together |

If human feedback is available, it can become a high-value evaluation signal. If not, teams still need proxy checks such as rubric-based review, constraint validation, or model-assisted judging.

Warning: A prompt that looks good on one demo example is not evidence that the application is ready for deployment.

### Deployment Thinking

Deploying an LLM application means deploying each important component, not just exposing one model endpoint.

| Component | Operational Concern |
| --- | --- |
| model access | hosting, latency, quotas, and fallback providers |
| retrieval layer | index freshness, permissions, and metadata quality |
| tool layer | API reliability, timeouts, and side-effect controls |
| application service | scaling, auth, logging, and release process |

A lightweight deployment lifecycle often includes:

1. build the application artifact
2. run deployment tests
3. release to a controlled environment
4. watch behavior closely after rollout

### Monitoring and Observability

Observability is what turns production use into learnable evidence.

| Signal | Why It Matters |
| --- | --- |
| input patterns | detect changing user behavior or prompt injection attempts |
| latency and failure rates | reveal system reliability problems |
| output quality metrics | track regressions against testing baselines |
| tool and retrieval traces | show where the workflow actually failed |

Tip: Observability should capture the whole path from user input to final answer, not only the last model response.

### Input, Functional, and Output Monitoring

Different failures show up in different layers.

| Monitoring Layer | What to Watch |
| --- | --- |
| Input monitoring | distribution shifts, malformed requests, suspicious prompt-like injections |
| Functional monitoring | tool failures, retrieval misses, broken chains, timeout behavior |
| Output monitoring | factuality, task completion, refusal quality, user satisfaction |

Data drift changes the inputs. Model drift shows up as changing output behavior relative to expectations. Both matter.

### Feedback Loops

A healthy LLMOps workflow keeps learning after launch.

| Feedback Source | Operational Use |
| --- | --- |
| human ratings | create labeled examples for future evaluation |
| support tickets | reveal failure modes users actually care about |
| trace review | identify weak prompts, bad routing, or stale retrieval |
| automated judges | provide scalable but imperfect review support |

Key point: Feedback is most useful when it is linked back to the exact prompt, config, and application version that produced the output.

### Cost and Performance Controls

Operational quality includes efficiency.

| Lever | Why It Helps |
| --- | --- |
| prompt compression | reduces token cost and latency |
| caching | avoids repeated work for repeated requests |
| smaller models for simpler tasks | lowers cost without sacrificing quality |
| retrieval and routing discipline | prevents unnecessary calls |

### Minimum Checklist

Before calling an LLM application operationally healthy, make sure you can explain:

1. how prompts and configs are versioned
2. which evaluation cases guard against regressions
3. what is deployed besides the model itself
4. which production signals are monitored
5. how feedback becomes the next round of improvements

## Operating Agent Systems

An agent that works in a demo is not automatically an agent that scales. Once an agent is expected to run repeatedly, call tools reliably, coordinate subagents, and survive real traffic, its operating design becomes part of the product.

Key point: Scalable agent systems depend less on one smart model and more on modular design, robustness under failure, and operational visibility.

### When Agent Scaling Becomes a Different Problem

A small agent prototype and a production agent system fail in different ways.

| Prototype Concern | Scaled-System Concern |
| --- | --- |
| can the workflow solve the task once | can it solve the task repeatedly under real conditions |
| does one tool call work | how do failures, retries, and fallback behave |
| is the prompt good enough | how are modules versioned, monitored, and improved |
| is one path coherent | how do routing and coordination stay maintainable |

Tip: The moment an agent needs multiple tools, longer runtime, or team ownership, you should start thinking like an operator rather than only a prompt designer.

### Three Pillars of Scalable Agent Design

Several practical concerns tend to reappear in scalable agent systems.

| Pillar | Why It Matters |
| --- | --- |
| modularity | makes parts easier to swap, test, and maintain in isolation |
| robustness | keeps the system useful when tools, data, or routing fail |
| adaptability | helps the system evolve as tasks, tools, and workloads change |

Key point: These pillars are linked. A system that is not modular is harder to make robust, and a system that is not robust becomes painful to adapt.

### Modularity Makes Maintenance Possible

Scalable agents should be decomposed into understandable responsibilities.

| Module Type | Practical Role |
| --- | --- |
| router or supervisor | decides which path or subagent should act |
| specialist agent | handles one narrower task well |
| tool interface | isolates external-system interaction |
| validation layer | checks outputs before the next step |

This matters because maintenance and evaluation become easier when each unit can be inspected separately.

### Routing Should Be Explicit

As agent systems grow, routing becomes architecture rather than implementation detail.

| Routing Pattern | Why It Helps |
| --- | --- |
| router agent | delegates subtasks explicitly |
| functional-area agents | split work by domain or role |
| workflow end conditions | prevent endless delegation loops |
| clear agent roles | reduce overlap and ambiguous responsibility |

Tip: If two agents appear to do almost the same job, the architecture is probably drifting toward maintenance trouble.

### Robustness Starts with Grounding and Verification

Agent systems break when they choose the wrong action, select the wrong tool, or act on weak context.

| Failure Mode | Better Design Response |
| --- | --- |
| erroneous tool use | verify whether the tool is needed before invocation |
| incorrect tool selection | constrain role and tool contracts more clearly |
| weak grounding | connect the agent to trusted data or retrieval |
| brittle outputs | add validation before continuing the workflow |

Key point: Robustness is not only about retries. It starts with reducing bad decisions upstream.

### Monitoring Needs to Be Agent-Aware

Generic application monitoring is not enough for agent systems.

| Monitoring Signal | Why It Matters |
| --- | --- |
| tool selection patterns | reveal misrouting and prompt drift |
| step-level latency | shows where orchestration is slowing down |
| failure and retry counts | expose fragile dependencies |
| completion outcomes | distinguish useful resolutions from stalled workflows |
| custom business metrics | tie agent behavior back to real operational value |

This is why custom monitoring is often needed once agents affect real workflows.

### Human-in-the-Loop Is an Operating Control

Human review is often part of scalability, not a sign that the system failed.

| Human Checkpoint | Why It Helps |
| --- | --- |
| approval for high-impact actions | reduces risk of unsafe side effects |
| review of large changes | protects systems that can alter many records or files |
| escalation for ambiguous cases | preserves service quality when confidence is weak |

Warning: Removing humans too early can make an agent look efficient while actually increasing downstream operational risk.

### Tool Failure Handling Needs More Than One Strategy

Agent systems should expect tool calls to fail sometimes.

| Failure Strategy | Better Fit |
| --- | --- |
| retry mechanism | transient API or infrastructure failures |
| verification checks | uncertain or suspicious tool-selection decisions |
| cached fallback | repeated queries where stale data is acceptable |
| queue management | workloads where failed calls can be retried later |

Tip: Cache fallback is useful only when freshness is not critical. It is a poor default for real-time tools.

### Queueing and Backpressure Are Real Agent Concerns

When many requests or tool calls arrive together, orchestration has to manage pressure.

| Queue Concern | Why It Matters |
| --- | --- |
| repeated failed calls | can consume resources without progress |
| overloaded tool layer | slows the whole system, not just one request |
| delayed retries | may be better than immediate repeated failure |
| ordering logic | affects fairness and perceived responsiveness |

Key point: Scaling an agent can mean scaling its waiting and recovery behavior, not just its model calls.

### Deployment Choices Affect the Architecture

Scalable agent systems are shaped by where they run.

| Deployment Choice | Why It Matters |
| --- | --- |
| hybrid deployment | balance local control with hosted capabilities |
| lower-latency infrastructure | matters when agents use several sequential steps |
| maintainable hosting model | affects updates, observability, and cost |
| real-time data access | supports coordination across multiple agents or services |

This matters because architecture decisions can either simplify or multiply later operating pain.

### Interoperability Becomes a Scaling Issue

Larger agent systems often need to work across teams, vendors, or tool stacks.

| Interoperability Need | Why It Helps |
| --- | --- |
| tool-stack agnostic design | reduces lock-in and integration friction |
| dynamic tool discovery | lowers the cost of adding new capabilities |
| multi-agent collaboration patterns | make specialized agents easier to combine |
| stable interfaces | preserve maintainability as the system grows |

Key point: A scalable agent should be extendable without rewriting the whole system each time a new tool appears.

### Testing Should Reflect Operational Reality

Agent evaluation should include more than output quality on one example.

| Test Focus | Why It Matters |
| --- | --- |
| speed and latency | agents often chain several slow operations |
| reliability under failure | reveals weak tool and retry behavior |
| tool-choice correctness | catches bad routing before production incidents |
| workflow completion | checks whether the system actually resolves tasks |

Tip: For agents, "correct answer" is often too narrow a metric. You also need to know whether the workflow behaved well.

### Minimum Checklist

Before calling an agent system operationally scalable, make sure you can explain:

1. how the system is modularized into agents, tools, and control layers
2. what makes the workflow robust when tool calls fail or routing goes wrong
3. which custom monitoring signals reveal real agent health
4. where human approval or escalation is still required
5. how deployment, queueing, caching, and interoperability affect the design
