# Missing Data Mechanisms

Missing data can be classified into three categories based on the relationship between the missingness and the observed/unobserved data. Understanding these mechanisms is crucial for selecting appropriate statistical methods for handling missing data.

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

- **Implication:**

  - Standard imputation methods assuming MAR may lead to **biased estimates**.
  - Requires **specialized modeling**, such as selection models or pattern-mixture models.

- **Example:**

  - Patients with severe depression are less likely to complete a mental health questionnaire (severity is unobserved if missing).
  - Individuals with very high income are less likely to report it in a survey.

### **Summary Table**

| Mechanism | Depends on Observed Data? | Depends on Missing Value? | Example                                    |
| --------- | ------------------------- | ------------------------- | ------------------------------------------ |
| **MCAR**  | ❌ No                     | ❌ No                     | Random machine failure in lab              |
| **MAR**   | ✅ Yes                    | ❌ No                     | Older patients skip weight question        |
| **MNAR**  | ✅/❌ Maybe               | ✅ Yes                    | Very rich individuals skip income question |
