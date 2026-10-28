[Machine Learning](../README.md) › [模型評估](README.md) › 混淆矩陣指標

# 混淆矩陣指標 (Confusion Matrix Metrics)

混淆矩陣把分類結果拆成四格，所有分類指標都是從這四格算出來的。指標都依賴一個**閾值**（預設 0.5），換閾值就換一組數字，見 [閾值與校準](classification-thresholds-and-calibration.md)。

## 混淆矩陣

|  | 預測陰性 | 預測陽性 |
| --- | --- | --- |
| **實際陰性** | TN（真陰性） | FP（偽陽性，第一型錯誤） |
| **實際陽性** | FN（偽陰性，第二型錯誤） | TP（真陽性） |

sklearn `confusion_matrix` 的排列就是這樣：列 = 實際、欄 = 預測、類別依標籤值排序（0 在前）。

## 指標

| 指標 | 公式 | 問的問題 | 也叫 |
| --- | --- | --- | --- |
| Accuracy | (TP+TN) / 全部 | 整體猜對多少？ | — |
| Recall | TP / (TP+FN) | 真正的陽性抓到多少？ | **Sensitivity（敏感度）**、TPR |
| Specificity | TN / (TN+FP) | 真正的陰性排除多少？ | TNR（特異度） |
| Precision | TP / (TP+FP) | 預測為陽性的有多少是真的？ | **PPV（陽性預測值）** |
| NPV | TN / (TN+FN) | 預測為陰性的有多少是真的？ | 陰性預測值 |
| FPR | FP / (FP+TN) | 陰性被誤判的比例 | 1 − specificity |
| F1 | $2 \cdot \frac{P \cdot R}{P + R}$ | Precision 與 recall 的調和平均 | — |
| Balanced accuracy | (recall + specificity) / 2 | 不受類別比例影響的 accuracy | — |
| MCC | $\frac{TP \cdot TN - FP \cdot FN}{\sqrt{(TP+FP)(TP+FN)(TN+FP)(TN+FN)}}$ | 四格都用上的相關係數，−1 到 1 | Matthews correlation coefficient |

> **Sensitivity / specificity 不隨盛行率改變；precision (PPV) / NPV 會**。同一個篩檢工具，在盛行率 1% 的一般族群與 30% 的轉診族群中，PPV 差很多（見 [貝氏定理](../../statistics/probability-and-distributions/probability-basics.md#貝氏定理-bayes-theorem)）。

## 範例

乳癌資料（1 = 惡性，盛行率 37%），標準化 + 邏輯斯迴歸，測試集 171 筆：

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (confusion_matrix, classification_report, ConfusionMatrixDisplay,
                             balanced_accuracy_score, matthews_corrcoef)

X, y = load_breast_cancer(return_X_y=True)
y = 1 - y                      # 原始資料 0 = 惡性；改成 1 = 惡性，讓「陽性」= 我們要抓的類別
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X_train, y_train)
y_pred = model.predict(X_test)

confusion_matrix(y_test, y_pred)
# [[106   1]     TN  FP
#  [  4  60]]    FN  TP
classification_report(y_test, y_pred, digits=3)
#               precision  recall  f1-score  support
#            0      0.964   0.991     0.977      107
#            1      0.984   0.938     0.960       64
#     accuracy                        0.971      171
#    macro avg      0.974   0.964     0.968      171
# weighted avg      0.971   0.971     0.971      171
balanced_accuracy_score(y_test, y_pred)    # 0.964
matthews_corrcoef(y_test, y_pred)          # 0.938
ConfusionMatrixDisplay.from_predictions(y_test, y_pred)
```

判讀：64 個惡性中漏了 4 個（recall 0.938），107 個良性只誤判 1 個（specificity 0.991）。若漏診代價高，應[降低閾值](classification-thresholds-and-calibration.md)換取更高 recall。

`classification_report` 中類別 1 那列的 recall 就是 sensitivity，類別 0 那列的 recall 就是 specificity。

## 怎麼選指標

| 情境 | 優先看 |
| --- | --- |
| 漏掉陽性代價高（篩檢、診斷、詐欺） | Recall / sensitivity |
| 誤報代價高（垃圾郵件、昂貴的後續檢查） | Precision |
| 兩者都重要、正類稀少 | F1、PR-AUC、MCC |
| 類別比例會改變（換族群） | Sensitivity / specificity |
| 類別平衡、錯誤代價相近 | Accuracy 即可 |
| 多類別、每類同等重要 | **macro** 平均 |
| 多類別、依樣本數加權 | weighted 平均（會被多數類別主導，**不適合**評估不平衡資料中的少數類別） |

> Accuracy 在 [不平衡資料](class-imbalance.md) 上會誤導：正類 5% 時全猜陰性也有 95%。
