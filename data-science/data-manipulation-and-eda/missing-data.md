# Missing Data Mechanisms

Missing data can be classified into three categories based on the relationship between the missingness and the observed/unobserved data. Understanding these mechanisms is crucial for selecting appropriate statistical methods for handling missing data.

This note focuses on the **conceptual side** of missingness: MCAR, MAR, MNAR, and why those mechanisms change the validity of deletion or imputation choices. If you need tool-specific workflows, see [Pandas: Handling Missing Data](../python-foundations/pandas/missing-data.md) or [Missing Data in R](../r-foundations/missing-data.md).

## 1. **MCAR — Missing Completely at Random**

- **Definition:**
  The probability that a value is missing does **not depend on either the observed data or the missing (unobserved) data**.
  In other words, the missingness is **entirely random**.

- **Implication:**

  - Missing data introduces **no systematic bias**.
  - Complete-case analysis (simply dropping missing data) can still produce unbiased estimates, although statistical power is reduced.

- **Example:**

  - A lab machine randomly fails to record a measurement due to a temporary malfunction.
  - Survey participants randomly skip a question because the page refreshes unexpectedly.

## 2. **MAR — Missing at Random**

- **Definition:**
  The probability of a value being missing **depends only on the observed data**, not on the missing data itself.
  Once the observed variables are accounted for, missingness is **conditionally random**.

![Image](https://substackcdn.com/image/fetch/$s_!GsDj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0fc36c04-9478-482f-8820-432f005fbb78_2401x601.png)

- **Implication:**

  - Missingness can be modeled using the observed data.
  - Methods like **multiple imputation** or **maximum likelihood** can provide unbiased estimates under MAR.

- **Example:**

  - Older patients are less likely to report their weight in a medical survey (age is observed).
  - In a study, high-income participants are more likely to skip a question about the number of cars they own, and income is recorded.

## 3. **MNAR — Missing Not at Random**

- **Definition:**
  The probability of a value being missing **depends on the unobserved (missing) value itself**, even after considering the observed data.
  Missingness is **systematic and non-random**.

![Image](https://substackcdn.com/image/fetch/$s_!zsOl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a059c65-6a2a-4b0d-baf0-d3358f419baa_3028x905.png)

- **Implication:**

  - Standard imputation methods assuming MAR may lead to **biased estimates**.
  - Requires **specialized modeling**, such as selection models or pattern-mixture models.

- **Example:**

  - Patients with severe depression are less likely to complete a mental health questionnaire (severity is unobserved if missing).
  - Individuals with very high income are less likely to report it in a survey.

## 4. **Deletion Methods**

When handling missing data without imputation, deletion strategies are commonly applied.

### Listwise Deletion (Complete Case Analysis)

- Removes an entire row (case) if **any** variable has a missing value.
- **Pros:** Simple to implement; unbiased if data are MCAR.
- **Cons:** Reduces sample size, may lower statistical power, can bias results if data are not MCAR.
- **Example:** If `age` is missing for a participant, that participant is excluded from regression analysis entirely.

### Pairwise Deletion (Available Case Analysis)

- Uses all available data for each calculation, excluding cases only when values needed for a particular analysis are missing.
- **Pros:** Retains more data than listwise deletion.
- **Cons:** Different analyses may use different subsets of the data, leading to inconsistent sample sizes and possible bias.
- **Example:** In correlation analysis between `age` and `income`, a participant missing `income` is excluded only from that correlation but could still contribute to correlations involving `age` and `education`.

### **Summary Table**

| Mechanism/Method      | Depends on Observed Data? | Depends on Missing Value? | Example                                    |
| --------------------- | ------------------------- | ------------------------- | ------------------------------------------ |
| **MCAR**              | ❌ No                     | ❌ No                     | Random machine failure in lab              |
| **MAR**               | ✅ Yes                    | ❌ No                     | Older patients skip weight question        |
| **MNAR**              | ✅/❌ Maybe               | ✅ Yes                    | Very rich individuals skip income question |
| **Listwise Deletion** | N/A                       | N/A                       | Drop participant with any missing value    |
| **Pairwise Deletion** | N/A                       | N/A                       | Use partial data per analysis              |

## Related Notes

- [Pandas: Handling Missing Data](../python-foundations/pandas/missing-data.md): pandas-based detection, fill, interpolation, and imputation workflow
- [Missing Data in R](../r-foundations/missing-data.md): R and `naniar` oriented missingness workflow
- [Data Quality](../statistics/descriptive-statistics/data-quality.md): broader pre-model checks beyond missingness alone
