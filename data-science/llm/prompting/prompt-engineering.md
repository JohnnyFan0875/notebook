# Prompt Engineering

Prompt engineering is the practice of shaping instructions so the model can produce a useful answer with less ambiguity and less rework.

Key point: A strong prompt does not guarantee a strong system, but a weak prompt can break an otherwise capable model very quickly.

## What a Prompt Really Does

A prompt is not just a question. It is a task specification.

| Prompt Role | Why It Matters |
| --- | --- |
| define the task | tells the model what kind of job to perform |
| supply context | reduces ambiguity and missing assumptions |
| set constraints | narrows the allowed response space |
| shape the output | makes answers easier to use downstream |

## Traits of an Effective Prompt

Three basic traits show up repeatedly in good prompts.

| Trait | Practical Meaning |
| --- | --- |
| Clarity | include the relevant context so the model knows what you mean |
| Specificity | state the task and deliverable precisely |
| Open-endedness | leave enough room for reasoning when exploration is useful |

Tip: Specific prompts usually outperform vague ones, but over-constraining a creative task can also make the answer brittle or unnatural.

## Common Prompt Elements

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

## Common Failure Modes

Poor prompts often fail for predictable reasons.

| Failure Mode | What It Looks Like |
| --- | --- |
| Ambiguity | the answer stays generic because the task is underspecified |
| Missing context | the model guesses facts or intent |
| Weak formatting | output is hard to reuse or compare |
| Overloaded prompt | too many goals are mixed into one instruction |

Warning: If the prompt asks for unsupported facts without grounding, the model may produce confident but inaccurate output.

## Persona and Personalization

Role-setting can be useful when it changes the response style or decision lens.

| Use of Persona | Why It Helps |
| --- | --- |
| teacher | simplify explanations and define assumptions |
| analyst | emphasize structured comparison |
| editor | focus on clarity and revision |
| domain expert | bias the response toward a specific frame |

Key point: Persona is most useful when it changes priorities or evaluation criteria. It is less useful as decoration.

## Formatting and Delimiters

Prompt formatting helps separate instructions from content.

| Formatting Choice | Benefit |
| --- | --- |
| Delimiters | mark where source text begins and ends |
| Headed sections | separate role, task, context, and output rules |
| Explicit schemas | make results easier to parse |
| Numbered steps | guide multi-step responses |

Tip: Delimiters are a small change with large practical value because they reduce confusion between instructions and input text.

## Zero-Shot, One-Shot, and Few-Shot Prompting

These patterns differ mainly in how many examples the model receives.

| Pattern | Best Use |
| --- | --- |
| Zero-shot | the task is simple or already familiar to the model |
| One-shot | one example is enough to define tone or structure |
| Few-shot | consistency matters and the pattern is not obvious |

The trade-off is simple: examples usually improve consistency, but they also consume prompt space and can anchor the model too narrowly.

## Chain-of-Thought and Stepwise Guidance

For some tasks, performance improves when the prompt encourages staged reasoning.

| Pattern | Practical Use |
| --- | --- |
| Step-by-step instruction | useful for analysis, planning, or calculations |
| Zero-shot chain prompting | ask the model to work through the task in stages |
| Example-driven reasoning | provide one or more worked examples |

Key point: Stepwise prompting is often valuable because it decomposes the task, not because it is a magic phrase.

## Chaining Prompts Across Steps

Some workflows are easier when one large prompt is split into several smaller ones.

| Stage | Example |
| --- | --- |
| extract | pull facts or themes from a document |
| transform | summarize, classify, or rewrite them |
| evaluate | check completeness, tone, or policy fit |

This makes it easier to inspect failures and swap one stage without rewriting the whole workflow.

## Iteration Matters

Prompt engineering is usually iterative.

1. draft an initial prompt
2. inspect where the output fails
3. add missing context or tighter output constraints
4. test again on varied inputs
5. keep the simpler version if it performs just as well

Tip: Good prompt iteration focuses on failure patterns, not on one lucky example that happened to work.

## Prompt Quality Checklist

Before calling a prompt "done," check:

1. is the task clear and singular
2. does the model have enough context to avoid guessing
3. is the expected output shape explicit
4. would one or two examples improve consistency
5. should this be one prompt or a chained workflow instead
