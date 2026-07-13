# TensorFlow and Keras Basics

## Overview

如果 PyTorch 筆記讓你熟悉了 tensor、gradient 和 module 的基本語感，那 TensorFlow 版本其實是在同一套深度學習觀念上，換一組 API 與工作流。

TensorFlow 2 的核心特色是：

- eager execution 預設開啟，tensor 運算可以像一般 Python 一樣立即看到結果
- 同時提供低階 tensor 操作與高階 `keras` API
- 自動微分、模型定義、訓練流程都整合在同一個框架裡

對初學者來說，最重要的不是背 API，而是先建立這個心智模型：

1. 用 tensor 表示資料
2. 用 `Variable` 表示可訓練參數
3. 用運算式定義前向傳播
4. 用 `GradientTape` 計算梯度
5. 用 optimizer 更新參數
6. 規模變大後改用 `keras` 管理 layer、model 與 training loop

## Tensors and Variables

Tensor 是帶有 shape 與 dtype 的數值容器，可以把它看成 scalar、vector、matrix 以及高維陣列的統一表示。

```python
import tensorflow as tf

scalar = tf.constant(3)
vector = tf.constant([1, 2, 3])
matrix = tf.constant([[1.0, 2.0], [3.0, 4.0]])

zeros = tf.zeros((2, 3))
ones = tf.ones((2, 3))
filled = tf.fill((2, 2), 9)
same_shape_zeros = tf.zeros_like(matrix)
same_shape_ones = tf.ones_like(matrix)
```

常見區分是：

- `tf.constant(...)`: 固定值，適合資料或不需要更新的常數
- `tf.Variable(...)`: 可被訓練或手動更新的狀態，適合權重與 bias

```python
weights = tf.Variable([[-0.05], [-0.01]], dtype=tf.float32)
bias = tf.Variable([0.5], dtype=tf.float32)
```

如果資料型別不一致，訓練時很容易卡住，所以實務上常先做 `cast`：

```python
features = tf.cast(features, tf.float32)
targets = tf.cast(targets, tf.float32)
```

## Basic Tensor Operations

TensorFlow 的低階運算就是在組前向傳播。

```python
a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
b = tf.constant([[5.0, 6.0], [7.0, 8.0]])

tf.add(a, b)
tf.multiply(a, b)
tf.matmul(a, b)
tf.reduce_sum(a)
tf.reshape(a, (4, 1))
```

幾個容易混淆的點：

- `tf.multiply(a, b)` 是 elementwise multiplication
- `tf.matmul(a, b)` 是矩陣乘法
- `tf.reduce_sum(a)` 會把多個值聚合成總和，常出現在 loss 計算
- `tf.reshape(...)` 只改資料排列視角，不改數值本身

影像資料也常先用 reshape 調整維度：

```python
gray_image = tf.random.uniform((28 * 28,), maxval=255, dtype=tf.int32)
gray_image = tf.reshape(gray_image, (28, 28))

color_image = tf.random.uniform((28 * 28 * 3,), maxval=255, dtype=tf.int32)
color_image = tf.reshape(color_image, (28, 28, 3))
```

## Automatic Differentiation with GradientTape

TensorFlow 2 最重要的底層工具之一是 `tf.GradientTape()`。

它的角色是記住前向傳播中哪些運算依賴可訓練變數，之後才能反向算出梯度。

```python
x = tf.Variable(3.0)

with tf.GradientTape() as tape:
    y = x ** 2 + 2 * x + 1

grad = tape.gradient(y, x)
print(grad.numpy())  # 8.0
```

可以把它想成：

- `with GradientTape()` 期間：錄影前向運算
- `tape.gradient(loss, variable)`：回放計算圖，求出導數

這個模式就是手刻訓練 loop 的基礎。

## A Minimal Linear Model in TensorFlow

很多 TensorFlow 入門教材會先用線性回歸示範訓練流程，因為它足夠簡單，但已經完整包含參數、loss、gradient 與 optimizer。

```python
import tensorflow as tf

price = tf.constant([[100.0], [150.0], [200.0]])
size = tf.constant([[1.0], [2.0], [3.0]])

intercept = tf.Variable(0.1)
slope = tf.Variable(0.1)

def model(x):
    return intercept + slope * x

def mse(y_true, y_pred):
    return tf.reduce_mean(tf.square(y_true - y_pred))

optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)

for _ in range(100):
    with tf.GradientTape() as tape:
        preds = model(size)
        loss = mse(price, preds)

    grads = tape.gradient(loss, [intercept, slope])
    optimizer.apply_gradients(zip(grads, [intercept, slope]))
```

