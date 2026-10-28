# Prompt Engineering

Prompt 是指定任務、context、限制與輸出格式的那一層。本篇先講通用的 prompt 結構與技巧（shot strategies、chain-of-thought、chaining），再講 chatbot 的 system prompt 與多輪設計，最後是可重用的設定（custom instructions、XML tags、custom GPTs）。

Key point: Prompt engineering 不是巧妙措辭，而是讓任務對模型清楚可讀，使回應相關、有結構、容易評估。

## Prompt Fundamentals

Prompt engineering is the practice of shaping instructions so the model can produce a useful answer with less ambiguity and less rework.

Key point: A strong prompt does not guarantee a strong system, but a weak prompt can break an otherwise capable model very quickly.

### What a Prompt Really Does

A prompt is not just a question. It is a task specification.

| Prompt Role | Why It Matters |
| --- | --- |
| define the task | tells the model what kind of job to perform |
| supply context | reduces ambiguity and missing assumptions |
| set constraints | narrows the allowed response space |
| shape the output | makes answers easier to use downstream |

### Traits of an Effective Prompt

Three basic traits show up repeatedly in good prompts.

| Trait | Practical Meaning |
| --- | --- |
| Clarity | include the relevant context so the model knows what you mean |
| Specificity | state the task and deliverable precisely |
| Open-endedness | leave enough room for reasoning when exploration is useful |

Tip: Specific prompts usually outperform vague ones, but over-constraining a creative task can also make the answer brittle or unnatural.

### Common Prompt Elements

A useful prompt often combines several pieces.

| Element | Purpose |
| --- | --- |
| Instructions | define the job to perform |
| Persona or role | steer tone, lens, or expertise |
| Context | provide background facts, source material, or intent |
| Output format | make the answer easier to parse or compare |
| Examples | show the model what a good answer looks like |

Example structure:

```text
Role: You are a careful teaching assistant.
Task: Summarize the following notes for a beginner.
Context: Focus on practical implications for product teams.
Output: Return 3 bullet points and 1 warning.
```

### Common Failure Modes

Poor prompts often fail for predictable reasons.

| Failure Mode | What It Looks Like |
| --- | --- |
| Ambiguity | the answer stays generic because the task is underspecified |
| Missing context | the model guesses facts or intent |
| Weak formatting | output is hard to reuse or compare |
| Overloaded prompt | too many goals are mixed into one instruction |

Warning: If the prompt asks for unsupported facts without grounding, the model may produce confident but inaccurate output.

### Persona and Personalization

Role-setting can be useful when it changes the response style or decision lens.

| Use of Persona | Why It Helps |
| --- | --- |
| teacher | simplify explanations and define assumptions |
| analyst | emphasize structured comparison |
| editor | focus on clarity and revision |
| domain expert | bias the response toward a specific frame |

Key point: Persona is most useful when it changes priorities or evaluation criteria. It is less useful as decoration.

### Formatting and Delimiters

Prompt formatting helps separate instructions from content.

| Formatting Choice | Benefit |
| --- | --- |
| Delimiters | mark where source text begins and ends |
| Headed sections | separate role, task, context, and output rules |
| Explicit schemas | make results easier to parse |
| Numbered steps | guide multi-step responses |

Tip: Delimiters are a small change with large practical value because they reduce confusion between instructions and input text.

### Zero-Shot, One-Shot, and Few-Shot Prompting

These patterns differ mainly in how many examples the model receives.

| Pattern | Best Use |
| --- | --- |
| Zero-shot | the task is simple or already familiar to the model |
| One-shot | one example is enough to define tone or structure |
| Few-shot | consistency matters and the pattern is not obvious |

The trade-off is simple: examples usually improve consistency, but they also consume prompt space and can anchor the model too narrowly.

### Chain-of-Thought and Stepwise Guidance

For some tasks, performance improves when the prompt encourages staged reasoning.

