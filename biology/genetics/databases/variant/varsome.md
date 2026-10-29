[資料庫](../README.md) › [變異](README.md) › VarSome

# VarSome

Saphetor 公司的變異搜尋引擎：輸入一個變異（HGVS、rsID、座標），一頁彙整數十個資料庫（ClinVar、gnomAD、dbNSFP 預測分數、文獻、基因資訊），並**自動套用 ACMG 準則**給出建議分類與觸發的準則。

| 項目 | 內容 |
| --- | --- |
| 網站 | [varsome.com](https://varsome.com/) |
| 方案 | 免費帳號可查詢單一變異（有使用量限制）；VarSome Clinical / API 為付費服務 |
| 適合 | 快速瀏覽單一變異的全貌、檢查有沒有漏掉的證據 |
| 限制 | 自動 ACMG 是依可取得的資料機械式套用：缺少家族、表型、功能試驗證據，也可能誤用準則強度；**只能當起點** |

> 每條自動觸發的準則都要人工核對（例如 PM2 是否該降為 Supporting、PP3 用的是哪個工具與閾值），見 [ACMG/AMP](../../variant-interpretation/acmg-amp.md)。類似的整合工具：Franklin（Genoox）。
