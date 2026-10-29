[生資工具](../README.md) › [引子設計](README.md) › Primer3

# Primer3

最常用的引子設計引擎：給定模板序列與條件（產物長度、Tm、GC…），回傳排序好的候選引子對。NCBI Primer-BLAST、許多商業工具的底層都是 Primer3。

| 項目 | 內容 |
| --- | --- |
| 網頁版 | [Primer3Plus](https://www.primer3plus.com/)、[primer3.ut.ee](https://primer3.ut.ee/) |
| 程式 | 命令列 `primer3_core`；Python `primer3-py`（`pip install primer3-py`） |
| 輸入 | 模板序列；目標區 (`SEQUENCE_TARGET`)、排除區 (`SEQUENCE_EXCLUDED_REGION`，如 SNP、重複區） |
| 輸出 | 引子序列、位置、Tm、GC%、產物長度、penalty 分數 |
| 不負責 | 基因體專一性（用 Primer-BLAST 或 [In-Silico PCR](ucsc-in-silico-pcr.md) 檢查） |

## 常用條件

| 參數 | 設定範例 | 對應準則 |
| --- | --- | --- |
| `PRIMER_PRODUCT_SIZE_RANGE` | `120-180` | 產物長度 |
| `PRIMER_OPT_SIZE` / `MIN` / `MAX` | 20 / 18 / 25 | 引子長度 |
| `PRIMER_OPT_TM` / `MIN_TM` / `MAX_TM` | 60 / 57 / 63 | Tm |
| `PRIMER_PAIR_MAX_DIFF_TM` | 2 | 正反 Tm 差 |
| `PRIMER_MIN_GC` / `MAX_GC` | 40 / 60 | GC 含量 |
| `PRIMER_MAX_POLY_X` | 4 | homopolymer 上限 |
| `PRIMER_GC_CLAMP` | 1 | 3′ 端 G/C |
| `SEQUENCE_EXCLUDED_REGION` | `start,length` | 避開 SNP、重複區 |

```python
import primer3

res = primer3.design_primers(
    seq_args={"SEQUENCE_ID": "KRAS_ex2", "SEQUENCE_TEMPLATE": template,
              "SEQUENCE_TARGET": [200, 50]},           # 目標區：起點 200、長度 50
    global_args={"PRIMER_PRODUCT_SIZE_RANGE": [[120, 180]],
                 "PRIMER_OPT_TM": 60.0, "PRIMER_MIN_TM": 57.0, "PRIMER_MAX_TM": 63.0,
                 "PRIMER_MIN_GC": 40.0, "PRIMER_MAX_GC": 60.0},
)
res["PRIMER_LEFT_0_SEQUENCE"], res["PRIMER_RIGHT_0_SEQUENCE"], res["PRIMER_PAIR_0_PRODUCT_SIZE"]
primer3.calc_hairpin("GGCGAAGGCGTTCGCC").dg     # ≈ −4678 cal/mol = −4.7 kcal/mol：強 hairpin，不可用
```

以 `primer3-py` 2.4 驗證；舊版（< 1.0）的函式名稱是 `primer3.bindings.designPrimers`。

完整準則見 [引子設計](README.md)。
