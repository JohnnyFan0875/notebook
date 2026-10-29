[Data Science](../../README.md) › [Data Communication](../README.md) › BI 工具

# BI 工具 (BI Tools)

Power BI 與 Tableau 的精簡筆記。對分析與研究工作屬於選讀：需要交付互動式報表給非程式使用者、需要權限控管與排程更新時再看。通用的 dashboard 原則見 [Dashboard 設計](../dashboard-design.md)。

## 建議順序

```
Power Query（擷取與清理）→ 模型與 DAX（關係、計算）→ 報表（導覽、設計）
```

Tableau 可獨立閱讀；概念（dimension / measure、join、計算層級）與 Power BI 相通。

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Power Query](power-query.md) | 資料來源、Import / DirectQuery / Live、gateway 與增量重新整理、Applied Steps 清理、pivot / unpivot、append / merge、M 語言 | 資料怎麼接進來、清理成可重跑的步驟？ |
| [Power BI 模型與 DAX](power-bi-modeling-and-dax.md) | Desktop / Service、semantic model、關係與篩選方向、RLS / OLS、DAX context、measure、`CALCULATE()`、time intelligence | 數字怎麼算才會隨篩選正確變化？ |
| [Power BI 報表](power-bi-reports.md) | report vs dashboard、bookmark、drillthrough、tooltip、Q&A、漸進揭露、主題、無障礙、行動版 | 報表怎麼組織、怎麼設計才好用？ |
| [Tableau](tableau.md) | 工作流程、dimension / measure、join / union / relationship、計算欄位與 LOD | Tableau 的資料與計算模型怎麼想？ |

## Power BI vs Tableau

| 面向 | Power BI | Tableau |
| --- | --- | --- |
| 生態 | Microsoft（Excel、Azure、Fabric、Teams） | Salesforce |
| 強項 | 資料模型與 DAX、與 Office 整合、授權成本 | 視覺探索、拖放互動、圖表彈性 |
| 資料準備 | Power Query（M） | Tableau Prep、資料來源頁 |
| 計算語言 | DAX | 計算欄位、LOD 運算式、table calculation |
| 作者端 | Power BI Desktop（Windows） | Tableau Desktop（Windows / macOS） |

資料模型（fact / dimension、grain）的設計原則見 [維度模型](../../data-engineering/dimensional-modeling-and-star-schema.md)；Excel 中的同類功能見 [Power Pivot](../../../productivity/microsoft-office/power-pivot-in-excel.md)。
