# Probability Basics

**Probability** is a number between 0 and 1 that expresses how likely an event is to occur. It is the mathematical language for reasoning under uncertainty.

Key point: Why should we learn the basics of probability? p-value, confidence interval, hypothesis testing...the bottom layer of these statistical concepts is probability. Without an intuition of probability, it is easy to misunderstand the meaning of these tools.

## Three Interpretations of Probability

| Interpretation | Definition | Example |
| --------------- | ----------- | --------- |
| **Classical** | Equal likelihood — count favorable outcomes / total outcomes | Probability of rolling a 3 on a fair die = 1/6 |
| **Frequentist** | Long-run relative frequency of an event over many repeated trials | Flip a coin 10,000 times; heads appears ~50% |
| **Subjective** | Degree of personal belief, based on available evidence | "I think there's a 70% chance it will rain tomorrow" |

Tip: In practice, most statistics you'll encounter uses the frequentist interpretation — probability is defined by what would happen if you repeated an experiment many times.

## Core Terminology

| Term | Definition | Example |
| ------ | ----------- | --------- |
| **Experiment** | Any process with uncertain outcome | Rolling a die |
| **Sample Space (S)** | Set of all possible outcomes | S = {1, 2, 3, 4, 5, 6} |
| **Event (E)** | A subset of the sample space | E = {2, 4, 6} (rolling even) |
| **Probability P(E)** | Likelihood of event E occurring | P(even) = 3/6 = 0.5 |
| **Complement (Eᶜ)** | All outcomes NOT in E | Eᶜ = {1, 3, 5} |

**Basic probability rules:**

\[
0 \leq P(E) \leq 1
\]
\[
P(S) = 1
\]
\[
P(E^c) = 1 - P(E)
\]

```python
# Simple probability calculation
outcomes = [1, 2, 3, 4, 5, 6]
even = [2, 4, 6]

p_even = len(even) / len(outcomes)
p_odd  = 1 - p_even  # complement rule

print(f"P(even) = {p_even:.3f}")
print(f"P(odd)  = {p_odd:.3f}")
```

## Combining Events

### Union and Intersection

| Operation | Symbol | Meaning | Example |
| ----------- | -------- | --------- | --------- |
| **Union** | A ∪ B | A **or** B occurs (at least one) | Rolling even **or** rolling > 4 |
| **Intersection** | A ∩ B | A **and** B both occur | Rolling even **and** rolling > 4 |
| **Complement** | Aᶜ | A does **not** occur | Not rolling even |

### Addition Rule

\[
P(A \cup B) = P(A) + P(B) - P(A \cap B)
\]

Tip: We subtract the intersection to avoid double-counting outcomes that belong to both A and B.

**Special case — Mutually Exclusive Events:**
If A and B cannot both happen, then P(A ∩ B) = 0, so:

\[
P(A \cup B) = P(A) + P(B)
\]

```python
# Example: die rolling
# A = rolling even {2,4,6}, B = rolling > 4 {5,6}
p_A   = 3/6   # P(even)
p_B   = 2/6   # P(> 4)
p_AandB = 1/6 # P(even AND > 4) = {6} only

p_AorB = p_A + p_B - p_AandB
print(f"P(A or B) = {p_AorB:.3f}")  # 4/6 = 0.667
```

### Multiplication Rule

\[
P(A \cap B) = P(A) \times P(B|A)
\]

