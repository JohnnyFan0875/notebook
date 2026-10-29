[資料庫](../README.md) › [藥物基因體](README.md) › CPIC

# CPIC (Clinical Pharmacogenetics Implementation Consortium)

為「已經知道病人基因型」的情境撰寫臨床指引：怎麼把基因型轉成表型、再轉成具體的處方建議。CPIC 不建議「要不要檢測」，只回答「有結果後怎麼用」。目前併入 [ClinPGx](pharmgkb.md) 平台（[cpicpgx.org](https://cpicpgx.org/) 轉址至 ClinPGx 的 CPIC 頁面），指引仍以 CPIC 名義發布。

## 指引的結構

| 部分 | 內容 |
| --- | --- |
| 等位基因功能 | 每個 star allele 的功能（正常 / 降低 / 無功能 / 增加） |
| 雙倍型 → 表型 | 例：*CYP2C19* `*1/*2` → 中間代謝者；`*2/*2` → 不良代謝者 |
| 處方建議 | 依表型：標準劑量、調整劑量、或換用替代藥物，並附建議強度（強 / 中 / 選擇性） |
| 對照表 | 可直接嵌入電子病歷的臨床決策支援 |

## 基因–藥物配對的等級

| 等級 | 意義 |
| --- | --- |
| A | 有充分證據，應依基因型調整處方 |
| B | 證據支持調整處方，或有合理替代藥物 |
| C / D | 證據不足或不建議依基因型調整；CPIC 不撰寫完整處方建議 |

| 代表性 A 級配對 | 建議重點 |
| --- | --- |
| *CYP2C19* — clopidogrel | 中間 / 不良代謝者（ACS / PCI）改用 prasugrel 或 ticagrelor |
| *CYP2D6* — codeine、tramadol | 不良與超快速代謝者避免使用 |
| *DPYD* — 5-FU、capecitabine | 依活性分數減量 |
| *TPMT* / *NUDT15* — thiopurines | 依兩基因的表型減量 |
| *HLA-B\*57:01* — abacavir | 帶因者禁用 |
| *HLA-B\*15:02* — carbamazepine | 帶因者避免使用 |
| *SLCO1B1* — statins | 依功能調整藥物與劑量 |

> 東亞族群特別相關的等位基因：*CYP2C19\*2 / \*3*（不良代謝者比例高）、*HLA-B\*15:02*、*HLA-B\*58:01*、*NUDT15* 變異。基因型的 star allele 定義以 PharmVar 為準。
