[Biology](../../README.md) › [分子生物學](../README.md) › 實驗方法

# 實驗方法 (Experimental Methods)

偵測與定量核酸、蛋白質的常用濕實驗方法。重點是知道每個方法量到的是什麼分子、輸出是定性還是定量、以及在生資工作中扮演的角色（通常是驗證 NGS 或質譜的結果）。

建議順序：凝膠電泳 → 三種 blot → qPCR / ELISA（定量）→ 應用（病毒檢測、寡核苷酸、BAC）

## 依目標分子選方法

| 想偵測 | 定性 / 大小確認 | 定量 | 高通量 / 全面 |
| --- | --- | --- | --- |
| DNA | [Southern blot](southern-blot.md)、PCR + [電泳](gel-electrophoresis.md) | [qPCR](qpcr.md)、ddPCR | DNA-seq、微陣列 |
| RNA | [Northern blot](northern-blot.md)、RT-PCR | [RT-qPCR](qpcr.md) | [RNA-seq](../../genomics/workflows/rna-seq/README.md) |
| 蛋白質 | [Western blot](western-blot.md) | [ELISA](elisa.md)、Western（半定量） | 質譜、Olink / SomaScan |

## Blot 類型比較

| | Southern | Northern | Western |
| --- | --- | --- | --- |
| 目標 | DNA | RNA | 蛋白質 |
| 分離 | 限制酶切 → 洋菜膠 (agarose) | 變性洋菜膠（formaldehyde） | SDS-PAGE |
| 探針 | 標記的 DNA / RNA 探針（雜合） | 標記的 DNA / RNA 探針（雜合） | 一級 + 二級抗體 |
| 回答 | 片段大小、拷貝數、重排 | 轉錄本大小、剪接型、表現量 | 蛋白大小、表現量、修飾 |
| 目前替代 | PCR、NGS、long-read、optical mapping | RT-qPCR、RNA-seq | 質譜、ELISA、capillary Western |

命名：Southern 來自發明者 Edwin Southern，Northern / Western 是後來依方位類推的命名（另有偵測蛋白–DNA 結合的 Southwestern blot）。

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [凝膠電泳](gel-electrophoresis.md) | agarose vs PAGE、SDS-PAGE、片段大小判讀 | 片段多大？樣本完整嗎？ |
| [Southern blot](southern-blot.md) | 流程、應用（重複擴增、拷貝數、轉殖基因） | 何時仍需要 Southern？ |
| [Northern blot](northern-blot.md) | 流程、RNA 完整性、與 RT-qPCR / RNA-seq 比較 | 轉錄本大小與剪接型怎麼確認？ |
| [Western blot](western-blot.md) | 流程、loading control、抗體驗證、定量限制 | 蛋白是否表現？大小與修飾對嗎？ |
| [qPCR](qpcr.md) | PCR / RT-PCR / qPCR、SYBR vs TaqMan、Ct、效率、ΔΔCt、MIQE | 怎麼用 qPCR 定量並驗證 RNA-seq？ |
| [ELISA](elisa.md) | 四種格式、標準曲線 (4PL)、品質指標 | 怎麼定量血清 / 上清液中的蛋白？ |
| [寡核苷酸合成與純化](oligonucleotide-synthesis-and-purification.md) | 固相合成、累積產率、四種純化等級 | 引子 / 探針要選哪種純化？ |
| [病毒檢測方法](virus-detection-method.md) | 核酸、抗原、抗體、培養、定序的比較 | 感染期不同時要用哪種檢測？ |
| [細菌人工染色體 (BAC)](bacterial-artificial-chromosome.md) | 載體比較、在基因體計畫與細胞遺傳學的應用 | BAC 為何對人類基因體計畫重要？ |

相關：[引子設計](../../bioinformatics-tools/primer-design/README.md)、[檢測確效](../../genomics/assay-validation/README.md)、[免疫標記的量測方法](../../immunology/immune-marker.md#量測方法)。
