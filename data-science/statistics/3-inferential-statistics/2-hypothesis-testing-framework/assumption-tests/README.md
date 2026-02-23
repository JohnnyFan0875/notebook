# Assumption Tests

All inferential tests are valid only if their underlying assumptions hold.  
Failure to meet these assumptions affects both the Type I error rate (false positives) and statistical power.  
Before running a hypothesis test, data must meet specific assumptions:

| Assumption                                         | Why it matters                                        | Typical test             |
| -------------------------------------------------- | ----------------------------------------------------- | ------------------------ |
| [**Normality**](./normality-tests.md)              | Ensures accurate p-values for parametric tests.       | Shapiro–Wilk, K–S        |
| [**Homogeneity of variance**](./variance-tests.md) | Ensures fair comparison across groups.                | Levene, Bartlett         |
| [**Independence**](./independence-test.md)         | Prevents bias due to repeated or correlated measures. | Durbin–Watson, Runs test |

These diagnostics ensure test validity. If assumptions fail, use robust or nonparametric alternatives.
