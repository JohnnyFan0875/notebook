# LLM API Patterns

從「呼叫一次 API」到「可上線的請求處理」：先是 chat API 的心智模型（messages、roles、conversation state、temperature、token usage），再是應用層的模式（structured output、tool calling、retry、moderation、guardrails），最後是在 Python 裡直接用模型與 tokenizer 時要注意的事。

## Chat API Basics

Working with an LLM API is not only about sending a prompt. It is about packaging instructions, context, conversation state, and output controls into a request that a downstream application can rely on.

Key point: An API call is a workflow boundary. Once a model is used inside code, the important question becomes how requests are structured, repeated, constrained, and measured.

### The API Mental Model

A chat-style LLM request usually includes:

1. a model choice
2. one or more messages or instruction blocks
3. optional control parameters
4. a returned response plus usage metadata

This matters because application behavior depends on the full request structure, not only the last user sentence.

### Single-Turn Versus Multi-Turn Use

Some jobs only need one request. Others depend on ongoing conversation state.

| Interaction Style | Better Fit |
| --- | --- |
| single-turn | summarization, rewriting, labeling, extraction, or one-off Q&A |
| multi-turn | tutoring, assistants, iterative drafting, or contextual follow-up |

Key point: Multi-turn behavior is not magic memory. It is the result of resending relevant conversation history as part of later requests.

### Roles as an Interface Contract

Chat-style APIs often separate messages by role.

| Role | Practical Job |
| --- | --- |
| system | define behavior, boundaries, tone, or policy |
| user | provide the current task or new context |
| assistant | preserve prior answers or provide example responses |

This is more than prompt formatting. It is a way to separate stable instructions from changing requests.

### What the System Layer Is Good For

The system layer is usually the right place for durable behavioral rules.

| System-Level Instruction | Why It Belongs Here |
| --- | --- |
| act as a finance study assistant | stable role definition |
| answer briefly and clearly | persistent tone guidance |
| do not guess when evidence is missing | recurring uncertainty policy |
| stay within a domain | reusable boundary control |

Warning: If you push all rules into ad hoc user prompts, behavior often becomes inconsistent across turns.

### Assistant Messages as Structured Examples

Prior assistant messages can do more than preserve conversation history. They can also act like examples.

| Use | Why It Helps |
| --- | --- |
| preserve earlier answers | keeps follow-up questions coherent |
| show desired answer style | creates a structured few-shot pattern |
| demonstrate formatting | improves consistency without restating rules each time |

Key point: Example conversations are often easier to maintain in message form than inside one giant prompt block.

### Common API-Friendly Text Tasks

Many early application wins come from text transformation jobs.

| Task | Typical Value |
| --- | --- |
| editing | update wording, tone, names, or structure |
| summarization | condense tickets, transcripts, or long notes |
| classification | assign labels or route work |
| drafting | create first-pass copy or product text |
| extraction | pull structured facts from unstructured text |

These tasks are useful because a human can usually review the result quickly.

### Prompt Iteration Still Matters in Code

Putting a prompt into an application does not make it stable automatically.

| Iteration Lever | Why It Helps |
| --- | --- |
| add clearer constraints | reduces output drift |
| specify categories explicitly | improves classification consistency |
| include examples | helps the model infer the right mapping |
| split tasks into steps | makes failures easier to diagnose |

Tip: If a request works only on one example, the API integration is not ready yet.

### Temperature and Output Control

API parameters often influence variation and response length.

| Control | Why It Matters |
| --- | --- |
| temperature | affects determinism versus variability |
| output-length limits | protect cost and improve boundedness |
| model choice | changes quality, latency, and capability |

Lower variability is often better for extraction, routing, or repeatable transformations. Higher variability can help brainstorming or copy generation, but it also raises evaluation pressure.

### Token Usage Is an Engineering Signal

Many APIs return usage information alongside the result.

| Signal | Why It Matters |
| --- | --- |
| input tokens | indicate prompt and context cost |
| output tokens | indicate response cost and verbosity |
| total tokens | help estimate latency and budget impact |

Key point: Token usage is not bookkeeping only. It helps reveal when prompts are bloated or workflows are carrying too much history.

### Conversation State Is a Design Choice

Applications decide what to keep in memory and what to drop.

| State Choice | Risk if Mishandled |
| --- | --- |
| keep too little history | follow-up answers lose context |
| keep too much history | cost rises and irrelevant context accumulates |
| keep unfiltered history | bad earlier turns can pollute later behavior |

