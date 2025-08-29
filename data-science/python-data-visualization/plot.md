## Data Visualization

```python
dog_pack["height_cm"].hist(bins=10)
avg_weight_by_breed.plot(kind="bar")
sully.plot(x="date", y="weight_kg", kind="line", rot=45)
dog_pack.plot(x="height_cm", y="weight_kg", kind="scatter")
```

- Use `hist`, `bar`, `line`, and `scatter` to explore data visually.
- Add `alpha` for transparency, `legend` for grouping.

import seaborn as sns
import matplotlib.pyplot as plt
sns.histplot(data=books, x="rating")
plt.show()

sns.histplot(data=books, x="rating", binwidth=.1)
plt.show()

sns.boxplot(data=books, x="year", y="genre")

sns.barplot(data=books, x="genre", y="rating")
plt.show()

sns.countplot(data=salaries, x="Job_Category")
plt.show()

sns.boxplot(data=salaries, y="Salary_USD")
plt.show()

sns.lineplot(data=divorce, x="marriage_month", y="marriage_duration")
plt.show()

sns.heatmap(divorce.corr(numeric_only=True), annot=True)
plt.show()

sns.scatterplot(data=divorce, x="income_man", y="income_woman")
plt.show()

sns.pairplot(data=divorce)
plt.show()

sns.pairplot(data=divorce, vars=["income_man", "income_woman", "marriage_duration"])
plt.show()

sns.histplot(data=divorce, x="marriage_duration", binwidth=1)
plt.show()

sns.kdeplot(data=divorce, x="marriage_duration", hue="education_man")
plt.show()

sns.kdeplot(data=divorce, x="marriage_duration", hue="education_man", cut=0)
plt.show()

sns.kdeplot(data=divorce, x="marriage_duration", hue="education_man", cut=0, cumulative=True)
plt.show()

sns.scatterplot(data=divorce, x="woman_age_marriage", y="man_age_marriage")
plt.show()

sns.scatterplot(data=divorce,
x="woman_age_marriage",
y="man_age_marriage",
hue="education_man")
plt.show()

sns.heatmap(planes.corr(numeric_only=True), annot=True)
plt.show()

sns.scatterplot(data=planes, x="Duration", y="Price", hue="Total_Stops")
plt.show()

sns.barplot(data=planes, x="Airline", y="Duration")
plt.show()

sns.boxplot(data=salaries,
y="Salary_USD")
plt.show()

sns.lineplot(data=divorce, x="marriage_month", y="marriage_duration")
plt.show()

sns.heatmap(divorce.corr(numeric_only=True), annot=True)
plt.show()

sns.kdeplot(data=divorce, x="marriage_duration", hue="education_man", cut=0)
plt.show()

df.plot()