# Chi-square Tests

The **Chi-square test** is used to determine whether there is a significant association between categorical variables, or whether observed frequencies differ from expected frequencies.  
Chi-square ($\chi^2$) statistics are always non-negative (≥ 0) and tests are always **right-tailed**.

## Assumptions

- Data must be **counts or frequencies** (not percentages or continuous values).
- Observations must be **independent**.
- Expected frequencies should be sufficiently large:

$$
n \cdot \hat{p} \geq 5 \quad \text{and} \quad n \cdot (1-\hat{p}) \geq 5
$$

- n: Total number of observations
- $\hat{p}$: The proportion of “successes” observed in your data

## Chi-square Test of Independence

- **Purpose:** Test association between two categorical variables.
- **Null hypothesis (H₀):** The two variables are independent.
- **Alternative hypothesis (Hₐ):** The two variables are not independent (association exists).
- **Degrees of freedom:**

$$
(rows - 1) \times (columns - 1)
$$

### Python Example

```python
from scipy.stats import chi2_contingency
import numpy as np
import pandas as pd

# Example: SNP genotype (AA, AG, GG) vs. chemotherapy response (Responder/Non-responder)

data = np.array([[30, 20],   # AA genotype: responder/non-responder
                 [25, 25],   # AG genotype
                 [15, 30]])  # GG genotype

df = pd.DataFrame(data, columns=["Responder", "Non-responder"], index=["AA", "AG", "GG"])

chi2_stat, p_value, dof, expected = chi2_contingency(data)
print("Chi2 Statistic:", chi2_stat)
print("p-value:", p_value)
print("Degrees of freedom:", dof)
print("Expected frequencies:", expected)
```

### Limitations in Clinical Research

While Chi-square tests are widely used, they are not always appropriate in biomedical studies involving genetic and clinical outcomes:

- **Fixed variables vs. dynamic outcomes**: Germline SNPs (genetic variants that do not change over time) should not be directly tested against dynamic clinical outcomes such as cancer stage using Chi-square, as cancer stage evolves due to multiple confounding factors (treatment, follow-up time, comorbidities).

- **Better approaches**: For genetic association studies, regression models (e.g., logistic regression for incidence, Cox regression for survival outcomes) are more appropriate as they allow adjustment for covariates such as age, sex, and stage.

- **Proper endpoints**: Chi-square is best suited for binary or categorical clinical endpoints such as treatment response (responder vs. non-responder), recurrence (yes/no), or mortality status at a specific follow-up time.

## Chi-square Test for Homogeneity

- **Purpose:** Tests whether **proportions are the same across different populations**.
- **Null hypothesis (H₀):** Proportions are equal across groups.
- **Alternative hypothesis (Hₐ):** At least one group has different proportions.

- **Difference from independence test:**

| Feature                     | **Chi-square Test of Independence**                                                        | **Chi-square Test for Homogeneity**                                                                        |
| --------------------------- | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| **Purpose**                 | Tests whether **two categorical variables** are associated within a **single population**. | Tests whether **one categorical variable** has the **same distribution** across **different populations**. |
| **Design type**             | One population, two variables measured on each subject.                                    | Multiple populations, one variable measured per population.                                                |
| **Question asked**          | “Are genotype and treatment response related in these samples?”                            | “Do treatment and control groups have the same response rates?”                                            |
| **Example dataset**         | One cohort with two attributes (e.g., genotype × response).                                | Separate groups (e.g., treatment vs control) compared on one outcome.                                      |
| **Statistical computation** | Same χ² statistic formula and degrees of freedom.                                          | Same χ² statistic formula and degrees of freedom.                                                          |

### Python Example:

```python
import numpy as np
from scipy.stats import chi2_contingency

# Example: treatment vs control group responses
data = np.array([[30, 20],   # Treatment group: success/failure
                 [25, 25]])  # Control group: success/failure

chi2_stat, p_value, dof, expected = chi2_contingency(data)
print("Chi2 Statistic:", chi2_stat)
print("p-value:", p_value)
print("Expected frequencies:\n", expected)
```

## Chi-square Goodness-of-Fit

- **Purpose:** Tests whether the observed frequency distribution of a categorical variable matches a hypothesized distribution.
- **Null hypothesis (H₀):** The observed frequencies fit the expected distribution.
- **Alternative hypothesis (Hₐ):** The observed frequencies do not fit the expected distribution.
- **Degrees of freedom:**

$$
number of categories - 1
$$

### Python Example

```python
from scipy.stats import chisquare
import numpy as np

observed = np.array([11, 9, 10, 12, 8, 10])
expected = np.array([10, 10, 10, 10, 10, 10])

chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected)
print("Chi2 Statistic:", chi2_stat, "p-value:", p_value)
```
