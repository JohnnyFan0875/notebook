[Data Science](../README.md) › Machine Learning

# 機器學習 (Machine Learning)

以「從問題到部署」的工作流程整理機器學習，而不是只羅列演算法。

> 只記演算法名稱、沒有先建立驗證設計與資料洩漏 (data leakage) 的觀念，很容易得到「分數漂亮但不能用」的模型。好的流程是：**定義問題 → 切對資料 → 建 baseline → 在 pipeline 內前處理與調參 → 用對的指標評估 → 監控**。

**找方法**：不知道該用哪個模型、指標或驗證方式時，先看 [ML 方法速查](model-selection.md)。

## 模組

| 模組 | 核心內容 | 回答的問題 |
| --- | --- | --- |
| [基礎概念](foundations/README.md) | 泛化、損失函數、bias-variance、正則化、資料洩漏、高維資料 | 為什麼訓練分數高不代表模型好？ |
| [工作流程](workflow/README.md) | 問題定義、資料切分、交叉驗證、pipeline、調參 | 怎麼設計一個不會騙自己的實驗流程？ |
| [前處理](preprocessing/README.md) | 缺失值、編碼、縮放、離群值、特徵選擇 | 原始資料要怎麼變成模型能用的輸入？ |
| [監督式學習](supervised-learning/README.md) | 迴歸、分類、集成方法 | 有標籤時該用哪個模型？ |
| [非監督式學習](unsupervised-learning/README.md) | 分群、降維、異常偵測、關聯規則 | 沒有標籤時能找出什麼結構？ |
| [推薦系統](recommender-systems/README.md)（選讀） | 協同過濾、ALS、隱式回饋 | 怎麼從使用者行為推薦項目？ |
| [模型評估](evaluation/README.md) | 指標、閾值、校準、類別不平衡、錯誤分析 | 模型到底好不好？好在哪、錯在哪？ |
| [可解釋性與診斷](interpretability-and-diagnostics/README.md) | 特徵重要性、模型診斷 | 模型依據什麼做預測？可信嗎？ |
| [上線與維運](production/README.md) | 部署、監控、漂移、MLflow | 模型上線後怎麼維持品質？ |
| [套件](packages/README.md) | scikit-learn、statsmodels | 特定套件怎麼用？ |

## 建議路線

| 讀者 | 路線 |
| --- | --- |
| 初學 | 基礎概念 → 工作流程 → 前處理 → 監督式 / 非監督式學習 → 模型評估 → 可解釋性 → 上線與維運 |
| **生物資訊** | [資料洩漏](foundations/data-leakage.md) → [高維小樣本](foundations/high-dimensional-data.md) → [交叉驗證（Group / Nested CV）](workflow/cross-validation.md) → [Pipeline](workflow/pipeline-basic.md) → [正則化](foundations/regularization.md) → [類別不平衡](evaluation/class-imbalance.md) → [降維](unsupervised-learning/dimensionality-reduction/README.md) / [分群](unsupervised-learning/clustering/README.md) → [可解釋性](interpretability-and-diagnostics/model-interpretability.md) |
| 統計背景 | [損失函數（↔ MLE）](foundations/loss-functions.md) → [Bias-Variance](foundations/bias-variance-tradeoff.md) → [正則化（↔ 先驗）](foundations/regularization.md) → [交叉驗證](workflow/cross-validation.md) → [集成方法](supervised-learning/ensemble/README.md) → [statsmodels](packages/statsmodels/README.md) |

## 名詞對照

| ML | 統計 | 說明 |
| --- | --- | --- |
| 特徵 (feature) | 自變數、預測變數、解釋變數 | 輸入 X |
| 目標 (target) / 標籤 (label) | 依變數、反應變數 | 輸出 y；label 指監督式學習中已觀測到的 y |
| 訓練 (training) | 配適 (fitting)、估計 | 找出參數 |
| 損失函數 (loss) | 負 log-likelihood | 見 [損失函數](foundations/loss-functions.md) |
| 正則化 (regularization) | 收縮 (shrinkage)、先驗 | 見 [正則化](foundations/regularization.md) |
| 超參數 (hyperparameter) | 調整參數 (tuning parameter) | 訓練前就決定的設定，如 `alpha`、`max_depth`、`n_neighbors` |
| 泛化誤差 (generalization error) | 預測誤差、樣本外誤差 | 見 [泛化](foundations/generalization.md) |

## 四條貫穿全程的規則

| 規則 | 為什麼 |
| --- | --- |
| 先切資料，再 fit 任何前處理 | scaler、imputer、encoder、特徵選擇在全資料上 fit 就是洩漏 |
| 驗證方式要符合資料結構 | 分組、時間序列、重複量測不能隨機切 |
| 測試集只用一次 | 反覆看測試集等於拿它調參 |
| 先和簡單 baseline 比 | 沒有基準就無法判斷複雜模型是否真的有進步 |
