# NMF



## Overview

- **NMF (Non-negative Matrix Factorization)** decomposes a non-negative matrix into two lower-dimensional non-negative matrices (**W** and **H**).
- Applications: dimensionality reduction, feature extraction, and pattern recognition.
- Especially useful where interpretability is important: **image processing, topic modeling, collaborative filtering, biology (gene expression patterns)**.
- Compared to [PCA](pca.md), NMF ensures components and weights are non-negative, making them easier to interpret as “parts-based” representations.

## Example: Simple Matrix Factorization

```python
import numpy as np
from sklearn.decomposition import NMF

V = np.array([[5, 0, 3, 0, 2],
              [0, 3, 0, 2, 4],
              [1, 0, 4, 3, 0],
              [0, 1, 0, 5, 3]])

# row: documents 1-4, column: words 1-5

model = NMF(n_components=2, random_state=42) # 2 topics

W = model.fit_transform(V) # 4x2: Document-topic matrix
H = model.components_      # 2x5: Topic-word matrix

V_reconstructed = np.dot(W, H) # 4x5 reconstruction
```

- **W (basis matrix)**: rows = documents, columns = topics, values = weight of topics per document.
- **H (coefficient matrix)**: rows = topics, columns = words, values = weight of words per topic.

## Visualization of Decomposition

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 3, figsize=(15, 5))

# Plot original matrix V
ax[0].imshow(V, aspect='auto', cmap='Blues')
ax[0].set_title('Original Matrix V')
ax[0].set_xlabel('Features')
ax[0].set_ylabel('Samples')

# Plot basis matrix W
ax[1].imshow(W, aspect='auto', cmap='Blues')
ax[1].set_title('Basis Matrix W')
ax[1].set_xlabel('Components')
ax[1].set_ylabel('Samples')

# Plot coefficient matrix H
ax[2].imshow(H, aspect='auto', cmap='Blues')
ax[2].set_title('Coefficient Matrix H')
ax[2].set_xlabel('Features')
ax[2].set_ylabel('Components')

plt.tight_layout()
plt.show()
```

---

## Cosine Similarity with NMF

### Overview

- **Cosine similarity** measures the cosine of the angle between two vectors (values range from -1 to 1).
- In the context of NMF:
  - Compare **documents** (rows of W) based on topic distribution.
  - Compare **topics** (rows of H) based on their word distributions.
- **High cosine similarity (close to 1)** → vectors are very similar in orientation (similar topics or documents).
- **Low similarity (close to 0)** → vectors are unrelated.

### Example: Document and Topic Similarity

```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import cosine_similarity

documents = [
    "I love programming in Python.",
    "Python and machine learning are awesome.",
    "I love data science and machine learning.",
    "Data science is my favorite field.",
    "I am learning about machine learning algorithms."
]

# Convert text to bag-of-words representation
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

# Fit NMF
nmf = NMF(n_components=2, random_state=1)
W = nmf.fit_transform(X)  # Document-topic matrix
H = nmf.components_       # Topic-term matrix

# Cosine similarity for documents
cos_sim_matrix_docs = cosine_similarity(W)
sns.heatmap(cos_sim_matrix_docs, annot=True, cmap='Blues',
            xticklabels=documents, yticklabels=documents)
plt.title("Cosine Similarity Matrix for Documents")
plt.show()

# Cosine similarity for topics
cos_sim_matrix_topics = cosine_similarity(H)
sns.heatmap(cos_sim_matrix_topics, annot=True, cmap='Blues',
            xticklabels=[f"Topic {i+1}" for i in range(H.shape[0])],
            yticklabels=[f"Topic {i+1}" for i in range(H.shape[0])])
plt.title("Cosine Similarity Matrix for Topics")
plt.show()
```

### Recommended Notes

- Use **cosine similarity** when analyzing similarity between documents or topics in NMF results.
- Alternative measures: **Pearson correlation** (linear relationships) or **Jaccard similarity** (binary features).
- NMF + cosine similarity is widely used in **topic modeling** and **text [clustering](../clustering/README.md)**.
- Always validate interpretability with **domain knowledge** (e.g., topics should align with meaningful themes).

## Related Concepts

- [Dimensionality Reduction](README.md)
- [PCA](pca.md)
- [t-SNE](tsne.md)
- [Feature Engineering Principles](../../foundations/feature-engineering-principles.md)

[Back to Dimensionality Reduction](README.md)
