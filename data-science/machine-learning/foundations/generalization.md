[Machine Learning](../README.md) › [基礎概念](README.md) › 泛化

# 泛化 (Generalization)

泛化是模型在**沒看過的新資料**上維持表現的能力。機器學習的目標不是記住訓練資料，驗證集與測試集分數只是「未來真實表現」的代理指標。

## 三種誤差

| 誤差 | 用哪些資料算 | 用途 |
| --- | --- | --- |
| 訓練誤差 (training error) | 拿來配適模型的資料 | 檢查模型有沒有學到東西；**一定偏樂觀** |
| 驗證誤差 (validation error) | 用於選模型、調參的資料 | 模型選擇；因為被拿來挑選，也會略偏樂觀 |
| 測試誤差 (test error) | 最後才碰、只用一次的資料 | 回報最終效能 |

樣本內 (in-sample) 表現指在看過的資料上；樣本外 (out-of-sample) 表現指在沒看過的資料上。統計上的對應是訓練 R² vs 測試 R²，見 [多元迴歸](../../statistics/multivariate-analysis/multiple-regression.md)。

## 判讀

| 訓練誤差 | 驗證 / 測試誤差 | 診斷 |
| --- | --- | --- |
| 低 | 高 | [過擬合](overfitting-underfitting.md) |
| 高 | 高（與訓練接近） | [欠擬合](overfitting-underfitting.md) |
| 低 | 低且與訓練接近 | 健康 |
| — | 驗證很好、測試或上線很差 | 驗證設計有問題：[資料洩漏](data-leakage.md)、分布偏移、對驗證集過度調參 |

## 影響泛化的因素

| 因素 | 說明 | 對策 |
| --- | --- | --- |
| 模型複雜度 | 太複雜會記住雜訊 | [正則化](regularization.md)、限制深度、early stopping |
| 樣本數 | 樣本少時變異大；p ≫ n 時尤其嚴重 | 更多資料、更簡單的模型，見 [高維小樣本](high-dimensional-data.md) |
| 資料雜訊 | 雜訊設定了誤差下限 | 改善量測與標註品質 |
| [資料洩漏](data-leakage.md) | 驗證分數虛高 | Pipeline、正確切分 |
| 訓練與部署分布不同 | 換醫院、換定序平台、換時間 | 外部驗證、[監控](../production/deployment-and-monitoring.md)，見 [抽樣與代表性](sampling-and-representativeness.md) |
| 特徵品質 | 爛特徵靠複雜模型也救不回來 | [特徵工程](feature-engineering-principles.md) |

> **內部驗證 vs 外部驗證**：同一批資料切出來的測試集只代表「同一來源」的泛化。生醫模型要宣稱可用，通常需要另一家醫院、另一個 cohort 或另一個批次的**外部驗證 (external validation)**。

## 實務原則

- 隨時問：驗證設定是否像模型真正被使用的情境？
- 用 [交叉驗證](../workflow/cross-validation.md) 讓估計更穩定，測試集只在最後用一次。
- 改善特徵品質，比一味增加模型複雜度有效。
