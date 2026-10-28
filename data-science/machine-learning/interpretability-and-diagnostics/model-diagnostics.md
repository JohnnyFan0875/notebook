[Machine Learning](../README.md) › [可解釋性與診斷](README.md) › 模型診斷

# 模型診斷 (Model Diagnostics)

確認模型真的在學合理的訊號，而不是剛好在某個切分上得到好分數。模型表現**異常地好**或**異常地差**時，診斷通常比換演算法更重要。

## 三個層次

| 層次 | 檢查 | 工具 |
| --- | --- | --- |
| 資料 | 欄位定義、缺失型態、分布、重複 / 近似重複列、train vs test 差異 | 描述統計、adversarial validation |
| 預測 | 分數分布、殘差、混淆矩陣、校準 | 殘差圖、`PredictionErrorDisplay`、`CalibrationDisplay` |
| 切片 | 不同群體、時間、地區、數值區間的誤差 | 見 [錯誤分析](../evaluation/baselines-and-error-analysis.md#錯誤分析-error-analysis) |

## 迴歸診斷

| 圖 / 檢查 | 看什麼 | 問題時 |
| --- | --- | --- |
| 預測 vs 實際 | 點是否貼近對角線 | 高值區系統性低估 → 缺非線性項或目標需轉換 |
| 殘差 vs 預測值 | 無結構、等寬 | 漏斗形 = 異質變異；曲線 = 漏掉非線性 |
| 殘差分布 | 是否有極端殘差 | 離群值，見 [離群值處理](../preprocessing/outlier-handling.md) |
| 影響點 (leverage / Cook's distance) | 少數點是否主導結果 | 見統計筆記 |
| 依預測區間分組的誤差 | 某區間特別差 | 考慮分段或換模型 |

```python
from sklearn.metrics import PredictionErrorDisplay

PredictionErrorDisplay.from_predictions(y_test, y_pred, kind="actual_vs_predicted")
PredictionErrorDisplay.from_predictions(y_test, y_pred, kind="residual_vs_predicted")
```

殘差圖的判讀型態、影響點與正式檢定見 [模型假設與診斷](../../statistics/multivariate-analysis/assumptions-diagnostics.md)。

## 分類診斷

| 檢查 | 筆記 |
| --- | --- |
| 混淆矩陣、各類別 recall | [混淆矩陣指標](../evaluation/confusion-metrics.md) |
| 不同閾值下的 precision / recall | [閾值與校準](../evaluation/classification-thresholds-and-calibration.md) |
| 機率校準 | [校準](../evaluation/classification-thresholds-and-calibration.md#校準-calibration) |
| 分數分布：兩類是否分得開、有沒有大量極端值 | [ROC 與 AUC](../evaluation/roc-auc.md) |

## 資料診斷：train 與 test 長得一樣嗎？

**Adversarial validation**：訓練一個分類器去分辨「這筆來自 train 還是 test」。分得出來（AUC 明顯 > 0.5）代表兩者分布不同，驗證分數可能不代表上線表現；重要性最高的特徵就是偏移的來源。

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold

X_adv = pd.concat([X_train, X_test])
y_adv = np.r_[np.zeros(len(X_train)), np.ones(len(X_test))]     # 0 = train, 1 = test
cross_val_score(RandomForestClassifier(random_state=0), X_adv, y_adv, scoring="roc_auc",
                cv=StratifiedKFold(5, shuffle=True, random_state=0)).mean()
# 乳癌資料隨機切分：0.46 ≈ 0.5 → 沒有偏移
# 依醫院 / 時間 / 批次切分時若 > 0.7 → 有明顯偏移
```

| 其他資料檢查 | 說明 |
| --- | --- |
| 缺失型態 | train 與 test 的缺失率是否相近；缺失是否和目標有關 |
| 重複或近似重複列 | 同一實體跨 train / test → 用分組切分 |
| 特徵隨時間漂移 | 上線後持續監控，見 [部署與監控](../production/deployment-and-monitoring.md) |

## 檢查順序

```
1. 資料切分與 pipeline 正確嗎？（洩漏？）
2. 整體分數比 baseline 好多少？
3. 錯誤集中在哪些切片？
4. 最後才決定：改特徵、改閾值，還是換模型
```

## 常見警訊

| 警訊 | 先懷疑 |
| --- | --- |
| 測試分數高得不合理 | [資料洩漏](../foundations/data-leakage.md) |
| 整體平均不錯，但某少數群體很差 | 樣本代表性不足，見 [抽樣與代表性](../foundations/sampling-and-representativeness.md) |
| 高值區系統性低估、低值區系統性高估 | 向平均回歸；模型太簡單或正則化太強 |
| 預測機率很極端，但實際 precision 不穩 | 校準問題 |
| 驗證分數好、上線差 | 分布偏移、上線時特徵拿不到或定義不同 |
