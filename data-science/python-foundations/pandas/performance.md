# Pandas: Performance Patterns

Most pandas performance problems come from using row-by-row Python logic on data that could be handled in bulk.

The usual optimization order is:

1. Measure first.
2. Prefer vectorized pandas or NumPy operations.
3. Use `groupby().transform()` / `groupby().filter()` instead of manual loops over groups.
4. Drop to row-wise `.apply()` only when vectorization is awkward.
5. Use `.iterrows()` only as a last resort.

## Measure Before You Optimize

Small code differences can matter on large DataFrames, so benchmark before rewriting.

```python
import time

start = time.time()
result = df["x"] + df["y"]
elapsed = time.time() - start
print(f"Calculated in {elapsed:.6f} sec")
```

- `time.time()` is fine for quick comparisons.
- Compare approaches on the same dataset and same subset of columns.
- Prefer simple measurements before guessing where the bottleneck is.

## Prefer Vectorization Over Row Loops

Vectorized operations push work into pandas / NumPy internals and avoid Python-level loops.

```python
# Slow pattern
totals = []
for _, row in df.iterrows():
    totals.append(row["a"] + row["b"] + row["c"])

# Better
df["total"] = df["a"] + df["b"] + df["c"]
```

Another common example:

```python
import numpy as np

df["ratio"] = df["sales"] / df["users"]
df["flag"] = np.where(df["ratio"] > 2, "high", "normal")
```

- Arithmetic, comparisons, boolean masks, and string methods are usually already vectorized.
- If you can describe the logic as "operate on the whole column", pandas is probably the right layer.

## `.apply()` Is Better Than `.iterrows()`, But Still Not Free

If vectorization is hard, `.apply()` is often the next step.

```python
df["score"] = df[["x1", "x2", "x3"]].apply(lambda row: row.sum(), axis=1)
```

Compared with:

```python
scores = []
for _, row in df.iterrows():
    scores.append(row["x1"] + row["x2"] + row["x3"])
df["score"] = scores
```

Mental model:

- vectorization is usually fastest
- `.apply(axis=1)` is often easier than loops, but still creates Python overhead
- `.iterrows()` is usually the slow path and can silently coerce dtypes

If you truly must iterate, `itertuples()` is often better than `iterrows()`.

```python
for row in df.itertuples(index=False):
    ...
```

## Use the Right Tool for Replacement

For exact scalar remapping, `.replace()` is usually cleaner than conditional assignment.

```python
df["gender"] = df["gender"].replace({
    "MALE": "BOY",
    "FEMALE": "GIRL",
})
```

Instead of repeatedly doing:

```python
df.loc[df["gender"] == "MALE", "gender"] = "BOY"
```

Rules of thumb:

- use `.replace()` for exact value remapping
- use `.map()` when one Series is transformed by a mapping
- use `.str.replace()` for substring replacement in strings
- use `.loc[...] = ...` for conditional business logic, not simple dictionary-style remaps

## Group-Wise Work: Prefer `transform()` and `filter()`

When every row needs a value derived from its group, `transform()` keeps the result aligned to the original index.

```python
zscore = lambda s: (s - s.mean()) / s.std()

df["bill_zscore"] = (
    df.groupby("time")["total_bill"]
      .transform(zscore)
)
```

This is usually better than:

- looping through groups manually
- calculating group summaries separately and stitching them back row by row

Use `filter()` when the decision is made at the group level but the output should still be rows.

```python
large_days = df.groupby("day").filter(
    lambda g: g["total_bill"].mean() > 20
)
```

Use this mental split:

- `agg()` reduces groups
- `transform()` returns group-derived values aligned to original rows
- `filter()` keeps or drops entire groups

## Use NumPy for Tight Numeric Work

When you are doing pure numeric computation, converting a subset to NumPy can reduce pandas overhead.

```python
values = df[["x1", "x2", "x3"]].to_numpy()
df["row_sum"] = values.sum(axis=1)
```

This is most useful when:

- the columns are numeric
- labels are not needed during the computation
- the operation is large enough that pandas object overhead matters

Do not convert too early if labels, indexes, or mixed dtypes are still important to the logic.

## Accessors and Selection

Performance also improves when the selection method matches the job.

```python
df.loc[5:10, ["a", "b"]]
df.iloc[5:10, 0:2]
df.at[5, "a"]
df.iat[5, 0]
```

- `.at` / `.iat` are for single scalar access
- `.loc` is label-oriented
- `.iloc` is position-oriented

The bigger win is usually not the accessor itself, but avoiding repeated scalar access inside Python loops.

## Efficient Thinking Patterns

When code feels slow, check for these rewrites:

- "loop over rows" -> column expression or `np.where()`
- "if / else per row" -> boolean mask or vectorized condition
- "rebuild each group manually" -> `groupby().transform()` or `groupby().filter()`
- "many exact replacements" -> `.replace({...})`
- "DataFrame math in Python loop" -> `.to_numpy()` plus NumPy operation

## Key Takeaways

- The biggest pandas speedup usually comes from changing the shape of the solution, not micro-tuning syntax.
- Vectorization beats row iteration in most tabular workloads.
- `.apply()` is a compromise tool, not a free optimization.
- `transform()` and `filter()` are the right abstractions for many group-wise tasks.
- Benchmark first, then optimize the slowest pattern you can simplify.
