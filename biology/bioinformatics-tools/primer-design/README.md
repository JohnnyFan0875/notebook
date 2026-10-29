[Biology](../../README.md) › [生資工具](../README.md) › 引子設計

# 引子設計 (Primer Design)

PCR / qPCR / amplicon 定序的成敗多半取決於引子：要能專一結合目標、兩條引子條件相近、不形成二級結構或彼此配對。這裡整理設計準則與工具。

## 設計準則

| 項目 | 準則 | 原因 |
| --- | --- | --- |
| 引子長度 | 18–25 bp | 太短專一性不足，太長 Tm 過高、成本高 |
| 產物長度 (amplicon) | qPCR 70–150 bp；一般常見 120–180 bp（140–160 bp 最常用），上限 < 250 bp | 短產物擴增效率高；cfDNA、FFPE 等片段化樣本需要更短 |
| GC 含量 | 40–60% | 太低 Tm 低、太高易非專一結合 |
| 融解溫度 (Tm) | 55–65 °C；正反引子 Tm 差 ≤ 2 °C | 兩條引子才能在同一個 annealing 溫度有效結合 |
| 3′ 端 | 最後 5 個鹼基中 G/C 不超過 2–3 個（GC clamp）；最後約 7 個鹼基最關鍵 | 聚合酶從 3′ 端延伸，3′ 錯配或自我配對影響最大 |
| 二級結構 | 無強 hairpin（ΔG 不低於約 −2 kcal/mol）；避免 self-dimer / cross-dimer，尤其 3′ 端互補 | dimer 會產生 primer-dimer 產物、搶走試劑 |
| 避開 SNP | 引子結合區不可有常見 SNP；必要時與 rs 位點保持距離（如 ≥ 50 bp，依檢測設計） | 引子下的 SNP 會導致等位基因擴增失敗 (allele dropout) |
| 專一性 | 在人類基因體只有一個顯著結合位置（BLAST / In-Silico PCR）；同基因家族的額外命中需逐一確認 | 假基因 (pseudogene) 與同源基因是偽陽性主因 |
| 重複區 | 避開 homopolymer（如 ≥ 4 個相同鹼基）、tandem repeat 與 Alu 等散布型重複 | 滑動、非專一結合；先用 [RepeatMasker](../ngs-tools/repeatmasker.md) 軟遮蔽的序列設計 |
| qPCR 額外 | 跨越 exon-exon 接合處（避免 gDNA 擴增）；probe Tm 比引子高約 5–10 °C | 只偵測 cDNA |

## 設計流程

```
目標序列（軟遮蔽 FASTA，標出 SNP）
   │  Primer3 / Primer-BLAST 產生候選引子
   ▼
專一性：Primer-BLAST 或 UCSC In-Silico PCR（只有一個產物？）
   │
   ▼
二級結構與 dimer：OligoAnalyzer / OligoEvaluator
   │
   ▼
多重 PCR：PrimerPooler 分組，降低組內 dimer
   │
   ▼
實驗驗證：溫度梯度、熔解曲線 / 電泳只有單一條帶、效率 90–110%（qPCR）
```

## 工具

| 工具 | 用途 | 何時用 |
| --- | --- | --- |
| [Primer3](primer3.md) | 依條件設計引子對 | 標準設計引擎；也有 Python 套件 `primer3-py` |
| [NCBI Primer-BLAST](https://www.ncbi.nlm.nih.gov/tools/primer-blast/) | Primer3 + BLAST 專一性檢查一次完成 | 單一目標的設計首選 |
| [UCSC In-Silico PCR](ucsc-in-silico-pcr.md) | 在參考基因體上模擬 PCR | 確認產物只有一個、位置正確 |
| [OligoEvaluator](oligoevaluator.md) | Tm、GC、二級結構、dimer 計算 | 單條 oligo 檢查 |
| [PrimerPooler](primerpooler.md) | 多重 PCR 引子分組 | 數十到上千對引子的 panel |

相關：[qPCR](../../molecular-biology/experimental-methods/qpcr.md)、[寡核苷酸合成與純化](../../molecular-biology/experimental-methods/oligonucleotide-synthesis-and-purification.md)、[擴增子 panel](../../genomics/sequencing-techniques/targeted-panels.md)。
