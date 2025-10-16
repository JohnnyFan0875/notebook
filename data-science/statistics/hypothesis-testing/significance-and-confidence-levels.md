# Significance and Confidence Level

## Significance Level (α)

The **significance level (α)** is a threshold used in hypothesis testing to decide whether to reject the null hypothesis $H_0$.
接受多大的機率誤判。

### Definition

- **α (alpha):** The probability of rejecting the null hypothesis when it is actually true.  
  → This is a [**Type I error**](./README.md#type-i-and-type-ii-errors) (false positive).
- It represents the **risk you are willing to take** of making a false positive error.
- The value of α is determined **before** running the test.

Common choices:

- α = 0.05 (5% risk)
- α = 0.01 (1% risk)

### Familywise Error Rate (Multiple Tests)

When performing multiple hypothesis tests, the chance of at least one false positive increases.

- Probability of **not** making a false positive in one test: $1 − α$.
- Probability of **not** making a false positive in all $k$ tests: $(1 − α)^k$.
- Probability of making **at least one false positive** across $k$ tests: $1 − (1 − α)^k $

### Choosing α

- **Exploratory studies:** Higher α (e.g. 0.1) may be acceptable.
- **Confirmatory or critical studies (e.g., clinical trials):** Lower α (e.g. 0.01 or 0.001) is preferred.
- Always justify your chosen α level in the study context.

### Summary

- α sets the decision threshold for rejecting $H_0$.
- Smaller α reduces false positives but increases the chance of false negatives (Type II error).
- Balance between Type I and Type II errors depends on the research question.

## Confidence Level (1 − α)

The **confidence level** represents the degree of certainty that a particular estimate includes the true population parameter.
對這個『估計方法』有多少信心，若重複做很多次實驗，有這個比例的信賴區間會包含真實答案。

### Definition

- Confidence level = $1 − α$, where α is the significance level.
- Common choices:
  - 95% confidence level → α = 0.05
  - 99% confidence level → α = 0.01
- Interpretation:
  - If we repeat the same study many times, approximately 95% (or 99%) of the calculated confidence intervals would contain the true parameter.
  - It does **not** mean that there is a 95% probability the true parameter is in a specific interval (the parameter is fixed, the interval varies).
    - 想像射箭 100 次，每次都畫一個區間（信賴區間）去「包住靶心」。95 次成功包到靶心表示方法的「信心」是 95%。但單看其中一個箭圈（某一次的區間）時，靶心不是「有 95% 機率在圈裡」，而是要嘛在裡面、要嘛不在裡面。

### Confidence Interval of the Mean

- Please refer to [confidence interval](confidence-interval.md)

![Image](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*zhq4V275F0YthnSLYRU0FA.jpeg)
