Supervised/Unsupervised Learning

- Unsupervised Learning: Uncovering hidden patterns from unlabeled data e.g. clustering
- Supervised Learning: The predicted values are known

Naming conventions

- Feature = predictor variable = independent variable = explanatory variable
- Target variable = dependent variable = response variable
- Labeled data = training data

Hyperparameter

- parameters that are set before training a machine learning model
- Not learned from the data. manually specified
- Ridge/lasso regression: alpha
  KNN: n_neighbors

# Preprocessing

# Model training, evaluation, tuning

## Model training (fitting)

- hyperparameter tuning (e.g. grid search) if required

## Model tuning

- Analyze feature importance (e.g., for tree-based models).
- Perform model diagnostics (e.g., residual plots for regression, confusion matrix for classification).
- Tune hyperparameters further based on the evaluation results.
- Refine features or even add new data if needed.

# Model Deployment

- deploy it to make predictions on new, unseen data.
  - Save the trained model (e.g., using `joblib` or `pickle`).
  - Create an API or integration layer for real-time predictions.
  - Monitor model performance in production and update when necessary.

# FAQ

1. if all the datasets (independent variables + dependent variables) are fit_transform before splitting into train/test data → data leakage
2. model performance:
   1. regression model: RMSE, R-squared
   2. classification model: accuracy, confusion matrix, precision, recall, F1-score, ROC, AUC
3. how to know which feature has greater influence on the model
   1. classification: model.feature*importances* (decision tree, gradient boosting, random forest)
   2. regression: model.coef\_

# Unsupervised Learning

- find patterns in data without a specific prediction task in mind
- dimension: number of features
