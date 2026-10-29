[分子生物學](../README.md) › [實驗方法](README.md) › Northern blot

# Northern Blot

把 RNA 在變性膠上依大小分離、轉漬到膜上，再用探針雜合偵測特定轉錄本。能同時回答「有沒有表現」與「轉錄本多大」，因此可直接看到剪接型或截短產物。

## 流程

```text
總 RNA / mRNA → 變性洋菜膠（formaldehyde / glyoxal）→ 轉漬到尼龍膜
→ UV 交聯 → 與標記探針雜合 → 洗膜 → 顯影；以 GAPDH 等或 rRNA 作上樣對照
```

## 與其他 RNA 方法比較

| | Northern | RT-qPCR | RNA-seq |
| --- | --- | --- | --- |
| 輸出 | 轉錄本大小 + 相對量 | 單一擴增區的相對 / 絕對量 | 全轉錄體表現量、剪接、融合 |
| 靈敏度 | 低（需 µg 級 RNA） | 高 | 高（依深度） |
| 通量 | 低 | 中（數十基因） | 全基因 |
| 優勢 | 直接看完整長度、無擴增偏差 | 快、便宜、定量範圍廣 | 不需預知目標 |

## 注意事項

| 問題 | 說明 |
| --- | --- |
| RNase 汙染 | RNA 易降解：用 RNase-free 試劑與耗材、DEPC 水；先確認 RIN |
| 探針交叉雜合 | 基因家族序列相近時可能偵測到旁系同源基因 |
| 小 RNA | miRNA 需用 PAGE 版本的 Northern |

現在多用於驗證 RNA-seq 中的新轉錄本、截短轉錄本或 small RNA；一般表現量驗證改用 [RT-qPCR](qpcr.md)。
