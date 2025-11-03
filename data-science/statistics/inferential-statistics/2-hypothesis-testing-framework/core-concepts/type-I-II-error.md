# Type I and Type II Errors

Hypothesis testing involves decision-making under uncertainty. Every test carries a risk of making an incorrect conclusion — either rejecting a true null hypothesis or failing to reject a false one. These are known as **Type I** and **Type II** errors.

## 1. Concept Overview

| Concept            | True Condition         | Test Result                                | Interpretation                     | Type                  |
| ------------------ | ---------------------- | ------------------------------------------ | ---------------------------------- | --------------------- |
| **True Positive**  | Hₐ (difference exists) | Reject H₀ (conclude difference exists)     | Correctly detects a real effect    | Correct               |
| **False Positive** | H₀ (no difference)     | Reject H₀ (conclude difference exists)     | Incorrectly concludes a difference | **Type I error (α)**  |
| **True Negative**  | H₀ (no difference)     | Fail to reject H₀ (conclude no difference) | Correctly concludes no difference  | Correct               |
| **False Negative** | Hₐ (difference exists) | Fail to reject H₀ (conclude no difference) | Fails to detect a real effect      | **Type II error (β)** |

## 2. Definitions

- **Type I error (α):** Rejecting a true null hypothesis.

  - Also called a **false positive**.
  - Probability = **α**, the significance level (commonly 0.05).
  - Example: Concluding that a drug works when it actually does not.

- **Type II error (β):** Failing to reject a false null hypothesis.

  - Also called a **false negative**.
  - Probability = **β**, the complement of statistical power.
  - Example: Concluding that a drug has no effect when it truly does.

## 3. Relationship Between α, β, and Power

| Term                                                         | Symbol | Meaning                               | Desired Direction               |
| ------------------------------------------------------------ | ------ | ------------------------------------- | ------------------------------- |
| [**Significance level**](./significance-level.md)            | α      | Probability of Type I error           | ↓ smaller = stricter test       |
| **Type II error rate**                                       | β      | Probability of missing a real effect  | ↓ smaller = more sensitive test |
| [**Power**](../../4-effect-size-and-power/power-analysis.md) | 1 − β  | Probability of correctly rejecting H₀ | ↑ higher = better detection     |

The relationship is often visualized as overlapping distributions under H₀ and H₁. The critical region (α) defines when we reject H₀. Increasing α widens this region (fewer false negatives but more false positives). Reducing α makes the test stricter, increasing the risk of β.

## 4. Balancing α and β

- There is always a **trade-off** between α and β.
- Reducing α (more conservative test) usually increases β unless **sample size** or **effect size** increases.
- **Power analysis** helps determine adequate sample size to achieve desired α and β.

**Example:**

- α = 0.05 → 5% chance of false positive.
- β = 0.20 → 20% chance of false negative.
- Power = 1 − β = 0.80 → 80% chance of detecting a true effect.

![Image](https://www.six-sigma-material.com/images/xHypothesisTestErrorDepiction.png.pagespeed.ic.dWU2rGWhQ4.webp)

## 5. Practical Implications

| Field                    | Lower α preferred                        | Lower β (higher power) preferred    |
| ------------------------ | ---------------------------------------- | ----------------------------------- |
| **Clinical trials**      | To avoid claiming ineffective drugs work | To avoid missing beneficial effects |
| **Exploratory research** | Moderate α (0.05–0.10) acceptable        | Focus on power for discovery        |
| **Quality control**      | Strict α (0.01 or less)                  | Depends on cost of missed defects   |

## 6. Summary

- **Type I error (α):** Detecting a difference when none exists → false positive.
- **Type II error (β):** Missing a true difference → false negative.
- **Power (1 − β):** Sensitivity of the test to detect real effects.
- Proper study design and adequate sample size minimize both errors.
