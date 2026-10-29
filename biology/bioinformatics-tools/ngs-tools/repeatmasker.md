[生資工具](../README.md) › [NGS 工具](README.md) › RepeatMasker

# RepeatMasker

在 DNA 序列中找出散布型重複 (interspersed repeats：SINE / Alu、LINE、LTR、DNA transposon) 與低複雜度序列，並把它們遮蔽 (mask)。人類基因體約一半會被遮蔽。常用於：引子設計前避開重複區、基因註解前遮蔽、判斷變異或 peak 是否落在重複區。

## 用法

```bash
# Docker（pegi3s/repeat_masker）或 conda install -c bioconda repeatmasker
RepeatMasker -species human -xsmall -pa 8 -dir rm_out sequence.fa
```

| 參數 | 意義 |
| --- | --- |
| `-species` | 選物種的重複序列庫（human、mouse、arabidopsis…） |
| `-xsmall` | **軟遮蔽**：重複區改成小寫，其他保持大寫（比對器、引子工具可辨識） |
| 預設 / `-x` | **硬遮蔽**：重複區換成 `N` / `X`，序列長度不變 |
| `-pa N` | 平行處理數（參數名稱依版本而異，以 `RepeatMasker -help` 為準） |
| `-dir` | 輸出資料夾 |
| `-div N` | 只遮蔽與共通序列差異 < N% 的（較年輕的）重複 |

> 只是要查人類 / 小鼠參考基因體的重複區時，**不必自己跑**：直接下載 UCSC Table Browser 的 `rmsk` 軌道（就是 RepeatMasker 的結果），或用 UCSC / Ensembl 提供的軟遮蔽 FASTA（小寫 = 重複）。

## 輸出檔

| 檔案 | 內容 |
| --- | --- |
| `<file>.out` | 每個重複的註解（下表） |
| `<file>.masked` | 遮蔽後的序列，長度與輸入相同 |
| `<file>.tbl` | 摘要：序列長度、GC、被遮蔽的鹼基數、各類重複的比例 |

## `.out` 欄位

```text
463  1.3  0.6  1.7  chr1  10001  10468  (248945954)  +  (TAACCC)n  Simple_repeat  1  463  (0)  1
```

| # | 欄位 | 意義 |
| --- | --- | --- |
| 1 | SW score | Smith-Waterman 比對分數 |
| 2 | % div. | 與共通序列 (consensus) 的差異率；越低代表插入越晚 |
| 3–4 | % del. / % ins. | 缺失 / 插入比例 |
| 5 | query sequence | 染色體 / contig |
| 6–7 | q.start / q.end | 重複在基因體的起點 / 終點（1-based） |
| 8 | (q.left) | 到序列尾端剩餘的長度 |
| 9 | strand | `+` 或 `C`（互補股） |
| 10 | repeat name | 重複名稱（如 `AluY`、`L1HS`、`(TAACCC)n`） |
| 11 | class/family | 分類（`SINE/Alu`、`LINE/L1`、`Simple_repeat`…） |
| 12–14 | r.start / r.end / (r.left) | 對應到共通序列的位置；`C` 股時欄位順序不同 |
| 15 | ID | 同一個重複被切成多段時共用的 ID |

上例是 chr1 端粒附近的 `(TAACCC)n` 簡單重複（端粒序列 TTAGGG 的互補）。

## 對分析的影響

| 情境 | 影響 |
| --- | --- |
| 短讀比對 | 重複區 MAPQ 低、多重比對，變異呼叫偽陽性多（見 [Mapping Quality](../../genomics/ngs-qc/mapping-quality.md)） |
| 引子設計 | 引子落在 Alu 等重複會非專一擴增；設計前用軟遮蔽序列（見 [引子設計](../primer-design/README.md)） |
| ChIP-seq / ATAC-seq | 重複區常出現假 peak；搭配 ENCODE blacklist 過濾 |
| 結構變異、長讀定序 | 重複區是短讀的盲區，長讀較有優勢 |

序列庫來源為 Dfam 與 Repbase。官方：[RepeatMasker](https://www.repeatmasker.org/)、[網頁版說明](https://www.repeatmasker.org/webrepeatmaskerhelp.html)。
