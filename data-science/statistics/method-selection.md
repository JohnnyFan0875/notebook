[Statistics](README.md) › 統計方法速查

# 統計方法速查 (Method Selection Guide)

依「結果變數型態」與「研究問題」快速找到方法，點連結看細節。

## 1. 比較組別

| 結果變數 | 設計 | 母數方法 | 無母數 / 替代 |
| --- | --- | --- | --- |
| 連續 | 1 組 vs 已知值 | [單一樣本 t](inferential-statistics/statistical-tests.md#t-檢定) | [Wilcoxon signed-rank](nonparametric-methods/one-sample-and-paired.md) |
| 連續 | 2 組獨立 | [Welch t](inferential-statistics/statistical-tests.md#t-檢定) | [Mann-Whitney U](nonparametric-methods/two-independent-samples.md) |
| 連續 | 2 組配對 / 前後測 | [配對 t](inferential-statistics/statistical-tests.md#t-檢定) | [Wilcoxon signed-rank](nonparametric-methods/one-sample-and-paired.md) |
| 連續 | 3+ 組獨立 | [單因子 ANOVA](inferential-statistics/one-way-anova.md) → [Tukey](inferential-statistics/post-hoc-effect-size.md) | [Kruskal-Wallis](nonparametric-methods/kruskal-wallis.md) → Dunn |
| 連續 | 兩個因子 | [二因子 ANOVA](inferential-statistics/two-way-anova.md) | 迴歸 + 交互作用 |
| 連續 | 3+ 次重複量測 | [重複量數 ANOVA](inferential-statistics/repeated-measures-anova.md) | [混合效應模型](regression-analysis/mixed-effects-models.md)、[Friedman](nonparametric-methods/kruskal-wallis.md#friedman-檢定重複量測) |
| 二元 / 比例 | 2 組 | [兩比例 z](inferential-statistics/statistical-tests.md#比例檢定) | [Fisher's exact](nonparametric-methods/chi-square.md) |
| 二元 | 配對 | — | [McNemar](nonparametric-methods/chi-square.md) |
| 類別 | r × c 交叉表 | [卡方獨立性](nonparametric-methods/chi-square.md) | Fisher's exact |
| 計數 | 2+ 組 | [Poisson / 負二項 GLM](regression-analysis/glm-count-models.md) | — |
| 存活時間 | 2+ 組 | [Log-rank](survival-analysis/log-rank-test.md) | 加權 log-rank、RMST |
| 任意統計量 | — | — | [置換檢定、Bootstrap](probability-and-distributions/monte-carlo-simulation.md) |

## 2. 變數之間的關係 / 建模

| 結果變數 Y | 模型 | 係數解讀 |
| --- | --- | --- |
| 連續 | [線性迴歸](regression-analysis/multiple-linear-regression.md) | Y 的差 |
| 二元 | [邏輯斯迴歸](regression-analysis/logistic-regression.md) | Odds ratio |
| 有序類別 | 順序邏輯斯迴歸 | Cumulative odds ratio |
| 計數 | [Poisson / 負二項](regression-analysis/glm-count-models.md) | Rate ratio |
| 存活時間（有設限） | [Cox](survival-analysis/cox-ph-model.md)、[AFT](survival-analysis/parametric-models.md) | Hazard ratio、時間比 |
| 群集 / 重複量測 | [混合效應模型](regression-analysis/mixed-effects-models.md)、GEE | 同上 + 隨機效應變異 |
| 時間序列 | [ARIMA / SARIMA](time-series-analysis/arima.md) | — |
| 預測變數很多 (p ≫ n) | [Ridge / Lasso / Elastic Net](multivariate-analysis/multiple-regression.md) | 收縮後的係數（不做一般推論） |
| 兩個連續變數的關聯強度 | [Pearson / Spearman / Kendall](descriptive-statistics/bivariate.md) | r、ρ、τ |

## 3. 結構探索（無結果變數）

| 目的 | 方法 |
| --- | --- |
| 降維、看整體結構 | [PCA](multivariate-analysis/pca.md) |
| 找群組 | [K-Means / 階層式 / DBSCAN](multivariate-analysis/clustering.md) |
| 監督式降維、視覺化類別分離 | [LDA](multivariate-analysis/logistic-lda.md) |
| 驗證潛在構念 | [SEM / CFA](multivariate-analysis/structural-equation-modeling-with-lavaan.md) |

## 4. 其他常見需求

| 需求 | 去哪裡 |
| --- | --- |
| 一次做很多檢定（基因、特徵） | [多重檢定校正（BH / FDR）](inferential-statistics/multiple-testing.md) |
| 決定樣本數 | [樣本數與檢定力](experimental-design/sample-size-power.md) |
| 檢查常態 / 等變異 / 獨立 | [假設檢查](inferential-statistics/assumption-checks.md) |
| 迴歸診斷 | [模型假設與診斷](multivariate-analysis/assumptions-diagnostics.md) |
| 估計值的不確定性沒有公式 | [Bootstrap](probability-and-distributions/monte-carlo-simulation.md#拔靴法-bootstrap) |
| 想要「參數的機率」 | [貝氏統計](bayesian-statistics/README.md) |
| 線上實驗 | [A/B 測試](experimental-design/ab-testing.md) |
| 控制干擾 / 批次效應 | [干擾、偏誤與效度](experimental-design/confounding-bias.md) |

## 選擇前的三個問題

1. **分析單位是什麼？** 觀測是否獨立？（重複量測、同一樣本多個細胞、同一批次）→ 不獨立就要配對 / 混合模型
2. **結果變數是什麼型態？** 連續、二元、計數、有序、存活時間
3. **目的是什麼？** 描述、推論（效果是否存在、多大）、還是預測
