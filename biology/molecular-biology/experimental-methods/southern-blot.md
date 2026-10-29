[分子生物學](../README.md) › [實驗方法](README.md) › Southern blot

# Southern Blot

用限制酶切開基因體 DNA、電泳分離後轉漬到膜上，再以標記探針雜合，偵測特定 DNA 序列所在片段的大小。1975 年由 Edwin Southern 發表，是第一個 blot 方法。

## 流程

```text
基因體 DNA → 限制酶切 → 洋菜膠電泳 → 鹼變性 → 轉漬到尼龍 / 硝化纖維膜
→ 與標記探針雜合（放射性 32P 或 DIG）→ 洗去非專一結合 → 顯影
```

## 應用與替代

| 用途 | 為什麼 Southern 有用 | 現今常見替代 |
| --- | --- | --- |
| 大片段重複擴增（FMR1 CGG 全突變、C9orf72 G4C2） | PCR 擴增不了數 kb 的 GC-rich 重複；Southern 可看大小與甲基化（搭配甲基化敏感酶） | TP-PCR / AmplideX、long-read（PacBio、ONT） |
| 轉殖基因拷貝數與插入位點 | 一次看插入數與完整性 | ddPCR、全基因組定序 |
| 基因重排（如 B / T 細胞克隆性） | 重排改變酶切片段大小 | PCR + 片段分析、NGS 克隆性 |
| DNA 指紋（早期 VNTR） | 歷史用途 | STR + 毛細管電泳 |

> 需要大量 DNA（µg 級）、耗時數天，臨床上只保留在 PCR / 短讀定序看不到的情境。結構變異與重複擴增的定序方法見 [定序平台](../../genomics/sequencing-techniques/sequencing-platforms.md)。
