# 1. Probability Basics

**Probability** is a number between 0 and 1 that expresses how likely an event is to occur. It is the mathematical language for reasoning under uncertainty.

> 📌 **為什麼要學機率基礎？**  
> p-value、信賴區間、假設檢定……這些統計概念的底層都是機率。沒有機率的直覺，很容易誤解這些工具的意義。

---

## 1.1 Three Interpretations of Probability

| Interpretation | 中文 | Definition | Example |
|---------------|------|-----------|---------|
| **Classical** | 古典機率 | Equal likelihood — count favorable outcomes / total outcomes | Probability of rolling a 3 on a fair die = 1/6 |
| **Frequentist** | 頻率機率 | Long-run relative frequency of an event over many repeated trials | Flip a coin 10,000 times; heads appears ~50% |
| **Subjective** | 主觀機率 | Degree of personal belief, based on available evidence | "I think there's a 70% chance it will rain tomorrow" |

> 💡 In practice, most statistics you'll encounter uses the **frequentist** interpretation — probability is defined by what would happen if you repeated an experiment many times.

---

## 1.2 Core Terminology

| Term | 中文 | Definition | Example |
|------|------|-----------|---------|
| **Experiment** | 實驗 | Any process with uncertain outcome | Rolling a die |
| **Sample Space (S)** | 樣本空間 | Set of all possible outcomes | S = {1, 2, 3, 4, 5, 6} |
| **Event (E)** | 事件 | A subset of the sample space | E = {2, 4, 6} (rolling even) |
| **Probability P(E)** | 事件機率 | Likelihood of event E occurring | P(even) = 3/6 = 0.5 |
| **Complement (Eᶜ)** | 補集 | All outcomes NOT in E | Eᶜ = {1, 3, 5} |

**Basic probability rules:**

$$0 \leq P(E) \leq 1$$
$$P(S) = 1$$
$$P(E^c) = 1 - P(E)$$

```python
# Simple probability calculation
outcomes = [1, 2, 3, 4, 5, 6]
even = [2, 4, 6]

p_even = len(even) / len(outcomes)
p_odd  = 1 - p_even  # complement rule

print(f"P(even) = {p_even:.3f}")
print(f"P(odd)  = {p_odd:.3f}")
```

---

## 1.3 Combining Events

### Union and Intersection

| Operation | Symbol | Meaning | Example |
|-----------|--------|---------|---------|
| **Union** | A ∪ B | A **or** B occurs (at least one) | Rolling even **or** rolling > 4 |
| **Intersection** | A ∩ B | A **and** B both occur | Rolling even **and** rolling > 4 |
| **Complement** | Aᶜ | A does **not** occur | Not rolling even |

### Addition Rule

$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

> 💡 We subtract the intersection to avoid **double-counting** outcomes that belong to both A and B.  
> 減去交集是為了避免重複計算同時屬於 A 和 B 的結果。

**Special case — Mutually Exclusive Events (互斥事件):**  
If A and B cannot both happen, then P(A ∩ B) = 0, so:

$$P(A \cup B) = P(A) + P(B)$$

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

$$P(A \cap B) = P(A) \times P(B|A)$$

**Special case — Independent Events (獨立事件):**  
If A and B are independent (one doesn't affect the other):

$$P(A \cap B) = P(A) \times P(B)$$

```python
# Two independent coin flips
p_heads = 0.5
p_two_heads = p_heads * p_heads  # independent events
print(f"P(HH) = {p_two_heads:.3f}")  # 0.25
```

---

## 1.4 Conditional Probability (條件機率)

$$P(A|B) = \frac{P(A \cap B)}{P(B)}$$

This reads: "The probability of A **given** that B has already occurred."

> 💡 **直覺解釋**：條件機率是在「已知 B 發生」的前提下，縮小樣本空間後重新計算 A 的機率。  
> Think of it as "zooming in" on the subset of the sample space where B is true, then asking how often A also occurs within that subset.

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

> ⚠️ These two concepts are often confused. 這兩個概念很容易搞混。

| Concept | Definition | Implication |
|---------|-----------|-------------|
| **Independent** | P(A\|B) = P(A) — B gives no information about A | They CAN happen at the same time |
| **Mutually Exclusive** | P(A ∩ B) = 0 — they cannot both happen | Knowing B occurred means A definitely did NOT occur |

> If two events are mutually exclusive and both have non-zero probability, they **cannot** be independent — knowing one happened tells you the other didn't.

---

## 1.5 Law of Total Probability (全機率法則)

If events B₁, B₂, ..., Bₙ are mutually exclusive and cover the entire sample space:

$$P(A) = \sum_{i=1}^{n} P(A|B_i) \cdot P(B_i)$$

> 💡 **直覺**：把複雜事件拆成幾個互斥情境分別計算，再加總。  
> Think of it as: "A can happen in several different scenarios — compute the probability of A in each scenario, weighted by how likely each scenario is."

```python
# Example: Factory quality control
# Two machines: Machine 1 produces 60% of items, Machine 2 produces 40%
# Defect rate: Machine 1 = 2%, Machine 2 = 5%

p_m1 = 0.60; p_defect_given_m1 = 0.02
p_m2 = 0.40; p_defect_given_m2 = 0.05

p_defect = p_m1 * p_defect_given_m1 + p_m2 * p_defect_given_m2
print(f"P(defect) = {p_defect:.4f}")  # 0.0320
```

---

## 1.6 Bayes' Theorem (貝氏定理)

$$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$

Bayes' Theorem allows you to **update a prior belief** when new evidence arrives.

| Term | 中文 | Meaning |
|------|------|---------|
| **P(A)** | 先驗機率 (Prior) | Your initial belief about A before seeing evidence |
| **P(B\|A)** | 概似度 (Likelihood) | How likely you'd see B if A were true |
| **P(B)** | 邊際機率 (Marginal) | Overall probability of observing B |
| **P(A\|B)** | 後驗機率 (Posterior) | Updated belief about A after seeing evidence B |

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

> 💡 **Surprising result**: Even with a 95% accurate test, if the disease is rare (1%), a positive result only means ~16% chance of actually having it. This is why base rates matter enormously.  
> 即使測試準確率 95%，陽性反應真正患病的機率只有約 16%。稀有疾病的基礎率很低，大幅拉低了後驗機率。這是 Bayes' Theorem 最重要的實務直覺。

---

## 1.7 Key Takeaways

| Concept | Key Point |
|---------|-----------|
| **Probability range** | Always between 0 and 1; P(S) = 1 |
| **Complement rule** | P(Aᶜ) = 1 − P(A) — often easier than computing P(A) directly |
| **Addition rule** | Don't forget to subtract the intersection to avoid double-counting |
| **Multiplication rule** | For independent events only: P(A∩B) = P(A)×P(B) |
| **Conditional probability** | P(A\|B) updates the sample space — B is now the new "universe" |
| **Independence ≠ Mutual exclusivity** | These are opposite concepts — don't confuse them |
| **Bayes' Theorem** | Prior belief + new evidence → updated belief; base rate matters enormously |

---

**Next:** [Random Variables →](./2-random-variables.md)