| Pattern | Practical Use |
| --- | --- |
| Step-by-step instruction | useful for analysis, planning, or calculations |
| Zero-shot chain prompting | ask the model to work through the task in stages |
| Example-driven reasoning | provide one or more worked examples |

Key point: Stepwise prompting is often valuable because it decomposes the task, not because it is a magic phrase.

### Chaining Prompts Across Steps

Some workflows are easier when one large prompt is split into several smaller ones.

| Stage | Example |
| --- | --- |
| extract | pull facts or themes from a document |
| transform | summarize, classify, or rewrite them |
| evaluate | check completeness, tone, or policy fit |

This makes it easier to inspect failures and swap one stage without rewriting the whole workflow.

### Iteration Matters

Prompt engineering is usually iterative.

1. draft an initial prompt
2. inspect where the output fails
3. add missing context or tighter output constraints
4. test again on varied inputs
5. keep the simpler version if it performs just as well

Tip: Good prompt iteration focuses on failure patterns, not on one lucky example that happened to work.

### Prompt Quality Checklist

Before calling a prompt "done," check:

1. is the task clear and singular
2. does the model have enough context to avoid guessing
3. is the expected output shape explicit
4. would one or two examples improve consistency
5. should this be one prompt or a chained workflow instead

## Chatbot Prompt Design

Chatbot prompt design is the practice of shaping multi-message interactions so a conversational system responds consistently across many user questions.

Key point: A chatbot is harder to prompt than a one-off task because the system must stay useful across unpredictable turns, not just answer one carefully prepared request.

### Why Chatbots Need More Prompt Discipline

Open-ended interaction creates more variation than single-shot generation.

| Challenge | Why It Matters |
| --- | --- |
| unpredictable user questions | the system must handle many input styles and intents |
| shifting context | later turns depend on earlier turns |
| inconsistent tone risk | the assistant may drift without clear guidance |
| policy ambiguity | unsafe or out-of-domain questions still appear |

Tip: Chatbot quality depends less on one perfect answer and more on whether the system stays coherent across many different turns.

### Message Roles as a Design Tool

Conversational systems usually separate messages by role.

| Role | Practical Purpose |
| --- | --- |
| system | define behavior, boundaries, tone, or domain expectations |
| user | provide the current request or new context |
| assistant | represent prior responses that shape ongoing interaction |

Key point: Role separation matters because chatbot behavior is influenced not only by the current question, but also by how the conversation state is framed.

### What a System Prompt Should Do

The system prompt is the most stable instruction layer in a chat workflow.

| System Prompt Job | Example |
| --- | --- |
| define role | "You are a customer-support assistant." |
| constrain scope | answer only within a business or product domain |
| guide tone | be concise, gentle, formal, or teaching-oriented |
| specify behavior on uncertainty | say when evidence is missing instead of guessing |

A good system prompt reduces drift without trying to encode every possible answer.

### Domain Scoping Matters

Chatbots often work better when their scope is explicit.

| Scoped Bot | Benefit |
| --- | --- |
| finance assistant | can focus on finance-related questions and style |
| customer service bot | can stay aligned with support workflows |
| study helper | can simplify explanations and reinforce learning goals |

Warning: If the system prompt defines a role but not a boundary, the chatbot may still answer out-of-domain questions with false confidence.

### Response Guidelines

A chatbot usually needs instructions about how to answer, not just what it is.

| Guideline Type | Why It Helps |
| --- | --- |
| length constraints | avoid overlong answers |
| tone rules | keep responses consistent |
| uncertainty handling | reduce unsupported invention |
| escalation behavior | signal when human help is needed |

Example: A finance chatbot may need to answer carefully, stay neutral, and avoid pretending to know real-time market events it cannot verify.

### Conditional Behavior in Prompts

Some chatbot instructions work best as simple rules.

| Conditional Rule | Purpose |
| --- | --- |
| if in-domain, answer directly | keep the assistant useful |
| if out-of-domain, redirect politely | preserve boundaries |
| if evidence is missing, say so | reduce hallucination |
| if user asks for unsafe content, refuse | enforce policy |

