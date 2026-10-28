[Machine Learning](../../README.md) › [監督式學習](../README.md) › [分類](README.md) › Naive Bayes

# 單純貝氏 (Naive Bayes)

用 [貝氏定理](../../../statistics/bayesian-statistics/bayes-theorem.md) 計算「給定特徵時屬於各類別的機率」，並**假設所有特徵在給定類別下彼此獨立**。這個假設幾乎從不成立，但模型極快、需要的資料很少，在文字與計數資料上常是很強的 baseline。

$$
P(y \mid x_1, \dots, x_p) \propto P(y) \prod_{j=1}^{p} P(x_j \mid y)
$$

## 三種變體

| sklearn | $P(x_j \mid y)$ 的假設 | 適合的資料 |
| --- | --- | --- |
| `GaussianNB` | 常態分配 | 連續特徵 |
| `MultinomialNB` | 多項分配（計數） | 詞頻、**k-mer 計數** |
| `ComplementNB` | Multinomial 的變體 | 類別不平衡的文字資料 |
| `BernoulliNB` | 0 / 1 | 詞是否出現、突變是否存在 |
| `CategoricalNB` | 類別分配 | 類別特徵 |

## 用法

```python
import numpy as np
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score

# 1. 連續特徵：承乳癌範例
cross_val_score(GaussianNB(), X_train, y_train, cv=cv, scoring="roc_auc").mean()    # 0.982

# 2. DNA 序列 → 3-mer 計數 → MultinomialNB
#    序列 A 類富含 A/T、B 類富含 C/G（各 100 條、長 200）
kmer_nb = make_pipeline(CountVectorizer(analyzer="char", ngram_range=(3, 3), lowercase=False),
                        MultinomialNB(alpha=1.0))      # alpha = Laplace 平滑，避免沒見過的 k-mer 機率為 0
cross_val_score(kmer_nb, np.array(seqs), labels, cv=cv).mean()                      # 1.0（64 個 3-mer 特徵）
```

## 優缺點

| 優點 | 缺點 |
| --- | --- |
| 訓練與預測極快，可線上更新（`partial_fit`） | 獨立性假設不成立時，**機率極端且失準**（常需 [校準](../../evaluation/classification-thresholds-and-calibration.md#校準-calibration)） |
| 樣本少也能用 | 相關特徵的證據被重複計算 |
| 高維稀疏資料（文字、k-mer）表現好 | `GaussianNB` 假設每個特徵在各類別內為常態 |
| 不需縮放 | 通常不是最準的模型 |

> 排序能力（AUC）常不錯，但機率不可信：乳癌資料上 `GaussianNB` 的 AUC 0.996 與邏輯斯迴歸相當，Brier score 卻差了約 3 倍（0.056 vs 0.019）。

生資應用：序列分類（RDP Classifier 用 8-mer + Naive Bayes 做 16S rRNA 的分類學指派）、快速的文字探勘 baseline。
