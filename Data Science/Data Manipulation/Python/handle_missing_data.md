## Handling Missing Data

```python
dogs.isna()
dogs.dropna()
dogs.fillna(0)
dogs.isna().sum().plot(kind="bar")
```