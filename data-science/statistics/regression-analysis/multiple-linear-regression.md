[Statistics](../README.md) › [迴歸分析](README.md) › 多元線性迴歸

# 多元線性迴歸 (Multiple Linear Regression)

把簡單迴歸擴展到**兩個以上的預測變數**，可以同時控制多個因子，評估每個變數的**獨特貢獻**。

$$
Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \cdots + \beta_k X_k + \varepsilon
$$

> **偏迴歸係數 (partial coefficient)** βⱼ：在**其他變數固定不變**下 (holding others constant / ceteris paribus)，Xⱼ 增加 1 單位時 Y 的平均變化。
>
> 加入新變數後係數變很多、甚至變號，通常代表原本的簡單迴歸被**干擾 (confounded)**，而不是軟體出錯。

## Python 範例

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.datasets import load_iris

df = load_iris(as_frame=True).frame
df.columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", "target"]

model = smf.ols("petal_length ~ sepal_length + sepal_width + petal_width", data=df).fit()
model.summary()
model.rsquared, model.rsquared_adj, model.aic, model.bic
```

| 變數 | 係數 | SE | p | 解讀（控制其他變數下） |
| --- | --- | --- | --- | --- |
| sepal_length | 0.729 | 0.064 | < .001 | 花萼長 +1 cm → 花瓣長 +0.729 cm |
| sepal_width | −0.648 | 0.067 | < .001 | 花萼寬 +1 cm → 花瓣長 −0.648 cm |
| petal_width | 1.447 | 0.065 | < .001 | 花瓣寬 +1 cm → 花瓣長 +1.447 cm |

**輸出要一起讀**：係數（方向與大小）、95% CI（精確度）、p 值、R² / 調整 R²、殘差圖。

## 解釋 vs 預測

| 目的 | 工具 | 重視 |
| --- | --- | --- |
| 解釋 / 推論 | `statsmodels` | 係數、SE、p 值、CI |
| 預測 | `sklearn` | 測試集誤差、交叉驗證、pipeline |

```python
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import statsmodels.api as sm

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
res = sm.OLS(y_train, sm.add_constant(X_train)).fit()   # 推論：只看訓練資料
r2_score(y_test, res.predict(sm.add_constant(X_test)))  # 預測：一定要在測試集評估
```

> 訓練 R² 永遠偏樂觀（模型越複雜越高）；測試 R² 才代表泛化能力，見 [ML：泛化](../../machine-learning/foundations/generalization.md)。預測變數很多（p > n）時改用 [正則化](../../machine-learning/foundations/regularization.md)，見 [高維小樣本](../../machine-learning/foundations/high-dimensional-data.md)。

## R² vs 調整後 R² (Adjusted R²)

加任何變數（即使無意義）R² 都**只會上升**。調整後 R² 會懲罰沒貢獻的變數：

$$
R^2_{adj} = 1 - \frac{(1-R^2)(n-1)}{n-k-1}
$$

| 模型 | 變數數 | R² | 調整 R² |
| --- | --- | --- | --- |
| 1 | 1 | 0.80 | **0.79** ← 較好 |
| 2 | 10 | 0.85 | 0.75 |

比較變數數不同的模型時用調整 R²、AIC / BIC，或更好的是**測試集 / 交叉驗證誤差**。

## 類別預測變數：虛擬編碼 (Dummy Coding)

k 個類別 → 建立 **k − 1** 個虛擬變數，省略的類別為**參考組 (reference group)**。全放 k 個會造成完全共線性（dummy variable trap）。

```python
smf.ols("petal_length ~ sepal_length + C(target)", data=df).fit()
# C(target)[T.1] = versicolor 與 setosa（參考組）的差
smf.ols("y ~ C(group, Treatment(reference='control'))", data=d)   # 指定參考組
```

R 中 `lm(y ~ species + 0)` 移除截距後，每個係數就是各組的平均，而不是與參考組的差。

## 交互作用 (Interaction)

```python
smf.ols("y ~ dose * genotype", data=d)   # = dose + genotype + dose:genotype
```

交互作用顯著時，dose 的效果**取決於** genotype，不能只報單一的 dose 係數。概念同 [二因子 ANOVA](../inferential-statistics/two-way-anova.md)。

## 多重共線性 (Multicollinearity)

預測變數彼此高度相關。**不太影響預測準確度**，但讓個別係數不穩定：SE 變大、符號反直覺、顯著性不可靠。

$$
\text{VIF}_j = \frac{1}{1-R_j^2}, \quad R_j^2 = X_j \text{ 對其他 X 迴歸的 } R^2
$$

| VIF | 解讀 |
| --- | --- |
| 1 | 無共線性 |
| 1–5 | 可接受 |
| 5–10 | 需注意 |
| > 10 | 嚴重 |

```python
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