這裡最值得記住的是流程，不是語法細節：

1. 參數用 `Variable`
2. 預測函數手動寫出來
3. loss 明確定義
4. tape 算梯度
5. optimizer 更新參數

當 feature 不只一欄時，模型就從單一斜率變成權重向量，通常會改成 `tf.matmul(X, weights) + bias`。

## From Manual Dense Layers to Keras Layers

Dense layer 的本質是：

\[
y = activation(XW + b)
\]

你可以手動組出這個運算：

```python
inputs = tf.constant([[1.0, 35.0]])
weights = tf.Variable([[-0.05], [-0.01]])
bias = tf.Variable([0.5])

logits = tf.matmul(inputs, weights) + bias
outputs = tf.keras.activations.sigmoid(logits)
```

但當模型變複雜，自己管理 shape、初始化與 activation 很快就會變麻煩，所以通常直接交給 `keras.layers.Dense`：

```python
layer = tf.keras.layers.Dense(
    units=1,
    activation="sigmoid",
    kernel_initializer="glorot_uniform"
)

outputs = layer(inputs)
```

這裡可以順便連到幾個關鍵概念：

- activation 決定非線性，常見如 `sigmoid`、`relu`、`softmax`
- initializer 決定權重初始分布，會影響訓練穩定度
- Dense layer 其實就是「線性變換 + 非線性」

如果在隱藏層之間加入 dropout，目的通常是降低過度依賴特定神經元，幫助 regularization。

## Sequential API

當模型是單一路徑、由前往後堆疊時，`keras.Sequential()` 最直觀。

```python
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(16, activation="relu", input_shape=(784,)),
    keras.layers.Dense(8, activation="relu"),
    keras.layers.Dense(4, activation="softmax")
])
```

它適合這種結構：

- 一個輸入
- 一層接一層
- 沒有分支、跳接或多輸入多輸出

典型訓練流程是：

```python
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(
    X_train,
    y_train,
    epochs=10,
    validation_split=0.2
)

model.evaluate(X_test, y_test)
```

可以把這三步理解成：

- `compile`: 決定怎麼學
- `fit`: 開始訓練
- `evaluate`: 用獨立資料檢查效果

## Functional API

如果模型不再是單一路徑，例如：

- 多個輸入來源
- 分支後再合併
- 較複雜的 DAG 結構

這時 Functional API 會比 Sequential 更合適。

```python
from tensorflow.keras import Input, Model, layers

team_in = Input(shape=(1,))
home_in = Input(shape=(1,))

team_vec = layers.Dense(8, activation="relu")(team_in)
home_vec = layers.Dense(8, activation="relu")(home_in)

merged = layers.add([team_vec, home_vec])
output = layers.Dense(1)(merged)

model = Model(inputs=[team_in, home_in], outputs=output)
```

Functional API 的好處不是語法比較炫，而是你可以清楚描述資料流向。

## Batch Training and Input Pipelines

資料量變大後，不會每次都把整份資料一次丟進模型。

常見做法是分 batch 訓練：

```python
import pandas as pd

for batch in pd.read_csv("kc_house_data.csv", chunksize=100):
    x_batch = tf.cast(batch[["sqft_living"]], tf.float32)
    y_batch = tf.cast(batch[["price"]], tf.float32)
```

batch training 的重點：

- 記憶體壓力比較小
- 更新更頻繁
- 梯度比較 noisy，但通常更可擴展

全量訓練則比較穩定，但成本高，也比較不適合大資料。

## Common Beginner Pitfalls

- shape 不對：`Dense` 預期最後一維是 feature 維度
- dtype 不對：整數、字串、浮點數混在一起時常需要 `tf.cast`
- loss 與輸出層不匹配：例如 multi-class classification 常搭配 `softmax` 與 `categorical_crossentropy`
- 把 elementwise multiplication 和 matrix multiplication 搞混
- 只會呼叫 `fit()`，卻不知道底層其實還是「前向傳播 -> loss -> gradient -> update」

## Practical Mental Model

學 TensorFlow/Keras 時，可以把它分成三層：

1. tensor operations: `constant`、`Variable`、`matmul`、`reshape`
2. training mechanics: `GradientTape`、loss、optimizer、batch
3. model abstraction: `Dense`、`Sequential`、Functional API、`compile/fit/evaluate`

真正穩固之後，你會發現 TensorFlow 和 PyTorch 的差異主要在 API 風格，不在深度學習原理本身。
