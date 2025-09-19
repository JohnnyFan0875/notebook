multivariate regression
multiple regression
Y=β0​+β1​X1​+β2​X2​+ϵ
how to evaluate β and p-value

---

import statsmodels.api as sm
sm.OLS(y, x).fit()

pd.ols(y, x)

from scipy import stats
stats.linregress(x, y)

np.polyfit(x, y, deg=1)

import statsmodels.api as sm
df['SPX_Ret'] = df['SPX_Prices'].pct_change()
df['R2000_Ret'] = df['R2000_Prices'].pct_change()
df = sm.add_constant(df)

results = sm.OLS(df['R2000_Ret'],df[['const','SPX_Ret']]).fit()

results.params[0]
results.params[1]

# Question

When using a regression model to test the relationship between postpartum meal consumption and breastmilk parabens, what does it mean if we add the variable **postpartum days (≤7 days vs. >7 days)** to the model and obtain different significance results?

---

## Scenario 1

- Postpartum meal (V) → significant
- Postpartum meal + postpartum days (V, V) → both significant

**Interpretation**  
Both postpartum meal and postpartum days have independent effects on the outcome.  
Even when both variables are included in the model, their effects remain.

**Conclusion**: Both are **independent predictors**.

---

## Scenario 2

- Postpartum meal (V) → significant
- Postpartum meal + postpartum days (V, V) → postpartum meal not significant, postpartum days significant

**Interpretation**  
The effect of postpartum meal disappears because postpartum days explains the relationship between postpartum meal and the outcome.  
In other words, the observed association between postpartum meal and outcome is due to postpartum days acting as a **confounding factor**.

**Conclusion**: Postpartum days is the true predictor; postpartum meal is not an independent predictor.

---

## Scenario 3

- Postpartum meal (V) → significant
- Postpartum meal + postpartum days (V, V) → neither significant

**Interpretation**  
When both variables are included in the model, explanatory power is dispersed.  
This usually indicates **high collinearity** between the two variables and possibly insufficient sample size, which reduces statistical power.

**Conclusion**: Postpartum meal and postpartum days may be highly correlated, making it difficult to distinguish their independent effects.

---

## Scenario 4

- Postpartum meal (V) → not significant
- Postpartum meal + postpartum days (V, V) → postpartum days significant

**Interpretation**  
Postpartum meal alone has no effect; after adding postpartum days, only postpartum days remains significant.

**Conclusion**: Postpartum days is the main predictor; postpartum meal has no effect.

---

## Scenario 5

- Postpartum meal (V) → not significant
- Postpartum meal + postpartum days (V, V) → both significant

**Interpretation**  
Postpartum meal is not significant when examined alone, but becomes significant when controlling for postpartum days.  
This indicates that **postpartum days is a suppressor variable**:  
it accounts for hidden variation, allowing the effect of postpartum meal to emerge.

**Conclusion**: Both have effects, but the effect of postpartum meal is only visible after controlling for postpartum days.

---

## Scenario 6

- Postpartum meal (V) → not significant
- Postpartum meal + postpartum days (V, V) → postpartum meal significant, postpartum days not significant

**Interpretation**  
Postpartum meal alone shows no association with the outcome; however, when controlling for postpartum days, postpartum meal becomes significant while postpartum days is no longer significant.  
This reflects a **suppressor effect**, meaning postpartum days absorbs noise, allowing the true effect of postpartum meal to become apparent.

**Conclusion**: Postpartum meal may be the main predictor, but its effect only becomes clear after controlling for postpartum days.

## test homogeneity of variance

- variance of the residuals (the difference between observed and predicted values) is constant across all levels of the independent variables
- H₀: variance of the residuals (errors) from the regression model is constant

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target
X = df.drop('target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

train_data = X_train.copy()
train_data['target'] = y_train

logit_model = smf.logit('target ~ ' + ' + '.join(X_train.columns), data=train_data)
logit_result = logit_model.fit()

y_pred = logit_result.predict(X_train)  # predicted probabilities
residuals = y_train - y_pred  # residuals (actual - predicted)

bp_test = sms.het_breuschpagan(residuals, X_train)
bp_test_statistic, bp_test_p_value, _, _ = bp_test
```
