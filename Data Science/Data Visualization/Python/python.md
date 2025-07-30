## Data Visualization

```python
dog_pack["height_cm"].hist(bins=10)
avg_weight_by_breed.plot(kind="bar")
sully.plot(x="date", y="weight_kg", kind="line", rot=45)
dog_pack.plot(x="height_cm", y="weight_kg", kind="scatter")
```

- Use `hist`, `bar`, `line`, and `scatter` to explore data visually.
- Add `alpha` for transparency, `legend` for grouping.
