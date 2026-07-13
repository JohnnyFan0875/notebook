# Linear Algebra Foundations for Multivariate Analysis

多變量分析真正困難的地方，常常不是演算法名稱，而是你是否能把資料看成向量、矩陣與線性轉換。這些概念一旦穩定下來，PCA、multiple regression、LDA 甚至 clustering 的數學形式都會變得比較自然。

Key point: 線性代數在資料科學裡不是抽象符號遊戲，而是描述「多個變數如何一起變動」的語言。

## Why It Matters

當資料從單一變數變成多變數時，最自然的表示方式就是矩陣：

- 每一列代表一個 observation
- 每一欄代表一個 variable
- 一整個資料表可以視為一個 data matrix

一旦接受這個表示法，很多常見任務都會變成矩陣問題：

- regression: 解釋輸入矩陣如何映射到 outcome
- PCA: 找到最能保留變異的方向
- covariance structure: 描述變數如何共同變動
- dimensionality reduction: 用較少軸保留主要資訊

## Vectors: One Variable or One Direction

向量可以有兩種直覺：

- 把它看成單一變數的一串數值
- 把它看成多維空間中的一個方向

例如一位球員的 combine 測量值：

\[
x = \begin{bmatrix}
71 \\
192 \\
4.38 \\
35.0
\end{bmatrix}
\]

這個向量同時代表：

- 一筆 observation 的多個特徵
- 四維空間中的一個點

這種雙重視角很重要，因為 multivariate analysis 幾乎都在處理「點雲在高維空間中的結構」。

## Basic Vector Operations

最基本的運算有三種：

### Scalar multiplication

\[
c x
\]

表示把向量的每個分量都乘上同一個常數。幾何上，這表示沿著原方向拉長、縮短，或反向。

### Vector addition

\[
x + y
\]

表示把兩個向量逐項相加。這個觀念在 regression 與 PCA 裡很常見，因為許多結果都可寫成多個方向的線性組合。

### Linear combination

\[
a_1 v_1 + a_2 v_2 + \cdots + a_k v_k
\]

這是整個線性代數最核心的觀念之一。當我們問「這個向量能不能由另外幾個向量組出來」，其實就是在問它是否位於那些向量張成的空間中。

Key point: regression 的 fitted value、PCA 的 component score、matrix factorization 的近似表示，本質上都在使用線性組合。

## Matrices: Many Variables at Once

矩陣可以視為：

- 多個向量排在一起
- 一個資料表的數值表示
- 一個線性轉換的操作規則

若資料矩陣為：

\[
X =
\begin{bmatrix}
x_{11} & x_{12} & \cdots & x_{1p} \\
x_{21} & x_{22} & \cdots & x_{2p} \\
\vdots & \vdots & \ddots & \vdots \\
x_{n1} & x_{n2} & \cdots & x_{np}
\end{bmatrix}
\]

那麼：

- `n` 是 observation 數
- `p` 是 variable 數

這正是 multivariate data 的標準形式。

## Matrix-Vector Multiplication

矩陣乘向量：

\[
A x
\]

不是單純的記號操作，而是把向量 `x` 經過一個線性轉換 `A`。這個轉換可能代表：

- 旋轉
- 伸縮
- 反射
- 投影
- 上述效果的組合

這個幾何直覺非常關鍵，因為它讓你知道矩陣不是「很多數字排成方格」，而是「把資料從一個座標系統搬到另一個座標系統」。

在資料科學裡，這個觀念會反覆出現：

- PCA 是把資料投影到新的正交座標軸
- regression 是把輸入特徵映射到預測值
- embeddings 也是把物件映射到向量空間

## Systems of Linear Equations

當我們寫：

\[
A x = b
\]

問題就變成：是否存在一個向量 `x`，使得矩陣 `A` 經過線性轉換後得到 `b`？

這種問題可以有幾種情況：

- 有唯一解
- 有無限多解
- 無解

