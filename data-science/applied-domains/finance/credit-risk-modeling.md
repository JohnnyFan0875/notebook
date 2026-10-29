[Data Science](../../README.md) › [應用領域](../README.md) › [Finance](README.md) › 信用風險模型

# 信用風險模型 (Credit Risk Modeling)

信用風險模型的核心不是把借款人分成好人壞人，而是估計違約機率，再把它接到放款、拒絕、定價與資本配置的決策上。模型分數本身不是終點：違約機率是否可解釋、夠穩、有校準，以及不同門檻下的經濟後果，才是重點。這套邏輯直接適用於臨床風險模型（再入院、敗血症預警）：同樣是分類 → 校準 → 成本不對稱下的門檻。

## 風險的組成

| 量 | 意義 |
| --- | --- |
| PD (probability of default) | 某筆貸款在定義期間內違約的機率 |
| EAD (exposure at default) | 違約時仍暴露的金額 |
| LGD (loss given default) | 違約後最終損失占暴露金額的比例（1 − 回收率） |
| 預期損失 (expected loss) | $EL = PD \times EAD \times LGD$ |

很多模型直接建的是 PD，但實際決策是用它去影響預期損失。

## 標籤與預測目標

| 先釐清 | 例子 |
| --- | --- |
| 違約的定義 | 逾期 90 天以上、轉催收、核銷 |
| 觀察窗 | 放款後 12 個月內是否違約 |
| 時間對齊 | 特徵只能用申請當下可得的資訊；用了之後才知道的資料（例如後續的催收紀錄）就是洩漏 |

目標定義含糊，再好的模型也只是學到一個模糊標籤。

## 模型

| 模型 | 優點 | 代價 |
| --- | --- | --- |
| Logistic regression | 直接輸出機率、可解釋、監管與溝通友善；常搭配 WOE 分箱做成評分卡 | 非線性與交互作用要手動處理 |
| 決策樹、XGBoost / LightGBM | 捕捉非線性與交互作用，表格資料表現強 | 解釋性差；機率常需要重新校準；容易只顧排序 |

通用背景見 [logistic regression](../../machine-learning/supervised-learning/classification/logistic-regression.md)、[XGBoost](../../machine-learning/supervised-learning/ensemble/xgboost.md)。

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, brier_score_loss, classification_report
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from xgboost import XGBClassifier

# 時間切分：用較早的放款訓練、較晚的放款測試（模擬實際部署）
train, test = loans[loans.issue_date < "2023-01-01"], loans[loans.issue_date >= "2023-01-01"]

lr = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
xgb = CalibratedClassifierCV(XGBClassifier(n_estimators=300, max_depth=4), method="isotonic", cv=5).fit(X_tr, y_tr)

for name, m in [("logistic", lr), ("xgb", xgb)]:
    pd_hat = m.predict_proba(X_te)[:, 1]
    print(name, roc_auc_score(y_te, pd_hat), brier_score_loss(y_te, pd_hat))
prob_true, prob_pred = calibration_curve(y_te, pd_hat, n_bins=10, strategy="quantile")
print(classification_report(y_te, pd_hat > 0.2))     # 只是第一層檢查
```

## 評估：從分類指標走到經濟後果

| 面向 | 指標 | 回答 | 不回答 |
| --- | --- | --- | --- |
| 排序 (discrimination) | ROC AUC、Gini（= 2·AUC − 1）、KS | 高風險借款人有沒有被排在前面？ | 最佳門檻、機率是否準 |
| 校準 (calibration) | 校準曲線、Brier score | 模型說 PD = 0.12 的那群，實際違約率接近 12% 嗎？ | 排序好壞 |
| 經濟後果 | 核貸率、被核准貸款的壞帳率、預期損益 | 這個模型與門檻會賺還是賠？ | — |

ranking 好不代表能直接拿來定價或核貸：定價、資本估算、風險分層都直接用到機率值，需要校準。

| 錯誤 | 成本 |
| --- | --- |
| False positive：會還款的人被判高風險 | 錯失一筆貸款的利潤（較小） |
| False negative：會違約的人被核准 | 損失本金減回收（大） |

成本極不對稱，所以 accuracy、甚至一般的分類報告都不足以回答放款風險；某些誤判即使數量少，只要落在高曝險貸款上，總損失就很大。

## 類別不平衡是資料生成機制的一部分

多數借款人本來就不會違約；而且過去的審核流程已經篩掉高風險申請，被拒絕的人沒有結果標籤（reject inference 問題），壞帳也可能很快被出售或轉移。不平衡不只是技術問題，而是樣本機制本身：模型只在「過去被核准的人」上學習，套用到全部申請者時可能有偏差。

重抽樣或類別權重會改變預測機率的尺度，之後要重新校準；決策時用調整門檻比重抽樣更直接。

## 門檻與核貸策略

| 門檻 | 結果 |
| --- | --- |
| 降低（PD 門檻放寬） | 核准更多貸款，也接受更多壞帳 |
| 提高（PD 門檻收緊） | 壞帳變少，但拒絕大量好客戶 |

```python
# 策略表：核貸率 → 對應 PD 門檻 → 被核准者的實際壞帳率
res = pd.DataFrame({"pd": pd_hat, "default": y_te.values}).sort_values("pd")
rows = []
for accept in np.arange(0.5, 1.0, 0.05):
    k = int(accept * len(res))
    accepted = res.iloc[:k]
    rows.append({"accept_rate": accept, "cutoff": accepted["pd"].max(),
                 "bad_rate": accepted["default"].mean()})
strategy = pd.DataFrame(rows)
```

策略表把模型門檻翻譯成業務後果：多放 10% 貸款，壞帳率上升多少？把壞帳率壓低，犧牲多少核貸量？最佳門檻常不是 0.5，也不是讓 sensitivity 與 specificity 最平衡的點，而是讓核貸量、風險成本與利潤率取得可接受折衷的點；還要考慮風險胃納、人工審核量、資金限制，見 [門檻與校準](../../machine-learning/evaluation/classification-thresholds-and-calibration.md)。

## 工作流程

1. 定義違約標籤與觀察期間，確認特徵在申請當下可得
2. 用時間切分建立訓練與測試集
3. 先建可解釋的基準（logistic regression）
4. 比較 tree / XGBoost 等模型的排序能力
5. 分開看排序（AUC）、校準（校準曲線、Brier）、分類報告
6. 把 PD 接到 EL = PD × EAD × LGD
7. 用策略表把門檻接到核貸率、預期損失與投組影響

| 常見錯誤 | |
| --- | --- |
| 把 PD 當硬分類，不用機率資訊 | 只追 AUC，不檢查校準 |
| 用 accuracy 當主指標 | 忽略違約稀少與錯誤成本不對稱 |
| 門檻固定用 0.5 | 沒依核貸目標或損失函數調整 |
| 隨機切分 | 高估部署後的表現（經濟環境會變） |
| 忽略不平衡反映的是審核流程 | 只在被核准者上學習的偏差 |

公平性與受保護屬性（信用模型是 EU AI Act 的高風險應用）見 [資料偏誤](../../responsible-ai/data-bias-and-representativeness.md)、[EU AI Act](../../responsible-ai/understanding-the-eu-ai-act.md)。
