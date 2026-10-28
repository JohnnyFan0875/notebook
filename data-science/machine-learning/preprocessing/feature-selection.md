[Machine Learning](../README.md) › [前處理](README.md) › 特徵選擇

# 特徵選擇 (Feature Selection)

從所有特徵中挑出子集合。目的不只是分數：較少的特徵代表較低的 [過擬合](../foundations/overfitting-underfitting.md) 風險、較少的上線資料依賴、較好的可解釋性與維護性。

> 一個稍簡單但穩定、好維護的模型，常比「多加十個欄位才多一點分數」更有價值。

## 三類方法

| 類型 | 做法 | 例子 | 速度 | 缺點 |
| --- | --- | --- | --- | --- |
| 過濾法 (filter) | 不看模型，用統計量逐一評分 | 變異數門檻、相關係數、F 檢定、卡方、互資訊 (mutual information) | 最快 | 忽略特徵間交互作用與冗餘 |
| 包裝法 (wrapper) | 反覆訓練模型、比較特徵子集合 | RFE、前向 / 後向逐步選擇 | 最慢 | 計算量大，容易對驗證資料過擬合 |
| 嵌入法 (embedded) | 訓練過程中順便選 | Lasso / L1、樹模型重要性 | 中 | 結果綁定特定模型 |

降維（[PCA](../unsupervised-learning/dimensionality-reduction/pca.md)）是**產生新特徵**，不是特徵選擇；選擇保留的是原始特徵，可解釋性較好。

## sklearn 工具

| 工具 | 類型 | 說明 |
| --- | --- | --- |
| `VarianceThreshold` | 過濾 | 刪除（近乎）常數的欄位；不用標籤 |
| `SelectKBest(f_classif / f_regression)` | 過濾 | 單變量 F 檢定 |
| `SelectKBest(chi2)` | 過濾 | 只適用**非負**特徵（計數、one-hot） |
| `SelectKBest(mutual_info_classif)` | 過濾 | 能抓非線性關係 |
| `RFE` / `RFECV` | 包裝 | 反覆刪除最不重要的特徵；`RFECV` 用 CV 決定保留幾個 |
| `SequentialFeatureSelector` | 包裝 | 前向 / 後向逐步選擇，以 CV 分數為準 |
| `SelectFromModel(L1 模型或樹)` | 嵌入 | 保留係數非 0 或重要性超過門檻的特徵 |

```python
from sklearn.datasets import load_breast_cancer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif, SelectFromModel, SequentialFeatureSelector, RFECV
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

X, y = load_breast_cancer(return_X_y=True, as_frame=True)     # 30 個特徵
y = 1 - y                                                      # 改成 1 = 惡性
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
cv = StratifiedKFold(5, shuffle=True, random_state=0)
clf = LogisticRegression(max_iter=1000)

# 選擇步驟一律放進 pipeline，CV 才會在每個 fold 內重新選
pipes = {
    "全部 30 個":   make_pipeline(StandardScaler(), clf),
    "F 檢定前 10":  make_pipeline(StandardScaler(), SelectKBest(f_classif, k=10), clf),
    "L1 嵌入":      make_pipeline(StandardScaler(),
                                  SelectFromModel(LogisticRegression(C=0.1, l1_ratio=1, solver="liblinear")), clf),
    "前向逐步 5 個": make_pipeline(StandardScaler(),
                                  SequentialFeatureSelector(clf, n_features_to_select=5,
                                                            direction="forward", scoring="roc_auc", cv=3), clf),
}
{k: cross_val_score(p, X_train, y_train, cv=cv, scoring="roc_auc").mean() for k, p in pipes.items()}
# 全部 0.992、F 檢定前 10 0.982、L1（保留 8 個）0.993、前向 5 個 0.991

# RFECV：用 CV 決定保留幾個特徵
rfecv = make_pipeline(StandardScaler(), RFECV(clf, cv=cv, scoring="roc_auc")).fit(X_train, y_train)
rfecv[-1].n_features_    # 17
```

這個例子裡，5–8 個特徵就能達到與 30 個幾乎相同的 AUC：很多特徵彼此高度相關（半徑、周長、面積）。

## 前向逐步選擇 (Forward Stepwise)

```
從空集合開始
  ↓
每輪把每個候選特徵試加進來 → 用 CV 指標（如 AUC）評分 → 加入最好的那個
  ↓
重複，直到提升很小、達到上限，或新增欄位的維護成本不值得
```

| 停止條件 | 說明 |
| --- | --- |
| 驗證指標不再明顯提升 | 搭配 CV 標準差判斷「明顯」 |
| 達到預設欄位上限 | 上線資料依賴的考量 |
| 新特徵與既有特徵重複表達同一件事 | 高相關欄位誰被選進來常是偶然 |
| 新特徵有時間洩漏風險或上線拿不到 | 見 [資料洩漏](../foundations/data-leakage.md) |

> 逐步選擇的評分**必須在驗證資料或 CV 上算**。在同一份訓練資料上 fit 再算 AUC，分數一定隨特徵增加而上升，選不出任何東西。

## 注意事項

| 注意 | 原因 |
| --- | --- |
| 選擇要放在 CV 迴圈內 | 在全資料上用標籤選特徵再 CV = 洩漏；p ≫ n 時純雜訊也能有 90%+ 準確率，見 [高維小樣本](../foundations/high-dimensional-data.md) |
| 選出的特徵清單不穩定 | 相關特徵可互換；換個子樣本選出的就不同。重要時用 bootstrap 看被選中頻率 |
| 重要性依方法與模型而異 | 不要把某個方法的排名當成真理，見 [可解釋性](../interpretability-and-diagnostics/model-interpretability.md) |
| 刪太多 → 欠擬合；留太多 → 過擬合 | 用 CV 決定數量 |
| 正則化本身就是軟性的特徵選擇 | 很多時候不必另外選，直接用 Lasso / Elastic Net，見 [正則化](../foundations/regularization.md) |
| 「預測重要」≠「差異顯著」 | 要回答「哪些基因有差異」是推論問題，用 [多重檢定校正](../../statistics/inferential-statistics/multiple-testing.md) |
