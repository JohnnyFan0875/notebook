[基因體學](../README.md) › [NGS 品質指標](README.md) › 重複率

# 重複率 (Duplication Rate)

重複 reads 是來自**同一個原始 DNA 片段**的多份拷貝。它們不提供獨立證據：一個 PCR 早期的錯誤被複製 10 次，看起來就像 10 條 reads 支持的變異。重複率反映 library complexity（library 裡有多少不同的分子）。

## 重複的種類

| 類型 | 成因 | 辨識方式 |
| --- | --- | --- |
| PCR 重複 | library 擴增時同一片段被複製多份 | 比對起點、終點、方向都相同 |
| 光學重複 (optical) | 同一個 cluster 被影像辨識成兩個（相鄰位置） | 同上，且在 flow cell 上位置很近 |
| 圖案化 flow cell 重複 (ExAmp / pad hopping) | NovaSeq 等的分子跳到鄰近的 well | 同上，距離較遠；Picard 設 `--OPTICAL_DUPLICATE_PIXEL_DISTANCE 2500` |
| 「自然」重複 | 高表現基因、短基因、amplicon：不同分子剛好起點相同 | **不是**技術誤差，無法和 PCR 重複區分（除非用 UMI） |

## 合理範圍（粗略參考）

| 實驗類型 | 常見重複率 | 說明 |
| --- | --- | --- |
| WGS（PCR-free） | < 5–10% | 偏高代表 library 起始量不足或 PCR 過多 |
| WES / capture panel | 10–20%；深度越高越高 | 越深定序越接近 library 的分子上限 |
| RNA-seq | 20–60% 甚至更高 | 高表現基因造成，屬正常；通常不去重複 |
| Amplicon panel | 接近 100% | 設計上所有 reads 起點相同；**不能**去重複 |
| cfDNA / 低起始量 | 高 | 用 UMI 區分真重複與獨立分子 |

> 重複率隨定序深度上升：同一個 library 定序越深，越多新 reads 只是在重讀已讀過的分子 (saturation)。Picard 的 `ESTIMATED_LIBRARY_SIZE` 可用來判斷再加深定序還值不值得。

## 對分析的影響

| 影響 | 說明 |
| --- | --- |
| 有效深度降低 | 1000× 的原始深度、50% 重複 → 只有約 500× 的獨立證據 |
| 變異呼叫偽陽性 | PCR 錯誤被重複放大；germline / somatic 流程都需標記重複 |
| 低頻變異的 VAF 偏差 | 某個分子被擴增較多次，VAF 被扭曲；用 UMI consensus 修正 |

## 怎麼量

```bash
picard MarkDuplicates -I in.bam -O dedup.bam -M metrics.txt   # PERCENT_DUPLICATION、ESTIMATED_LIBRARY_SIZE
samtools flagstat dedup.bam                                   # duplicates 一行
```

fastp 報告的重複率是未比對前依序列估計的粗略值；以比對後的 Picard / samtools 數值為準。工具與 UMI 處理見 [Picard MarkDuplicates](../../bioinformatics-tools/ngs-tools/picard-markduplicates.md)；FastQC 的 duplication 模組判讀見 [FastQC](../../bioinformatics-tools/ngs-tools/fastqc.md)。
