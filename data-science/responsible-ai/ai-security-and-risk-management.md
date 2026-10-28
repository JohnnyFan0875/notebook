# AI Security and Risk Management

AI security and risk management focuses on identifying how AI systems can fail, be manipulated, or cause harm, then putting controls in place before and after deployment.

Key point: Traditional security controls are not enough for AI systems. You also need to manage model behavior, data integrity, lifecycle drift, and decision quality.

## Why AI Risk Management Is Different

AI systems introduce risks that are partly technical, partly statistical, and partly organizational.

| Traditional Concern | AI-Specific Extension |
| --- | --- |
| Unauthorized access | Sensitive prompt, feature, or training data exposure |
| System failure | Hallucinated or biased outputs that still look plausible |
| Input tampering | Adversarial examples and manipulated prompts |
| Bad data quality | Data poisoning or silent model drift |

Warning: Many AI failures do not look like outages. The system may remain available while silently producing wrong, unfair, or unsafe results.

## Common AI Security and Model Risks

| Risk | What It Means | Typical Impact |
| --- | --- | --- |
| Bias | Uneven treatment caused by data, assumptions, or objectives | Disparate outcomes and trust erosion |
| Hallucination | Confident but false or misleading output | Bad decisions and misinformation |
| Data poisoning | Malicious or corrupted training data | Distorted predictions and hidden backdoors |
| Adversarial attack | Inputs crafted to mislead the model at runtime | Integrity failures and unsafe behavior |
| Sensitive data exposure | Private or confidential data leaked through training or inference | Compliance, privacy, and reputational harm |
| Model drift | A once-accurate model becomes less reliable over time | Degraded performance and biased outputs |
| Data leakage | Information from outside the true training boundary influences evaluation or training | Inflated metrics and weak real-world performance |

Tip: Some risks are security problems, some are modeling problems, and some are both. Treating every issue as only a cybersecurity problem usually misses important statistical controls.

## Bias and Hallucination

Bias and hallucination are often subtle because the output can still appear fluent or efficient.

| Risk | Common Causes | First Control |
| --- | --- | --- |
| Bias | Skewed data, flawed proxies, untested assumptions | Evaluate across relevant groups and review proxies |
| Hallucination | Weak grounding, insufficient data, incorrect assumptions | Add verification, retrieval, and confidence-aware workflows |

Key point: Fast automation amplifies harm. A biased or hallucinated system can scale mistakes much faster than a human review process.

## Data Poisoning and Adversarial Attacks

These risks focus on manipulation rather than ordinary model error.

| Attack Type | Attack Surface | Example |
| --- | --- | --- |
| Data poisoning | Training or fine-tuning pipeline | Injected records push the model toward bad outputs |
| Adversarial attack | Runtime inputs | Slightly modified inputs trigger incorrect predictions |
| Prompt or context manipulation | LLM instructions or retrieved context | Malicious content steers the response away from intended behavior |

Useful controls include:

1. validate data sources and provenance
2. restrict who can modify training data or prompts
3. test the system with adversarial or edge-case inputs
4. isolate high-risk workflows behind human review

## Transparency, Interpretability, and Sensitive Domains

In healthcare, finance, hiring, or public services, the decision process matters almost as much as the output itself.

| Term | Practical Meaning |
| --- | --- |
| Transparency | Stakeholders can understand the system purpose, scope, and main logic |
| Interpretability | Teams can explain why the model produced a specific output |
| Traceability | Inputs, versions, approvals, and incidents are recorded over time |

A model that cannot be interpreted well enough for its use case is a risk management problem, not just an explainability preference.

## Monitoring Risk Across the Lifecycle

Risk management starts during development and continues after deployment.

| Stage | Main Question |
| --- | --- |
| Data and development | Is the model learning from fair, accurate, and relevant data? |
| Validation | Are metrics believable, or are they inflated by leakage or bad splits? |
| Deployment | What harms occur if the model is wrong in production? |
| Monitoring | Is the environment changing in ways that break model assumptions? |

Warning: A model that passed offline evaluation can still become unsafe later because of [data leakage](../machine-learning/foundations/data-leakage.md), drift, or changing user behavior.

## Model Drift, Overfitting, Underfitting, and Leakage

These are not always malicious, but they are core risk sources.

| Risk | Signal | Typical Response |
| --- | --- | --- |
| Model drift | Performance drops as data patterns change | Monitor, recalibrate, or retrain |
| Overfitting | Strong training results but weak generalization | Simplify, regularize, cross-validate |
| Underfitting | Model is too simple to capture the signal | Improve features or model capacity |
| Data leakage | Validation results look unrealistically good | Redesign splitting and pipeline boundaries |

Tip: Leakage is especially dangerous because it creates false confidence. The model looks excellent right up until real deployment.

## Strategic Risk Management Decisions

Risk management is not only a technical checklist. Teams also need to decide where to spend attention and what level of residual risk is acceptable.

| Decision Area | Core Question |
| --- | --- |
| Threat prioritization | Which risks have the highest severity and likelihood? |
| Risk appetite | How much residual risk can the organization tolerate? |
| Innovation vs. security | Where should speed be limited by safeguards? |
| Cost vs. benefit | Does mitigation cost less than expected harm? |
| Stakeholder perspective | Who experiences the real-world effect of failure? |

## Threat Prioritization

A practical first step is to rank risks by severity and likelihood.

| Priority Pattern | Typical Action |
| --- | --- |
| High impact, high likelihood | Immediate mitigation and active monitoring |
| High impact, low likelihood | Strong contingency planning |
| Low impact, high likelihood | Process fixes or automation to reduce repetition |
| Low impact, low likelihood | Monitor lightly and revisit later |

Low-hanging improvements are often worth doing early if they reduce meaningful risk quickly and create momentum for broader controls.

## Minimum Standard Before Deployment

Before shipping an AI system, you should be able to answer:

1. what the main model and security risks are
2. which risks are highest priority and why
3. what controls exist for bias, hallucination, manipulation, and drift
4. how sensitive data is protected in training and inference
5. who monitors the system and what triggers escalation or rollback