This is why conversation design often requires pruning, summarizing, or resetting context deliberately.

### System Messages Can Reduce Misuse, Not Eliminate It

System instructions help constrain the assistant, especially in domain-bounded applications.

They are useful for:

1. narrowing the assistant to a study, support, or product role
2. encouraging refusal or caution outside scope
3. setting a consistent tone for repeated interactions

Warning: System messages are guardrails, not guarantees. High-risk systems still need stronger controls than prompt text alone.

### A Practical API Development Loop

A healthy workflow often looks like this:

1. start with one narrow task such as summarization or classification
2. write the smallest clear request that solves it
3. inspect output quality and token usage
4. add examples, constraints, or role instructions where failure patterns repeat
5. decide whether the task should stay single-turn or become conversational

Key point: Most reliable API integrations emerge from repeated tightening of task boundaries, not from one elaborate prompt written upfront.

### Minimum Checklist

Before calling an LLM API workflow healthy, make sure you can explain:

1. whether the task is single-turn or multi-turn
2. what belongs in system, user, and assistant messages
3. which parameters affect reliability, creativity, and cost
4. how token usage and conversation history are being controlled
5. what review step or guardrail exists for important outputs

## Application Patterns

An LLM becomes an application component when you stop asking only for free-form text and start requiring structured behavior, controlled failure handling, and safer integration with external logic.

Key point: A production-ready LLM call is usually more than a prompt. It includes output constraints, fallback logic, safety checks, and a clear way to connect model output to application code.

### Free-Form Output Is Often Not Enough

Natural language is easy for people to read, but hard for software to depend on.

| Requirement | Why It Matters |
| --- | --- |
| consistent field names | enables downstream parsing |
| predictable shape | reduces brittle glue code |
| explicit missing-data behavior | avoids unsafe assumptions |
| machine-readable output | supports routing, storage, and automation |

This is why many applications need structured outputs rather than prose alone.

### Structured Output Is a Core Pattern

One of the simplest application upgrades is to ask the model for a constrained structure.

| Structured Output Use | Typical Benefit |
| --- | --- |
| JSON-style extraction | convert unstructured text into usable records |
| labeled classification results | support routing and analytics |
| fixed response schemas | make validation and monitoring easier |
| nested objects | preserve richer detail without ambiguous formatting |

Key point: Structured output reduces ambiguity between what the model says and what the application needs.

### Tool or Function Calling Connects the Model to Code

Tool calling is useful when the model should decide which operation to trigger or which arguments to supply.

| Tool-Calling Role | Why It Helps |
| --- | --- |
| collect arguments in a known schema | makes invocation safer |
| choose among available functions | supports routing and delegation |
| separate reasoning from execution | keeps application logic explicit |
| support multi-step retrieval or action | enables richer workflows |

This pattern is especially helpful when the model should not invent business data but should instead request it from code or APIs.

### Good Tool Design Reduces Unsafe Assumptions

A model should not confidently fabricate missing arguments just to satisfy a function schema.

| Design Practice | Why It Helps |
| --- | --- |
| tell the model not to assume missing fields | encourages clarification |
| make required arguments explicit | reduces silent misuse |
| allow follow-up questions | improves data quality |
| validate arguments before execution | prevents bad calls from reaching real systems |

Warning: Tool calling is not safe merely because the output is structured. Bad arguments can still produce bad actions.

### Parallel Tool Use Can Be Valuable

Some systems benefit when several tool calls can be planned or requested together.

| Parallel Pattern | Why It Helps |
| --- | --- |
| multiple lookups in one turn | reduces latency from serial orchestration |
| separate retrieval targets | improves aggregation workflows |
| multi-entity extraction | supports richer responses from one request |

Use it when the orchestration layer can actually handle the parallelism cleanly.

### Production Error Handling Needs Categories

LLM applications fail in several distinct ways.

| Error Type | Typical Meaning |
| --- | --- |
| authentication error | credentials or access setup is wrong |
| bad request error | request structure or parameters are invalid |
| not found or model error | the requested model or endpoint is unavailable |
| connection error | network or service reachability failed |
| rate or resource limit error | usage exceeded current quotas or capacity |

Key point: Different error classes need different responses. A retry is helpful for transient failures, but not for malformed requests or invalid credentials.

### Retries Should Be Selective

Blind retries can waste time and money.