Tip: Conditional prompting is often more reliable than hoping the model will infer your policy from tone alone.

### Lack of Information Is a First-Class Case

Chatbots should be designed to handle unknowns well.

| Missing-Information Case | Desired Behavior |
| --- | --- |
| latest event outside model context | acknowledge uncertainty or use retrieval |
| private personal fact | state that the system does not know it |
| missing product details | ask for context or defer |

Key point: "I do not know" is a product feature in a chatbot, not a failure.

### Using Extra Information Well

Additional context can be added through the system message or later user turns.

| Added Context | Why It Helps |
| --- | --- |
| company service details | enables better support answers |
| policy excerpts | anchors responses to real rules |
| product descriptions | improves specificity |
| recent user history | keeps the conversation coherent |

This works best when the added material is clearly scoped and easy for the model to reference.

### Multi-Turn Memory and Prior Assistant Messages

Earlier turns influence later ones.

| Conversation Element | Why It Matters |
| --- | --- |
| prior user requests | reveal evolving intent |
| earlier assistant answers | shape consistency and continuity |
| stored constraints | keep preferences or policies active |
| unresolved questions | prevent abrupt topic loss |

A chatbot prompt design is therefore partly a state-design problem.

### Role-Playing Prompts

Role-playing can be especially useful in chat systems.

| Role Style | Practical Effect |
| --- | --- |
| gentle support agent | more empathetic user-facing answers |
| tutor | clearer educational scaffolding |
| domain expert | narrower, more specialized framing |

Tip: Role-playing is valuable when it changes the response policy or user experience, not merely the wording.

### A Practical Chatbot Prompt Checklist

When designing a chatbot prompt, make sure you can answer:

1. what domain the chatbot serves
2. what the system prompt says about tone and boundaries
3. how the bot behaves when it lacks information
4. how out-of-domain or unsafe requests are handled
5. what conversation history is retained and why

## Reusable Prompt Workflows

Once a ChatGPT workflow becomes repetitive, the main question is no longer "What prompt should I write?" It becomes "Which parts of this interaction should be reused, structured, or packaged?"

Key point: Intermediate ChatGPT use is mostly about reducing repeated setup. Good customization turns one-off prompting habits into reusable interaction patterns.

### Three Levels of Control

Not every preference belongs in the same place.

| Control Layer | Better Use |
| --- | --- |
| one prompt | solve one specific conversation or task |
| custom instructions | keep stable personal or workflow preferences across many conversations |
| custom GPT | package instructions, examples, knowledge, and capabilities into a reusable tool |

Tip: Start with a normal prompt first. Move to custom instructions or a custom GPT only when the setup repeats often enough to justify the extra structure.

### Prompt Versus Custom Instructions

A useful distinction is:

| Mechanism | Practical Meaning |
| --- | --- |
| prompt | preferences or constraints for one conversation |
| custom instructions | preferences that should persist across conversations |

Examples of prompt-level guidance:

1. summarize this article in 5 bullets
2. act as my interviewer for one mock session
3. rewrite this email in a more concise tone

Examples of custom-instruction guidance:

1. answer briefly unless I ask for depth
2. use a teaching style with practical examples
3. default to markdown tables when comparing options

Key point: If a preference applies every time, pushing it into the conversation repeatedly is usually unnecessary friction.

### Custom Instructions Improve Interaction Consistency

Custom instructions are useful when a user repeatedly wants the same style, audience framing, or response format.

| Persistent Preference | Why It Helps |
| --- | --- |
| response tone | reduces style drift across chats |
| preferred level of detail | avoids repeating "keep it short" or "go deeper" |
| domain background | lets the assistant tailor explanations more consistently |
| formatting habits | makes outputs easier to reuse |

Warning: Custom instructions are broad defaults, not hard guarantees. They should guide recurring behavior, not replace task-specific prompting.

### Simulation Prompts Can Turn Chat into Practice

One strong ChatGPT pattern is simulation-style prompting.