**Special case — Independent Events:**
If A and B are independent (one doesn't affect the other):

\[
P(A \cap B) = P(A) \times P(B)
\]

```python
# Two independent coin flips
p_heads = 0.5
p_two_heads = p_heads * p_heads  # independent events
print(f"P(HH) = {p_two_heads:.3f}")  # 0.25
```

## Conditional Probability

\[
P(A|B) = \frac{P(A \cap B)}{P(B)}
\]

This reads: "The probability of A **given** that B has already occurred."

Tip: Intuitive explanation: Conditional probability is to recalculate the probability of A after reducing the sample space under the premise that "B is known to occur". Think of it as "zooming in" on the subset of the sample space where B is true, then asking how often A also occurs within that subset.

```python
# Example: drawing cards
# P(King | face card drawn)?
# Face cards = Jack, Queen, King (3 per suit × 4 suits = 12)
# Kings = 4

p_king_and_face = 4/52   # P(King AND face card) — all kings are face cards
p_face          = 12/52  # P(face card)

p_king_given_face = p_king_and_face / p_face
print(f"P(King | Face card) = {p_king_given_face:.3f}")  # 0.333
```

### Independence vs Mutual Exclusivity

Warning: These two concepts are often confused.

| Concept | Definition | Implication |
| --------- | ----------- | ------------- |
| **Independent** | P(A\ | B) = P(A) — B gives no information about A | They CAN happen at the same time |
| **Mutually Exclusive** | P(A ∩ B) = 0 — they cannot both happen | Knowing B occurred means A definitely did NOT occur |

If two events are mutually exclusive and both have non-zero probability, they cannot be independent — knowing one happened tells you the other didn't.

## Law of Total Probability

If events B₁, B₂, ..., Bₙ are mutually exclusive and cover the entire sample space:

\[
P(A) = \sum_{i=1}^{n} P(A|B_i) \cdot P(B_i)
\]

Tip: Intuition: Divide complex events into several mutually exclusive situations, calculate them separately, and then add them together. Think of it as: "A can happen in several different scenarios — compute the probability of A in each scenario, weighted by how likely each scenario is."

```python
# Example: Factory quality control
# Two machines: Machine 1 produces 60% of items, Machine 2 produces 40%
# Defect rate: Machine 1 = 2%, Machine 2 = 5%

p_m1 = 0.60; p_defect_given_m1 = 0.02
p_m2 = 0.40; p_defect_given_m2 = 0.05

p_defect = p_m1 * p_defect_given_m1 + p_m2 * p_defect_given_m2
print(f"P(defect) = {p_defect:.4f}")  # 0.0320
```

## Bayes' Theorem

\[
P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}
\]

Bayes' Theorem allows you to **update a prior belief** when new evidence arrives.

| Term | Meaning |
| ------ | --------- |
| **P(A)** | Your initial belief about A before seeing evidence |
| **P(B\ | Likelihood | How likely you'd see B if A were true |
| **P(B)** | Overall probability of observing B |
| **P(A\ | Posterior probability (Posterior) | Updated belief about A after seeing evidence B |

**Classic Example — Medical Test:**

A disease affects 1% of the population. A test is 95% accurate (sensitivity = 95%, false positive rate = 5%).
**If you test positive, what is the probability you actually have the disease?**

```python
p_disease          = 0.01   # prior: 1% of population has disease
p_positive_given_disease  = 0.95   # sensitivity
p_positive_given_no_disease = 0.05 # false positive rate
p_no_disease       = 1 - p_disease

# P(positive) using total probability law
p_positive = (p_positive_given_disease * p_disease +
              p_positive_given_no_disease * p_no_disease)

# Bayes' Theorem
p_disease_given_positive = (p_positive_given_disease * p_disease) / p_positive

print(f"P(positive)                = {p_positive:.4f}")
print(f"P(disease | positive test) = {p_disease_given_positive:.4f}")  # ~16%
```

Tip: Surprising result: Even with a 95% accurate test, if the disease is rare (1%), a positive result only means ~16% chance of actually having it. This is why base rates matter enormously. The base rate of rare diseases is very low, which greatly reduces the posterior probability. This is the most important practical intuition of Bayes' Theorem.

## From Formula to Simulation

Probability rules give the exact answer when the sample space is simple. When the system becomes complicated, a useful habit is to **approximate probability empirically** by repeated simulation and compare the result back to the formula.

Example: the probability of getting at least one head in three fair coin flips is

\[
1 - P(\text{all tails}) = 1 - \left(\frac{1}{2}\right)^3 = \frac{7}{8} = 0.875
\]

```python
import numpy as np

rng = np.random.default_rng(42)
n_trials = 200_000

# 1 = heads, 0 = tails
flips = rng.integers(0, 2, size=(n_trials, 3))
p_at_least_one_head = (flips.sum(axis=1) >= 1).mean()

print(f"Simulated P(at least one head) = {p_at_least_one_head:.4f}")
print("Exact probability              = 0.8750")
```

Tip: This "simulate first, derive second" loop is a fast way to debug intuition. If the simulation and the formula disagree, one of your assumptions is probably wrong.

## Key Takeaways

| Concept | Key Point |
| --------- | ----------- |
| **Probability range** | Always between 0 and 1; P(S) = 1 |
| **Complement rule** | P(Aᶜ) = 1 − P(A) — often easier than computing P(A) directly |
| **Addition rule** | Don't forget to subtract the intersection to avoid double-counting |
| **Multiplication rule** | For independent events only: P(A∩B) = P(A)×P(B) |
| **Conditional probability** | P(A\ | B) updates the sample space — B is now the new "universe" |
| **Independence ≠ Mutual exclusivity** | These are opposite concepts — don't confuse them |
| **Bayes' Theorem** | Prior belief + new evidence → updated belief; base rate matters enormously |