| Retry Principle | Why It Matters |
| --- | --- |
| retry transient failures | useful for unstable connections or temporary service pressure |
| back off exponentially | reduces repeated pressure during outage windows |
| stop after bounded attempts | avoids runaway loops |
| do not retry invalid requests unchanged | prevents repeated guaranteed failure |

Tip: Retry policy belongs to the application layer, not inside the prompt.

### Moderation Is a First-Class System Step

For many applications, moderation should be treated as part of request handling rather than as an optional afterthought.

| Moderation Use | Why It Helps |
| --- | --- |
| screen risky user input | reduces unsafe prompt handling |
| classify sensitive content | supports safer branching logic |
| detect policy-violating output candidates | adds protection before delivery |
| provide context-aware safety checks | avoids simplistic keyword-only filtering |

Key point: Moderation is most useful when it influences what the application does next, not only when it produces a label.

### Guardrails Need More Than One Layer

Prompt instructions help, but they are not enough on their own.

| Guardrail Layer | Example |
| --- | --- |
| system instructions | define role, limits, and refusal behavior |
| input limits | cap user input size or complexity |
| output limits | bound cost and reduce overgeneration |
| moderation checks | detect unsafe categories |
| postprocessing validation | reject malformed or risky structured output |

Warning: If a workflow is high-stakes, rely on several guardrail layers together.

### Token Limits Are Also a Safety and Cost Tool

Constraining input and output length is not only a performance choice.

| Limit Type | Why It Helps |
| --- | --- |
| shorter user input bounds | reduce abuse surface and prompt bloat |
| output token caps | control verbosity, latency, and cost |
| bounded context windows | reduce accidental carryover from irrelevant history |

This is one of the simplest ways to make an LLM workflow more predictable.

### A Healthy Application Loop

For many production patterns, the workflow looks like this:

1. validate the request shape
2. moderate or screen risky input if needed
3. choose whether the task needs prose, structured output, or tool calls
4. execute the request with bounded parameters
5. validate the response or tool arguments
6. retry only when the failure mode is transient
7. log the outcome for later debugging and evaluation

### Minimum Checklist

Before calling an LLM workflow application-ready, make sure you can explain:

1. whether the output must be free-form, structured, or tool-driven
2. how tool arguments are validated before execution
3. which error classes are retried and which are surfaced immediately
4. where moderation or safety checks happen in the request flow
5. how token and output limits are used to control risk, cost, and predictability

## Model Interfaces and Tokenization in Python

Python-based LLM work usually follows a repeatable path: choose a model interface, prepare text inputs, run inference, evaluate the outputs, and only then decide whether fine-tuning is justified.

Key point: A useful workflow is less about memorizing one library API and more about understanding which layer of abstraction you need for the task.

### Start with the Right Abstraction

Many LLM libraries expose both high-level task wrappers and lower-level model classes.

| Interface Style | Best Use | Tradeoff |
| --- | --- | --- |
| high-level pipeline | quick prototyping for summarization, classification, generation, or translation | faster setup but less control |
| lower-level model and tokenizer classes | custom preprocessing, training, or evaluation flows | more flexibility but more moving parts |

Tip: Start high-level when the task is standard. Drop lower only when you need custom batching, training, inspection, or output handling.

### The Basic Inference Flow

A practical Python workflow usually includes:

1. select a model suited to the task
2. load the tokenizer or input processor
3. convert raw text into model-ready tokens
4. run inference
5. decode or structure the output for downstream use

This framing matters because the model does not consume raw language directly. It consumes tokenized representations with sequence limits and formatting assumptions.

### Tokenization Is Part of the System

Tokenization is not just a preprocessing detail. It shapes cost, truncation behavior, and what information survives into the model.

| Tokenization Concern | Why It Matters |
| --- | --- |
| padding | allows variable-length inputs to be batched together |
| truncation | prevents overly long inputs from exceeding model limits |
| max length | affects both runtime cost and information loss |
| decoding cleanup | improves readability of generated outputs |

Warning: If you ignore truncation and sequence limits, the model may silently lose the exact context you cared about most.

### Model Cards and Task Fit

Before using a model, check what it was built for.

| Question | Why It Helps |
| --- | --- |
| Is this model generative or discriminative? | generation and classification have different output behavior |
| What data was it trained or adapted on? | domain mismatch often explains weak results |
| What task is it intended for? | translation, summarization, and sentiment models are not interchangeable |
| What are the context and resource limits? | hardware and latency shape practical viability |

Key point: "A model exists" does not mean it fits your task, data, or deployment budget.