| Simulation Style | Example Use |
| --- | --- |
| mock interview | practice answers and receive coaching |
| negotiation scenario | simulate a manager or client conversation |
| teaching dialogue | ask the assistant to quiz, critique, and guide |
| role-play rehearsal | practice difficult conversations before a real meeting |

This is useful because the model can alternate between acting in the scenario and giving feedback on the user's response.

Tip: Simulation prompts work best when you define roles, stopping conditions, and the type of feedback expected after each turn.

### Multi-Role Prompts Need Clear Boundaries

Some useful prompts ask ChatGPT to perform more than one role in the same interaction.

| Role Pattern | Why It Works |
| --- | --- |
| actor plus coach | one role runs the scenario while another critiques it |
| interviewer plus evaluator | one role asks questions while another scores answers |
| manager plus mentor | one role applies pressure while another teaches improvements |

Key point: Multi-role prompting is easier to manage when the prompt explicitly says when each role should speak and what output each role should produce.

### XML Tags Help Structure Complex Prompts

When prompts become long or contain several kinds of information, explicit structure helps.

| Tag Purpose | Example Meaning |
| --- | --- |
| `<context>` | background information |
| `<task>` | the main job to perform |
| `<constraints>` | rules the answer must follow |
| `<output_format>` | required answer shape |

This makes the prompt easier for both humans and the model to parse.

Key point: XML-style markup is not magic syntax. Its value is organizational clarity.

### Structured Prompts Improve Reuse

Tagged prompts are especially helpful when the same prompt pattern is reused across many inputs.

| Benefit | Why It Matters |
| --- | --- |
| easier editing | one section can change without rewriting the whole prompt |
| clearer separation of concerns | context, task, and constraints do not blur together |
| better collaboration | teammates can inspect prompt parts more easily |
| easier templating | applications can fill different fields programmatically |

Tip: If a prompt keeps growing, add structure before adding more prose.

### Custom GPTs Package a Reusable Workflow

A custom GPT is useful when a repeated workflow needs more than persistent preferences.

| Custom GPT Element | Why It Matters |
| --- | --- |
| name and description | communicate the GPT's role clearly |
| instructions | define behavior, scope, and priorities |
| conversation starters | guide users into the intended workflow |
| knowledge files | provide reference material for repeated tasks |
| capabilities | enable the GPT to work with the tools it actually needs |

Key point: A custom GPT is best thought of as a packaged interaction design, not merely a saved prompt.

### When a Custom GPT Is Better Than a Repeated Chat

Custom GPTs become more valuable when:

1. the same role and behavior are reused by many people
2. the workflow depends on a recurring knowledge base
3. users benefit from guided starters instead of blank-chat prompting
4. the task needs a clear, branded, or constrained experience

They are less necessary when a normal prompt already solves the task without repeated setup.

### Testing Still Matters

Reusable ChatGPT setups should be tested like any other workflow design.

| Test Question | Why It Matters |
| --- | --- |
| does it stay within scope | prevents generic or drifting behavior |
| do the defaults help most tasks | avoids overfitting to one example |
| are instructions too broad or conflicting | reduces inconsistent output |
| do conversation starters lead users well | improves adoption and usability |

Warning: Reuse can scale both strengths and weaknesses. A bad prompt is annoying once; a bad reusable setup spreads the problem everywhere.

### A Practical Escalation Path

When a workflow becomes more complex, a useful progression is:

1. start with a one-off prompt
2. reuse the prompt as a template
3. move repeated defaults into custom instructions
4. package a stable workflow into a custom GPT

Key point: Each step increases structure. Do not jump to the most elaborate setup before repetition actually exists.

### Minimum Checklist

Before calling a ChatGPT workflow well customized, make sure you can explain:

1. which instructions belong to one prompt versus persistent defaults
2. whether simulation or role-play is adding real value
3. how complex prompts are being structured
4. when a custom GPT is justified instead of a normal chat
5. how the reusable setup is tested for drift, scope, and usability
