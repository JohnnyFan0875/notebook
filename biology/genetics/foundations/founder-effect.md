[遺傳學](../README.md) › [基礎概念](README.md) › 創始者效應

# 創始者效應 (Founder Effect)

一個新族群由少數個體建立（遷徙、隔離、瓶頸）時，創始者身上恰好帶有的變異會在後代中變得常見，使該族群的等位基因頻率與原族群明顯不同。它是遺傳漂變 (genetic drift) 的一種特例。

| 概念 | 說明 |
| --- | --- |
| 創始者效應 | 少數個體建立新族群 |
| 瓶頸效應 (bottleneck) | 原族群數量驟減後再擴張 |
| 遺傳漂變 | 小族群中頻率的隨機變動，兩者都是其表現 |
| 天擇 | 與漂變不同：頻率因適應優勢改變（例：鐮刀型貧血帶因者對瘧疾有抵抗力） |

## 例子

| 族群 | 常見致病變異 / 疾病 |
| --- | --- |
| 阿什肯納茲猶太人 | *BRCA1* c.68_69del、c.5266dupC；*BRCA2* c.5946del；Tay-Sachs（*HEXA*）；Gaucher |
| 芬蘭 | 「芬蘭疾病遺產」：約 40 種在芬蘭特別常見的隱性疾病 |
| 魁北克法裔 | 多種隱性疾病（如 *FAH* 酪胺酸血症） |
| 阿米許 | Ellis-van Creveld 症候群等 |

## 對判讀的影響

| 影響 | 說明 |
| --- | --- |
| 族群頻率 | 某變異在 gnomAD 的某族群頻率特別高，不一定代表良性；先確認是否為已知創始者變異（看 [gnomAD](../databases/population-frequency/gnomad.md) 的 grpmax 與 ClinVar） |
| 篩檢策略 | 高風險族群可先做創始者變異的標靶檢測（如阿什肯納茲 *BRCA* 三點檢測） |
| 本地資料庫的價值 | 東亞或台灣特有的變異在國際資料庫中代表性不足，見 [TaiwanGenomes](../databases/population-frequency/taiwangenomes.md) |
| 單倍型 | 創始者變異通常位在同一個祖先單倍型上，可用來確認來源 |

相關：[變異等位基因頻率](variant-allele-frequency.md)。