X = sm.add_constant(df[["sepal_length", "sepal_width", "petal_width"]])
pd.Series([variance_inflation_factor(X.values, i) for i in range(1, X.shape[1])], index=X.columns[1:])
```

| 對策 | 時機 |
| --- | --- |
| 移除其一 | 兩者測量幾乎相同的東西 |
| 合併成綜合指標 / [PCA](../multivariate-analysis/pca.md) | 兩者都有資訊 |
| [Ridge / Lasso](../../machine-learning/foundations/regularization.md) | 變數多，重視預測 |

## 遺漏變數偏誤 (Omitted Variable Bias)

比共線性更危險的是**漏掉重要變數**：若某變數同時影響 Y 與某個已放入的 X，那個 X 的係數就會有偏。迴歸只能控制「有測量且有放入」的變數；「其他條件不變」的強度不會超過資料與設計允許的程度。見 [干擾與偏誤](../experimental-design/confounding-bias.md)。

## 變數選擇

| 方法 | 評價 |
| --- | --- |
| 領域知識 + 事先指定 | **首選**，尤其是以解釋為目的 |
| AIC / BIC 比較候選模型 | 好（AIC 偏預測、BIC 偏精簡），見 [最大概似估計](../probability-and-distributions/maximum-likelihood.md#用-likelihood-比較模型) |
| Lasso / 交叉驗證 | 變數多、以預測為目的 |
| 逐步選擇 (stepwise) | **不建議**：模型不穩定、p 值與 CI 失真、易過擬合 |

## 標準化係數與轉換變數

- **標準化係數**：先把 X 做 z-score，係數變成「X 增加 1 SD 時 Y 的變化」，可粗略比較相對重要性，但不取代原始單位的解讀。
- **轉換後的預測變數**（`I(x**3)`、`np.log(x)`）仍是線性模型，但係數意義改變：

| 模型 | β₁ 的解讀 |
| --- | --- |
| `y ~ x` | x +1 → y + β₁ |
| `np.log(y) ~ x` | x +1 → y 約變為 $e^{\beta_1}$ 倍（≈ +100·β₁ %） |
| `y ~ np.log(x)` | x 增加 1% → y + β₁/100 |
| `np.log(y) ~ np.log(x)` | x 增加 1% → y 約增加 β₁ %（彈性 elasticity） |

## 假設與診斷

同 [簡單線性迴歸的 LINE](simple-linear-regression.md#假設line針對殘差)，再加上**無嚴重共線性**。完整的診斷流程（部分迴歸圖、異質變異檢定、影響點）見 [多變量：假設與診斷](../multivariate-analysis/assumptions-diagnostics.md)。

## 係數圖 (Coefficient Plot)

```python
import matplotlib.pyplot as plt

coefs = model.params.drop("Intercept")
ci = model.conf_int().drop("Intercept")
plt.errorbar(coefs, coefs.index, xerr=[coefs - ci[0], ci[1] - coefs], fmt="o", capsize=5)
plt.axvline(0, color="red", ls="--")
plt.xlabel("Coefficient (95% CI)"); plt.show()
```

CI 跨過 0 → 在 5% 水準下不顯著。
