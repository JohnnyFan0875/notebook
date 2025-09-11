# Confusion Matrix

A **confusion matrix** is used to evaluate the performance of a classification model. It summarizes prediction results by comparing actual labels vs. predicted labels.

## Key Metrics

- **Accuracy** = (TP + TN) / (TP + TN + FP + FN)  
  _Proportion of total correct predictions._

- **Sensitivity / Recall / True Positive Rate (TPR)** = TP / (TP + FN)  
  _Ability of the model to correctly identify positives._

- **Specificity / True Negative Rate (TNR)** = TN / (TN + FP)  
  _Ability of the model to correctly identify negatives._

- **Precision / Positive Predictive Value (PPV)** = TP / (TP + FP)  
  _Out of predicted positives, how many are actually positive._

- **F1-score** = 2 × (Recall × Precision) / (Recall + Precision)  
  _Harmonic mean of precision and recall, balances false positives and false negatives._

## Example in Python

```python
from sklearn.metrics import confusion_matrix, classification_report

conf_matrix = confusion_matrix(y_test, y_pred)

print(conf_matrix)
'''
Confusion Matrix:
[[140  12]        [[TN   FP]
 [ 16 132]]        [FN   TP]]
'''

class_report = classification_report(y_test, y_pred)
print(class_report)
'''
Classification Report:
              precision    recall  f1-score   support

           0       0.90      0.92      0.91       152
           1       0.92      0.89      0.91       148

    accuracy                           0.91       300
   macro avg       0.91      0.91      0.91       300
weighted avg       0.91      0.91      0.91       300

# Binary classification: class 0 / class 1 = negative / positive outcome
# Support: Number of actual occurrences of each class in the dataset
'''
```

## Critical Notes

- **Accuracy** can be misleading in **imbalanced datasets**. Example: If 95% of data belongs to one class, predicting everything as that class yields 95% accuracy but poor performance.
- **Recall** is important in medical diagnoses (e.g., catching as many true positives as possible).
- **Precision** is important in scenarios where false positives are costly (e.g., spam detection).
- **F1-score** is a balanced measure, especially useful when data is imbalanced.
- **Specificity** complements recall: together they describe performance on negatives and positives.
- Use **macro avg** when you want to give equal weight to all classes, and **weighted avg** when class imbalance exists.

## Key Takeaways

- Confusion matrix provides a detailed breakdown of classification performance.
- **Precision vs Recall tradeoff**: higher precision reduces false positives, higher recall reduces false negatives.
- **F1-score** balances precision and recall.
- **Specificity** is crucial when the correct identification of negatives matters.
- Always interpret **accuracy** alongside other metrics for a complete picture.
