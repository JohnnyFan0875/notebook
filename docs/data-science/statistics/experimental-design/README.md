# Introduction

**Experimental design** is the process of planning a study to ensure that the data collected can answer the research question **validly, efficiently, and without bias**. A well-designed experiment allows you to establish **causal relationships** — something descriptive statistics and observational studies cannot do.

Key point: Good experimental design happens before data collection starts. Analysis can rescue very little once the design is flawed, because design determines what evidence the data can support.

## Start Here If...

This module should come before data collection whenever you are asking:

- "What exactly is my experimental unit?"
- "How should I assign treatments?"
- "How do I reduce bias before analysis begins?"
- "How many observations do I need for a meaningful result?"

## Why This Order?

Experimental design logically bridges descriptive statistics (what does data look like?) and inferential statistics (what can we conclude?):

```
Descriptive Statistics → understand your data
        ↓
Experimental Design → plan how to collect data that can answer causal questions
        ↓
Inferential Statistics → draw valid conclusions from that data
```

A poorly designed experiment produces data that cannot answer your question — no matter how sophisticated the analysis. Getting the design right first is the highest-leverage step in any study.

## Overview of Topics

| Section | Level | Key Questions Answered |
| -------------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------ |
| [**Core Concepts & Terminology**](./core-concepts.md) | Foundation | What are variables, treatments, controls, and experimental units? |
| [**Principles of Experimental Design**](./principles.md) | Foundation | What makes an experiment valid? Randomization, replication, blocking. |
| [**A/B Testing**](./ab-testing.md) | Applied | How do I run product experiments without common instrumentation and inference mistakes? |
| [**Common Experimental Designs**](./designs.md) | Core | Which design structure fits my situation? |
| [**Confounding, Bias & Validity**](./confounding-bias.md) | Core | What can go wrong, and how do I prevent it? |
| [**Sample Size & Statistical Power**](./sample-size-power.md) | Applied | How many observations do I need? |

## What's Inside Each Section

### Core Concepts & Terminology

- Independent vs. dependent vs. confounding variables
- Experimental units, subjects, and observational units
- Treatment, control, placebo, and levels of a factor
- The difference between experimental and observational studies

### Principles of Experimental Design

The three fundamental principles that make an experiment trustworthy:

| Principle | Purpose |
| ------------------- | ------------------------------------------------ |
| **Randomization** | Eliminates systematic bias in group assignment |
| **Replication** | Ensures results are not due to chance |
| **Blocking** | Reduces nuisance variability to improve precision |

### Common Experimental Designs

Organized by complexity and use case:

| Design | When to Use |
| --------------------------------- | -------------------------------------------------- |
| Completely Randomized Design (CRD) | Homogeneous units, simplest structure |
| Randomized Complete Block (RCBD) | Known source of variability to control |
| Factorial Design | Multiple factors; studying interactions |
| Latin Square | Two blocking factors simultaneously |
| Crossover Design | Each subject receives all treatments |
| Split-Plot Design | Some factors harder to randomize than others |

### A/B Testing

- when randomized product experiments are the right tool
- how to write testable product hypotheses
- why the randomized unit and analysis unit must match
- how metric type affects test choice
- why peeking and weak instrumentation invalidate conclusions

### Confounding, Bias & Validity

- Types of confounding and how to detect them
- Selection bias, attrition bias, observer bias, demand characteristics
- Internal validity vs. external validity vs. statistical conclusion validity
- Blinding (single, double, triple) and its role

### Sample Size & Statistical Power

- Type I error (α), Type II error (β), and statistical power (1−β)
- Effect size and why it matters more than p-values
- Power analysis in Python using `statsmodels`
- Practical rules of thumb

## Experimental vs. Observational Studies

| Feature | Experiment | Observational Study |
| ----------------------------- | --------------------------------------- | ---------------------------------------- |
| Assignment to groups | Random (by researcher) | Self-selected or by circumstance |
| Can establish causation | ✅ Yes (if well-designed) | ❌ No — association only |
| Controls confounders | ✅ Via randomization | ❌ Must use statistical adjustment |
| Feasibility | Sometimes impractical or unethical | Usually easier to conduct |
| Examples | RCT, A/B test, lab experiment | Survey, cohort study, case-control study |

Tip: In many real settings, true randomization is impossible or unethical. Quasi-experimental designs such as difference-in-differences, regression discontinuity, and instrumental variables belong to the broader causal-inference toolkit and are best treated as an advanced follow-up topic.

## Visualization Quick Reference

| Diagram / Chart | Best For |
| ------------------------ | ----------------------------------------------------- |
| Design diagram (flowchart) | Showing treatment allocation and group structure |
| Power curve | Visualizing the tradeoff between n, effect size, power |
| Interaction plot | Detecting and displaying factorial interactions |
| Residual plots | Checking model assumptions post-analysis |

## Key Takeaway

Experimental design answers: "How should I collect data so I can answer my question?" The best analysis cannot save a bad design — invest effort here before collecting a single data point.

## Deep-Study Priorities

The most important progression in this module is:

1. causal question clarity
2. randomization and control
3. blocking and nuisance variation
4. A/B testing workflow for modern product experiments
5. effect size and power planning

Tip: Good analysis after bad design is still bad evidence.

## Suggested Reading Order

For most readers, this sequence works well:

1. clarify the causal question and experimental unit
2. learn randomization, replication, and blocking
3. study [A/B Testing](./ab-testing.md) if you work on product or web experiments
4. choose the design structure
5. think through bias and validity threats
6. finish with power and sample-size planning
