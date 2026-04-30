# Pipeline Basics



Pipelines are one of the safest ways to build machine learning workflows in `[scikit-learn](../packages/scikit-learn/README.md)`.
They help ensure preprocessing is learned only from training data and applied consistently at inference time.

## Why Use a Pipeline

- Prevent [data leakage](../foundations/data-leakage.md)
- Keep preprocessing and model training together
- Make [cross-validation](cross-validation.md) and [hyperparameter tuning](hyperparameter-tuning.md) safer
- Reuse the exact same transformation logic in production

## Basic Example

```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
```

## Mixed Data Types with ColumnTransformer

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

numeric_features = ["age", "income"]
categorical_features = ["city", "segment"]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ]),
            numeric_features
        ),
        (
            "cat",
            Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore"))
            ]),
            categorical_features
        ),
    ]
)

pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("model", RandomForestClassifier(random_state=42))
])
```

## Hyperparameter Tuning with a Pipeline

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    "model__n_estimators": [100, 300],
    "model__max_depth": [None, 5, 10]
}

search = GridSearchCV(pipeline, param_grid=param_grid, cv=5, scoring="roc_auc")
search.fit(X_train, y_train)
```

## Key Rules

- Put preprocessing inside the pipeline, not before the split.
- Use `ColumnTransformer` when different columns need different preprocessing.
- Tune pipeline steps using names like `model__max_depth`.
- Save the entire pipeline, not only the estimator.

## Related Concepts

- [Data Leakage](../foundations/data-leakage.md)
- [Categorical Encoding](../preprocessing/categorical-encoding.md)
- [Imputation](../preprocessing/imputation.md)
- [Hyperparameter Tuning](hyperparameter-tuning.md)

[Back to Workflow](README.md)
