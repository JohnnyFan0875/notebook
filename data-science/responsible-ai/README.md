[Data Science](../README.md) › Responsible AI

# 負責任的 AI (Responsible AI)

模型進入真實決策（尤其醫療、基因、臨床研究）時，準確率之外還要回答：誰會受影響、錯了會造成什麼傷害、資料能不能合法使用、出事時誰負責。本章涵蓋倫理與治理、偏誤、隱私法規、匿名化與 AI 資安。資料品質與資料治理的工程實作見 [資料品質檢查](../data-engineering/data-quality-checks.md)、[資料治理](../data-engineering/governance.md)。

## 建議順序

```
原則與治理 → 資料偏誤 → 隱私與法規 → EU AI Act → 匿名化實作 → AI 資安與風險
（為什麼、誰負責）  （錯在資料）   （能不能用）   （AI 專屬規範）  （怎麼釋出）    （怎麼被攻擊、怎麼監控）
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Responsible AI](responsible-ai.md) | 原則、生命週期、倫理框架、資料倫理（同意、FAIR）、AI 用資料的責任、治理（角色、文件、Model Card） | 怎麼把「應該怎麼做」變成流程？ |
| [資料偏誤與代表性](data-bias-and-representativeness.md) | 選擇偏誤、歷史偏誤、標註偏誤、認知偏誤、GWAS / PRS 族群偏誤、EHR 偏誤、子群評估 | 模型對誰比較不準？為什麼？ |
| [隱私與法規](privacy-and-regulation.md) | 個資、GDPR、HIPAA、台灣個資法、基因資料、受控存取、資料安全 | 這份資料能不能用？要做到什麼？ |
| [EU AI Act](understanding-the-eu-ai-act.md) | 風險分級、禁止用途、高風險義務、GPAI、醫療器材（MDR / IVDR）、時程 | 我的 AI 系統屬於哪一級？ |
| [Python 匿名化](anonymization-in-python.md) | 識別碼分類、抑制 / 遮罩 / 概化、k-anonymity、差分隱私、合成資料、基因資料的限制 | 怎麼在釋出資料時降低再識別風險？ |
| [AI 資安與風險管理](ai-security-and-risk-management.md) | 資料投毒、對抗樣本、prompt injection、成員推論、drift、風險排序 | AI 系統會怎麼被攻擊或悄悄失效？ |

## 審查 AI 系統時先問

| 問題 | 為什麼 |
| --- | --- |
| 誰受這個決策影響？ | 決定需要多嚴格的控制 |
| 錯了會造成什麼傷害？偽陽性與偽陰性哪個嚴重？ | 決定指標與門檻（見 [分類門檻](../machine-learning/evaluation/classification-thresholds-and-calibration.md)） |
| 決策能被解釋、被申訴嗎？ | 受影響者的救濟途徑 |
| 誰負責上線後的監控、升級與政策更新？ | 沒有負責人 = 沒有人在管 |
