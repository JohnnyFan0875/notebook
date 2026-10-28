[Python Foundations](../README.md) › 效能與擴展

# 效能與擴展 (Performance & Scaling)

程式變慢或資料變大時的工具。順序：先量測 → 換資料結構、向量化 → 才平行化或換引擎。

```
單核最佳化（Efficient Python）→ 多核（Parallel）/ 更快的引擎（Polars）→ 多機（Spark、Dask distributed）
```

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Efficient Python](efficient-python.md) | 量測與 profiler、資料結構、向量化、Numba、記憶體 | 瓶頸在哪？不加機器能快多少？ |
| [平行運算](parallel.md) | GIL、`concurrent.futures`、joblib、平行亂數、Dask | 怎麼用滿多核心？比記憶體大的陣列怎麼算？ |
| [Polars](polars.md) | 表達式、lazy 查詢最佳化、streaming | pandas 太慢或太吃記憶體時換什麼？ |

pandas 本身的效能模式見 [pandas 效能](../pandas/performance.md)；Spark 等分散式工具見 [Scalable Processing](../../data-engineering/scalable-processing-and-out-of-core.md)。
