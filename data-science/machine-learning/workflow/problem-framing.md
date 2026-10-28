[Machine Learning](../README.md) › [工作流程](README.md) › 問題定義

# 問題定義 (Problem Framing)

選模型之前，先把問題定義成符合資料與決策情境的形式。問題類型的總覽見 [問題類型與學習範式](../foundations/problem-types-and-learning-paradigms.md)。

## 一開始就要釐清的問題

| 問題 | 例子 | 影響 |
| --- | --- | --- |
| 目標 (target) 到底是什麼？ | 「流失」= 90 天沒登入？還是取消訂閱？ | 標籤定義、資料可得性 |
| 預測單位是什麼？ | 使用者、訂單、session、病人、樣本、細胞 | 一列代表什麼、怎麼切分 |
| 預測在什麼時間點做？ | 入院當下 vs 入院 24 小時後 | 哪些特徵合法 |
| 哪種錯誤代價高？ | 漏診（FN）vs 誤報（FP） | 指標、[閾值](../evaluation/classification-thresholds-and-calibration.md) |
| 預測時拿得到哪些資料？ | 檢驗報告兩天後才出來 | 特徵清單、[資料洩漏](../foundations/data-leakage.md) |
| 預測結果怎麼被使用？ | 排名前 5% 送人工審查 | 分類 vs 排序、評估方式 |
| 現行做法是什麼？ | 醫師經驗、既有評分系統 | [Baseline](../evaluation/baselines-and-error-analysis.md) |

## 問題定義決定後面所有選擇

| 決定 | 由什麼決定 |
| --- | --- |
| 能用哪些模型 | 輸出型態（連續、類別、排序、時間） |
| 用哪個指標 | 決策情境與錯誤代價，見 [評估思維](../foundations/evaluation-mindset.md) |
| 怎麼切資料 | 資料生成過程（時間、分組），見 [資料切分與洩漏](data-splitting-and-leakage.md) |

## 常見失敗

| 失敗 | 例子 |
| --- | --- |
| 把排序問題當一般 [分類](../supervised-learning/classification/README.md) | 只能聯絡 1,000 人，卻在最佳化整體 accuracy |
| 用預測時點不存在的資訊 | 用出院診斷預測入院時的風險 |
| 最佳化錯的指標 | 業務需要高 recall，卻在最佳化 accuracy |
| 預測單位錯 | 單細胞資料以細胞為單位切分，但要推論的是病人 |
| 其實不需要 ML | 規則或簡單統計就能解決 |

> 目標定義、決策閾值、預測時點任何一個不清楚，就先不要開始調模型。