這背後反映的是：

- `A` 的欄向量是否足以張成 `b`
- 欄向量之間是否彼此冗餘

這和 multicollinearity 的直覺很接近。當 predictors 太接近彼此的線性組合時，矩陣問題就會變得不穩定。

## Eigenvalues and Eigenvectors

eigenvector 是在某個矩陣轉換下「方向不變」的特殊向量；eigenvalue 則描述那個方向被放大或縮小多少。

\[
A v = \lambda v
\]

其中：

- `v` 是 eigenvector
- `\lambda` 是 eigenvalue

直覺上，矩陣通常會把大部分向量轉到新方向，但少數特定方向只會被伸縮，不會改變方向。這些特殊方向就是 eigenvectors。

## Why Eigenvectors Matter in Data Science

當矩陣是 covariance matrix 時：

- eigenvectors 代表資料主要變動方向
- eigenvalues 代表每個方向上的變異大小

這正是 PCA 的核心。

因此可以把 PCA 理解成：

1. 先用 covariance matrix 描述多變量資料的共同變動
2. 再找出這個矩陣的 eigenvectors
3. 用 eigenvalues 判斷每個方向保留了多少資訊

第一主成分不是憑空產生的新欄位，而是資料中最重要的變異方向。

## Orthogonality

在 PCA 與很多 multivariate 方法裡，`orthogonal` 很重要。兩個向量正交，表示它們彼此垂直，內積為 0：

\[
x^T y = 0
\]

在資料分析裡，這通常可以讀成：

- 兩個方向互不重疊
- 一個方向沒有攜帶另一個方向已經表達的線性資訊

PCA 之所以有用，正是因為每個 principal component 都和前面的 component 正交，所以不會重複解釋同一塊線性變異。

## Covariance Matrix as a Summary Object

當資料經過中心化後，covariance matrix 是理解多變量結構的起點：

\[
\Sigma = \frac{1}{n - 1} X^T X
\]

這個矩陣濃縮了所有變數之間的共同變動：

- 對角線是各變數自己的變異
- 非對角線是兩兩 covariances

如果某些欄位高度冗餘，covariance matrix 的結構通常會顯示出明顯相關性，這也是為什麼 PCA 常被用來做 redundancy reduction。

## PCA as a Change of Basis

很多人第一次學 PCA 會把它當成一個黑箱降維工具，但更好的理解方式是：

- 原始資料是在舊座標系統下表示
- PCA 找到一組新的正交基底
- 這組新基底按解釋變異大小排序

所以 PCA 不是單純刪資料，而是先旋轉座標軸，再決定只保留最有資訊量的方向。

Key point: PCA 本質上是 change of basis，不只是壓縮技巧。

## Practical Interpretation Habits

- 當你看到 matrix multiplication，先問自己這代表的是哪種轉換。
- 當你看到線性方程組，先問這是在解唯一解、冗餘解，還是不可解問題。
- 當你看到 eigenvectors，先把它想成資料最穩定或最重要的方向。
- 當你看到 PCA，先把它想成「找新座標系統」，再談保留幾個 components。

## Common Mistakes

- 把向量只當成欄位資料，忘記它同時代表空間中的方向。
- 把矩陣只當成表格，而不是線性轉換。
- 背下 `Av = \lambda v`，卻不知道 eigenvector 為什麼和 PCA 有關。
- 以為 PCA 是神奇 feature engineering，其實它只是把資料投影到更有資訊密度的方向。
- 在高度不同量尺的變數上直接做 PCA，忘記 scale 會主導結果。

## Where to Go Next

- 如果你想把這些概念用在降維，下一步看 [Principal Component Analysis (PCA)](./pca.md)。
- 如果你想先看多變量資料的相關結構，先看 [Multivariate EDA](./multivariate-eda.md)。
- 如果你想理解多個 predictors 如何一起解釋 outcome，接著看 [Multiple Linear Regression](./multiple-regression.md)。
