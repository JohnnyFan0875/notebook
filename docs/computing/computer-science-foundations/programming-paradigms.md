# Programming Paradigms

## Core Idea

A programming paradigm is a style of thinking about how programs should be structured. It is less about syntax and more about the organizing model used to express logic, split responsibilities, and manage change.

## Why Paradigms Matter

Different paradigms emphasize different strengths:

- how logic is decomposed
- how state is managed
- how reusable units are defined
- how easy code is to test, extend, or reason about

The same real-world problem can often be solved in more than one paradigm.

## A Useful High-Level Split

| Paradigm family | Main question it emphasizes |
| --- | --- |
| Imperative | How do we perform the task step by step? |
| Declarative | What result do we want, without spelling out every step? |

Procedural programming is a form of imperative programming. Functional programming is often presented as a declarative style. Object-oriented programming focuses on organizing behavior and data around interacting objects.

## Procedural Programming

### Core model

Programs are built from procedures or subroutines: named sequences of steps that can be reused.

### Strengths

- Clear step-by-step control flow
- Good modularity through procedures and functions
- Often approachable for beginners
- Works well for scripts, automation, and tasks with explicit ordered steps

### Common building blocks

- variables and mutable state
- conditionals such as `if` and `else`
- loops
- named procedures or helper functions

### Limits

- Shared mutable state can become hard to reason about in larger systems
- Large procedural codebases can become tightly coupled if responsibilities are not separated well

## Functional Programming

### Core model

Programs are expressed through functions, especially pure functions.

A pure function:

- returns the same output for the same input
- avoids side effects such as mutating shared state or writing externally as part of its core calculation

### Strengths

- Easier local reasoning and testing
- Better composability
- Reduced hidden state and side-effect bugs
- Often useful for transformations, pipelines, and data processing

### Limits

- Can feel less intuitive when the problem is naturally stateful
- Some teams find the abstraction style steeper at first

## Object-Oriented Programming

### Core model

Programs are organized around objects that bundle data and behavior.

| Concept | Meaning |
| --- | --- |
| Class | A blueprint that describes shared structure and behavior |
| Object | A concrete instance of a class |
| Method | Behavior associated with an object or class |
| Attribute / field | Data stored on the object |

### Strengths

- Good for modeling entities with state and behavior
- Encourages encapsulation
- Can improve reuse through composition and, sometimes, inheritance
- Often helpful in large application codebases

### Limits

- Overengineering with deep class hierarchies can hurt clarity
- Inheritance can be misused and create fragile designs
- Not every problem is best modeled as a network of objects

## Inheritance and Reuse

Inheritance lets one class derive behavior or structure from another, but it should be used carefully.

Practical rule:

- Prefer inheritance when there is a true "is-a" relationship and the abstraction is stable.
- Prefer composition when behavior should be assembled flexibly.

More inheritance is not automatically better design.

## Separation of Responsibilities Across Paradigms

Each paradigm decomposes work differently:

| Paradigm | Main unit of decomposition |
| --- | --- |
| Procedural | Procedures and stepwise control flow |
| Functional | Functions and transformations |
| Object-oriented | Objects, classes, and message passing |

This is one reason paradigm choice affects readability, architecture, and maintenance.

## Choosing a Paradigm

Use paradigm choice as a design decision, not an identity.

Questions that help:

- Is the problem mostly sequential and procedural?
- Is the logic mostly transformations over data?
- Is the domain naturally described as entities with state and behavior?
- Will the codebase benefit more from explicit flow, composable functions, or strong encapsulation?

In practice, many modern languages and codebases are multi-paradigm. Mixing styles thoughtfully is often better than forcing one style everywhere.

## Practical Takeaways

- Paradigms are different organizational models for code, not competing religions.
- Procedural programming emphasizes ordered steps and reusable procedures.
- Functional programming emphasizes pure functions and reduced side effects.
- Object-oriented programming emphasizes data plus behavior organized around objects.
- The best paradigm depends on the problem, team, and maintenance needs.
