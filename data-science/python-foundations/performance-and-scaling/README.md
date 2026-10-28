# Performance and Scaling

資料變大或程式變慢時的 Python 工具。先量測、再向量化，最後才考慮平行化或換引擎。

| 筆記 | 重點 |
| --- | --- |
| [Efficient Python](efficient-python.md) | 量測（`timeit`、profiler）、內建函式、向量化、避免不必要的迴圈 |
| [Parallel](parallel.md) | `multiprocessing` 與 Dask（out-of-core DataFrame、延遲計算） |
| [Polars](polars.md) | Rust 實作的 DataFrame 引擎、lazy query |

pandas 本身的效能模式見 [pandas Performance](../pandas/performance.md)；Spark 等分散式工具見 [Scalable Processing](../../data-engineering/scalable-processing-and-out-of-core.md)。
