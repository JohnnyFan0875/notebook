[生資工具](../README.md) › [引子設計](README.md) › PrimerPooler

# PrimerPooler

把多重 PCR (multiplex PCR) 的大量引子對分配到數個 pool，**讓每個 pool 內的 primer-dimer 最少**，並可讓基因體上重疊的 amplicon 分到不同 pool。它不設計引子，引子要先用 [Primer3](primer3.md) / Primer-BLAST 設計好。

| 項目 | 內容 |
| --- | --- |
| 來源 | [GitHub: ssb22/PrimerPooler](https://github.com/ssb22/PrimerPooler)（開源，Apache 2.0） |
| 執行 | 命令列（互動提示或參數）；從原始碼 `make` 編譯，支援 Linux / macOS / BSD，Windows 有 MinGW 版 |
| 輸入 | 多序列 FASTA：引子名稱結尾 `F` / `R`、其餘相同（如 `>KRAS_ex2F`、`>KRAS_ex2R`）；可含簡併鹼基 |
| 選擇性輸入 | 基因體檔（`.2bit` / `.fa`）與最大 amplicon 長度（預設 220 bp），用來找重疊 amplicon |
| 輸出 | 每個 pool 的引子清單、各 pool 的交互作用計數、dimer 配對圖 |
| 規模 | 可處理上千條引子，多核心平行 |

## 主要設定

| 設定 | 說明 |
| --- | --- |
| pool 數 / 每個 pool 上限 | 可讓程式建議最少 pool 數 |
| 交互作用計算 | `score`（快、較粗）或 ΔG（指定溫度、鹽、Mg²⁺、dNTP 濃度，較準） |
| 固定分組 | 名稱前綴 `>@2:` 強制放到第 2 個 pool |
| 共通 tag | 可加上所有正 / 反引子共用的 adapter 或 barcode 一起計算 |

> 沒做基因體掃描時不會考慮 amplicon 重疊；重疊的 amplicon 放同一個 pool 會產生短的非預期產物。替代工具：McGill 的 PrimerWeaver（網頁、同時設計與分組）、商業 panel 設計平台。

相關：[擴增子 panel](../../genomics/sequencing-techniques/targeted-panels.md)。
