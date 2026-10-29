[生資工具](../README.md) › [引子設計](README.md) › OligoEvaluator

# OligoEvaluator

Sigma-Aldrich（Merck）提供的線上 oligo 計算工具，檢查單條或一對引子的物理性質與二級結構。

| 項目 | 內容 |
| --- | --- |
| 網站 | [oligoevaluator.com](https://www.oligoevaluator.com/LoginServlet)（需登入） |
| 計算 | Tm、GC%、分子量、消光係數、hairpin、self-dimer / primer-dimer |
| 何時用 | 引子設計後、下單合成前，逐條檢查二級結構 |
| 替代 | [IDT OligoAnalyzer](https://www.idtdna.com/pages/tools/oligoanalyzer)（免登入可用基本功能）、`primer3-py` 的 `calc_hairpin` / `calc_heterodimer`（見 [Primer3](primer3.md)） |

> 不同工具的 Tm 會因鹽濃度、引子濃度與計算模型（nearest-neighbor 參數）而差好幾度；比較時固定同一工具與同一組條件，並依實際反應的 Na⁺ / Mg²⁺ 濃度設定。
