# Experimental Design

**Experimental design** is the process of planning a study to ensure that the data collected can answer the research question **validly, efficiently, and without bias**. A well-designed experiment allows you to establish **causal relationships** — something descriptive statistics and observational studies cannot do.

> 📌 **核心原則**：好的實驗設計必須在資料收集之前完成。事後補救一個設計不良的實驗，在統計上幾乎是不可能的。"Design of Experiments" (DoE) 不是分析方法，而是資料產生方式的規劃。

---

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

---

## Overview of Topics

| #   | Section                                                                    | Level       | Key Questions Answered                                             |
| --- | -------------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------ |
| 1   | [**Core Concepts & Terminology**](./1-core-concepts.md)                   | Foundation  | What are variables, treatments, controls, and experimental units?  |
| 2   | [**Principles of Experimental Design**](./2-principles.md)                | Foundation  | What makes an experiment valid? Randomization, replication, blocking. |
| 3   | [**Common Experimental Designs**](./3-designs.md)                         | Core        | Which design structure fits my situation?                          |
| 4   | [**Confounding, Bias & Validity**](./4-confounding-bias.md)               | Core        | What can go wrong, and how do I prevent it?                        |
| 5   | [**Sample Size & Statistical Power**](./5-sample-size-power.md)           | Applied     | How many observations do I need?                                   |

---

## What's Inside Each Section

### 1. Core Concepts & Terminology

- Independent vs. dependent vs. confounding variables
- Experimental units, subjects, and observational units
- Treatment, control, placebo, and levels of a factor
- The difference between experimental and observational studies

### 2. Principles of Experimental Design

The three fundamental principles that make an experiment trustworthy:

| Principle           | Purpose                                          |
| ------------------- | ------------------------------------------------ |
| **Randomization**   | Eliminates systematic bias in group assignment   |
| **Replication**     | Ensures results are not due to chance            |
| **Blocking**        | Reduces nuisance variability to improve precision |

### 3. Common Experimental Designs

Organized by complexity and use case:

| Design                            | When to Use                                        |
| --------------------------------- | -------------------------------------------------- |
| Completely Randomized Design (CRD)| Homogeneous units, simplest structure              |
| Randomized Complete Block (RCBD)  | Known source of variability to control             |
| Factorial Design                  | Multiple factors; studying interactions            |
| Latin Square                      | Two blocking factors simultaneously                |
| Crossover Design                  | Each subject receives all treatments               |
| Split-Plot Design                 | Some factors harder to randomize than others       |

### 4. Confounding, Bias & Validity

- Types of confounding and how to detect them
- Selection bias, attrition bias, observer bias, demand characteristics
- Internal validity vs. external validity vs. statistical conclusion validity
- Blinding (single, double, triple) and its role

### 5. Sample Size & Statistical Power

- Type I error (α), Type II error (β), and statistical power (1−β)
- Effect size and why it matters more than p-values
- Power analysis in Python using `statsmodels`
- Practical rules of thumb

---

## Experimental vs. Observational Studies

| Feature                       | Experiment                              | Observational Study                      |
| ----------------------------- | --------------------------------------- | ---------------------------------------- |
| Assignment to groups          | Random (by researcher)                  | Self-selected or by circumstance         |
| Can establish causation        | ✅ Yes (if well-designed)               | ❌ No — association only                 |
| Controls confounders          | ✅ Via randomization                    | ❌ Must use statistical adjustment        |
| Feasibility                   | Sometimes impractical or unethical      | Usually easier to conduct               |
| Examples                      | RCT, A/B test, lab experiment           | Survey, cohort study, case-control study |

> 💡 **When experiments are impossible**: In medicine, social science, and economics, you often cannot randomize (it would be unethical to randomly assign people to smoke). Quasi-experimental designs (difference-in-differences, regression discontinuity, instrumental variables) attempt to approximate experimental conditions in observational settings. These are covered in later sections on causal inference.

---

## Visualization Quick Reference

| Diagram / Chart          | Best For                                              |
| ------------------------ | ----------------------------------------------------- |
| Design diagram (flowchart)| Showing treatment allocation and group structure      |
| Power curve              | Visualizing the tradeoff between n, effect size, power|
| Interaction plot         | Detecting and displaying factorial interactions        |
| Residual plots           | Checking model assumptions post-analysis              |

---

## Key Takeaway

> Experimental design answers: **"How should I collect data so I can answer my question?"**  
> The best analysis cannot save a bad design — invest effort here before collecting a single data point.
