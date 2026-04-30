# Stacking



Stacking combines predictions from multiple base models and feeds them into a meta-model.

## Core Idea

- Train several diverse base learners
- Generate out-of-fold predictions from them
- Use those predictions as inputs to a second-level model

## Why Use It

- Different models capture different patterns
- The meta-model can learn when to trust each base model
- Often improves predictive performance when single models plateau

## Risks

- More complex training and debugging
- Easy to leak information if out-of-fold predictions are not used correctly
- Harder to interpret and maintain

## Example

```python
from sklearn.ensemble import StackingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

estimators = [
    ("rf", RandomForestClassifier(n_estimators=200, random_state=42)),
    ("knn", KNeighborsClassifier(n_neighbors=7)),
    ("svm", SVC(probability=True, random_state=42))
]

stack = StackingClassifier(
    estimators=estimators,
    final_estimator=LogisticRegression(max_iter=1000),
    cv=5
)

stack.fit(X_train, y_train)
```

## Practical Note

Always evaluate stacking against a strong single-model [baseline](../../evaluation/baselines-and-error-analysis.md), because the added complexity is not always worth it.

## Related Concepts

- [Voting Ensemble Learning](voting.md)
- [Baselines and Error Analysis](../../evaluation/baselines-and-error-analysis.md)
- [Cross-Validation Methods](../../workflow/cross-validation.md)
- [Model Lifecycle](../../workflow/model-lifecycle.md)

[Back to Ensemble Methods](README.md)
