[基因體學](../README.md) › [NGS 品質指標](README.md) › 均勻度

# 均勻度 (Coverage Uniformity)

均勻度描述深度在目標區域中分布得多平均。均勻度差時，即使平均深度很高，仍有一部分區域深度不足而漏掉變異；反過來說，均勻度好的 library 用較少的 reads 就能達到同樣的覆蓋度。

## 指標

| 指標 | 定義 | 好的範圍 | 來源 |
| --- | --- | --- | --- |
| Fold-80 base penalty | 平均深度 ÷ 第 20 百分位數的深度：**要讓 80% 鹼基達到目前平均深度，需要多定序幾倍** | 越接近 1 越好；capture < 2 | Picard `CollectHsMetrics` |
| % bases ≥ 0.2 × mean | 深度至少達平均 20% 的鹼基比例 | > 95% | Illumina / 多數 panel 報告 |
| % bases ≥ N× | 達到固定深度的比例 | 依應用（例：≥ 20× > 95%） | mosdepth、Picard |
| CV of coverage | 深度的變異係數 | 越小越好 | 自行計算 |

![平均深度相同、均勻度不同](src/sequencing-depth-coverage-uniformity.png)

圖中兩個 library 平均都是 100×：左邊第 20 百分位數 79× → fold-80 = 100 / 79 ≈ 1.3；右邊第 20 百分位數 33× → fold-80 ≈ 3.0，代表要再多定序約 3 倍，80% 的鹼基才能達到 100×。

## 影響均勻度的因素

| 因素 | 說明 |
| --- | --- |
| [GC 偏差](gc-bias.md) | PCR 對極端 GC 區擴增效率低 |
| 捕捉方式 | Hybrid capture 比 amplicon 均勻；amplicon 各 amplicon 之間的效率差異大 |
| probe / primer 設計 | 個別 probe 效率不佳造成固定的低覆蓋區 |
| PCR 循環數 | 越多越不均勻 |
| 樣本品質 | FFPE、低起始量的 DNA 片段化，均勻度差 |
| 重複序列與比對 | MAPQ 過濾後，重複區有效深度下降 |

## 判讀

- 均勻度要**跨批次追蹤**：同一 panel 的 fold-80 突然上升，通常是 library 製備或樣本品質問題。
- 固定出現在同一批目標的低覆蓋（每個樣本都低）是設計問題；只在個別樣本出現是樣本 / 製備問題。
- 臨床報告常列出「未達最低深度的區域」，讓判讀者知道哪些位置的陰性結果不可靠。

深度的定義與計算見 [定序深度與覆蓋度](sequencing-depth-coverage.md)。
