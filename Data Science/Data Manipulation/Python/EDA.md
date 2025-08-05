# Explo

## Crosstab
pd.crosstab(df['name'], df['age'])

.head()
.info()
.shape()
.describe()
.values()
.columns
.index

dogs.isna()
dogs.isna().sum().plot(kind="bar")

# summary
.median()
.mode()
.min()
.max()
.var() , .std()
.sum()
.quantile()

def pct30(column):
return column.quantile(0.3)
dogs["weight_kg"].agg(pct30)
dogs[["weight_kg", "height_cm"]].agg(pct30)
def pct40(column):
return column.quantile(0.4)
dogs["weight_kg"].agg([pct30, pct40])
dogs["weight_kg"].cumsum()
.cummax()
.cummin()
.cumprod()

# counting
.value_counts
.value_counts(sort=True) normalize=True

# calculation
dogs[dogs["color"] == "Black"]["weight_kg"].mean()