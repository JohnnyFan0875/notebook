# p-value

The **p-value** is a probability that helps evaluate evidence against the null hypothesis $H_0$.  
假設兩組本來沒差的前提下，出現現在這樣（或更極端）差異的機率。

## Definition

- The probability of obtaining a result at least as extreme as the one observed, **assuming $H_0$ is true**.
- It's the area in the "tail" or "tails" of the distribution, away from the center where the expected values lie.
- Provides a measure of evidence **against $H_0$**.
- Reference: [towardsdatascience](https://towardsdatascience.com/what-is-p-value-370056b8244d/)

<p align="center">
  <img src="https://miro.medium.com/v2/resize:fit:1100/format:webp/1*RXi2Ja89hpMjUvsHSpMW9Q.png" width="500" height="300">
</p>

## Decision Rule

- If **p ≤ α** → Reject the null hypothesis (evidence is strong against $H_0$).
  - 假設兩組本來沒差（$H_0$ 為真）的前提下，出現現在這樣（或更極端）差異的機率，比我能接受的誤判機率（$α$）還小。這代表如果真的沒差，要出現這樣的結果幾乎不可能。因此我認為這結果不是巧合，而是兩組真的有差，所以拒絕「沒差」這個假設（$H_0$）
- If **p > α** → Fail to reject the null hypothesis (evidence is weak against $H_0$).

## Example (using z-score)

- Suppose confidence level = 95% → significance level α = 0.05.
- For a two-tailed test, each tail has α/2 = 0.025.
- Critical z-values: $\pm 1.96$.
- If observed z-score = 2 (right-tailed):
  - The area beyond z=2 is smaller than beyond z=1.96.
  - So p = P(Z > 2) ≈ 0.023 < α/2 = 0.025 (right tail).
  - Reject $H_0$.

📌 **Caution:**

- A small p-value ≠ probability that $H_0$ is false. p-value 不代表 $H_0$ 錯的機率，而是在原假設 $H_0$ 為真時，觀察到目前這樣極端結果的機率。
- A large p-value does not prove $H_0$ true — it means insufficient evidence to reject.

## From t-score (Student’s t-distribution)

```python
from scipy import stats

t_score = 2.1
df = 20  # degrees of freedom

# Right-tailed
p_right = 1 - stats.t.cdf(t_score, df)

# Left-tailed
p_left = stats.t.cdf(t_score, df)

# Two-tailed
p_two = 2 * (1 - stats.t.cdf(abs(t_score), df))

print(p_right, p_left, p_two)
```

## From z-score (using Normal distribution)

```python
from scipy import stats

z_score = 2.0

# right-tailed (positive z-score)
p_right = 1 - stats.norm.cdf(z_score)

# left-tailed (negative z-score)
p_left = stats.norm.cdf(z_score)

# two-tailed
p_two = 2 * (1 - stats.norm.cdf(abs(z_score)))

print(p_right, p_left, p_two)
```

## Relationship with Statistical Power

- While the p-value measures evidence against H₀ in one test, power measures the ability of the test to correctly detect true effects (true positives). Plase see [Power of a Test](power-effect-size.md#power-of-a-test)
