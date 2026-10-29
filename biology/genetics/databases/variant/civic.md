[資料庫](../README.md) › [變異](README.md) › CIViC

# CIViC (Clinical Interpretation of Variants in Cancer)

華盛頓大學 Griffith Lab 主導的開放資料庫，由社群提交、專家審閱癌症變異的臨床證據（療效預測、診斷、預後、遺傳易感性），資料以 CC0 釋出，可自由使用。

| 項目 | 內容 |
| --- | --- |
| 網站 | [civicdb.org](https://civicdb.org/welcome) |
| 單位 | Evidence item（一篇文獻中的一個臨床主張）→ 彙整成 Assertion（附 AMP / ASCO / CAP Tier 與 ACMG 分類） |
| 授權 | CC0（公眾領域） |
| 存取 | 網頁、GraphQL API、每月資料匯出 |

## 證據類型與等級

| 證據類型 | 問題 |
| --- | --- |
| Predictive | 變異是否預測對某藥物的反應 / 抗藥？ |
| Diagnostic | 變異是否幫助診斷某癌別？ |
| Prognostic | 變異與預後的關係？ |
| Predisposing / Oncogenic / Functional | 遺傳易感性、致癌性、功能影響 |

| 等級 | 意義 |
| --- | --- |
| A | 已驗證：臨床實務或 FDA 核准 |
| B | 臨床研究證據 |
| C | 個案報告 |
| D | 臨床前（細胞、動物） |
| E | 推論（間接證據） |

> 臨床決策以 A / B 等級與 Assertion 為主。與 OncoKB（專有、以療效分級為主）、[PMKB](pmkb.md) 互相對照。CIViC 原本放在藥物基因體資料夾，但它處理的是**腫瘤體細胞變異**，與 germline 藥物基因體（[ClinPGx](../pharmacogenomics/pharmgkb.md)）不同。
