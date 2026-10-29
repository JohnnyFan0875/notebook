[Biology](../../README.md) › [基因體學](../README.md) › 檢測確效

# 檢測確效 (Assay Validation & Verification)

臨床或研究用的 NGS 檢測，在報告結果前要證明它「量得準、量得穩、知道自己的極限」。這包括濕實驗與生資流程兩部分；改動流程（換比對器、升級版本）也要重新評估。

## Validation vs Verification

| | 確效 (Validation) | 驗證 (Verification) |
| --- | --- | --- |
| 問題 | 這個方法適合預期用途嗎？ | 這個已確效的方法在我的實驗室表現如預期嗎？ |
| 對象 | 實驗室自行開發的檢測 (LDT)、修改過的方法 | 已核准的商業套組（照原廠方式使用） |
| 範圍 | 完整：準確度、精密度、LOD、可報告範圍… | 精簡：確認原廠宣稱的關鍵效能 |

## 評估指標

| 指標 | 定義 | 怎麼做 |
| --- | --- | --- |
| 敏感度 (sensitivity / recall) | TP / (TP + FN)：真實變異被偵測到的比例 | 對照參考標準品的已知變異 |
| 陽性預測值 (PPV / precision) | TP / (TP + FP)：報出的變異是真的比例 | 同上；NGS 常用 PPV 取代特異度 |
| 特異度 (specificity) | TN / (TN + FP) | 「真陰性」是整個基因組中數以百萬計的非變異位置，數值永遠接近 100%，意義有限 |
| 偵測極限 (LOD) | 能穩定偵測（如 ≥ 95%）的最低 VAF 或最低起始量 | 稀釋系列（標準品混合不同比例） |
| 精密度 | 重複性（同批）與再現性（跨批、跨人、跨儀器） | 同樣本多次重複 |
| 可報告範圍 | 哪些區域、哪些變異類型可以報告 | 列出低覆蓋區、不支援的變異類型（大型 indel、CNV） |
| 干擾 | 樣本品質（FFPE、溶血、低腫瘤比例）的影響 | 刻意加入干擾條件測試 |

依變異類型（SNV、小 indel、CNV、融合）**分開**計算；整體數字常被大量容易的 SNV 拉高。統計上這是分類器評估的問題，見 [混淆矩陣指標](../../../data-science/machine-learning/evaluation/confusion-metrics.md)；小樣本下的不確定性見 [指標的不確定性](../../../data-science/machine-learning/evaluation/metric-uncertainty.md)。

## 筆記

| 筆記 | 內容 |
| --- | --- |
| [參考標準品](reference-standard.md) | 商業標準品、Genome in a Bottle (GIAB)、比對工具 hap.py |

## 指引

| 指引 | 適用 |
| --- | --- |
| [AMP / CAP：NGS 腫瘤 panel 確效指引](https://www.amp.org/AMP/assets/File/resources/AssayValidation_Final.pdf?pass=34)（Jennings et al., J Mol Diagn 2017） | 體細胞變異 panel：錯誤導向的設計、最少樣本數、LOD |
| ACMG 臨床 NGS 標準（Rehm et al., Genet Med 2013） | germline 檢測 |
| AMP / CAP 生資流程確效建議（Roy et al., J Mol Diagn 2018） | 生資 pipeline 的確效與版本控管 |

> NGS 的「特異度」很難定義（真陰性位置的數量取決於怎麼數），所以確效報告多用敏感度與 PPV。這個問題的討論見 [Can you determine the specificity of an NGS assay?](https://blog.limbus-medtec.com/can-you-determine-the-specificity-of-an-ngs-assay-b5c811e17dcc)（網站目前無法存取）。
