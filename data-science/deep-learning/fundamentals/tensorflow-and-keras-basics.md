[Deep Learning](../README.md) › [基礎](README.md) › PyTorch ↔ Keras 對照

# PyTorch ↔ TensorFlow / Keras 對照

本章以 PyTorch 為主。深度學習的觀念（tensor、autograd、loss、optimizer）在兩個框架完全相同，差別在 API 風格：PyTorch 自己寫訓練迴圈，Keras 用 `compile` / `fit` 包起來。這篇讓你看得懂 Keras 程式碼並換算成 PyTorch。

> Keras 3（TensorFlow 2.16 起的預設）是多後端框架，可跑在 TensorFlow、JAX 或 PyTorch 上；`import keras` 取代過去的 `from tensorflow import keras`。

## 對照表

| 任務 | PyTorch | TensorFlow / Keras |
| --- | --- | --- |
| 建立 tensor | `torch.tensor(x)`、`torch.zeros(2, 3)` | `tf.constant(x)`、`tf.zeros((2, 3))` |
| 可訓練參數 | `nn.Parameter`（層內自動建立） | `tf.Variable` |
| 型別轉換 | `t.float()`、`t.to(torch.float32)` | `tf.cast(t, tf.float32)` |
| 矩陣乘法 / 逐元素 | `a @ b` / `a * b` | `tf.matmul(a, b)` / `tf.multiply(a, b)` |
| 改形狀 | `t.reshape(28, 28)` | `tf.reshape(t, (28, 28))` |
| 加總 | `t.sum()` | `tf.reduce_sum(t)` |
| 自動微分 | `loss.backward()` → `w.grad` | `with tf.GradientTape() as tape:` → `tape.gradient(loss, w)` |
| 全連接層 | `nn.Linear(in, out)` + 另外加激活 | `keras.layers.Dense(out, activation="relu")`（自動推斷 in） |
| 卷積 | `nn.Conv2d(C_in, C_out, k)`，輸入 `(N, C, H, W)` | `layers.Conv2D(C_out, k)`，輸入 `(N, H, W, C)` |
| 循序模型 | `nn.Sequential(...)` | `keras.Sequential([...])` |
| 多輸入 / 分支 | 繼承 `nn.Module`，在 `forward` 寫資料流 | Functional API：`Input` → 層 → `keras.Model(inputs, outputs)` |
| 損失 | `nn.CrossEntropyLoss()`（吃 logits + 類別索引） | `SparseCategoricalCrossentropy(from_logits=True)` |
| 訓練 | 自寫迴圈：forward → loss → backward → step | `model.compile(optimizer, loss, metrics)` → `model.fit(...)` |
| 評估 / 推論 | `model.eval()` + `torch.no_grad()` | `model.evaluate()` / `model.predict()` |
| 資料管線 | `Dataset` + `DataLoader` | `tf.data.Dataset`（`.batch().shuffle().prefetch()`） |
| Early stopping / checkpoint | 自己寫（見 [訓練迴圈](../training-workflows/pytorch-training-loop.md)） | `callbacks=[EarlyStopping(...), ModelCheckpoint(...)]` |
| 存檔 | `torch.save(model.state_dict(), "m.pt")` | `model.save("m.keras")` |
| 初始化 | `nn.init.xavier_uniform_` | `kernel_initializer="glorot_uniform"` |

> Loss 名稱對照最容易出錯：Keras 的 `categorical_crossentropy` 要 **one-hot** 標籤、`sparse_categorical_crossentropy` 要**整數**標籤；預設輸入是機率（最後一層要 softmax），除非設 `from_logits=True`。PyTorch 的 `CrossEntropyLoss` 一律吃 logits 與整數標籤。

## 同一個模型兩種寫法

```python
# Keras
import keras
from keras import layers

model = keras.Sequential([
    keras.Input(shape=(784,)),                 # Keras 3 建議用 Input，取代 Dense(input_shape=...)
    layers.Dense(64, activation="relu"),
    layers.Dropout(0.2),
    layers.Dense(10),                          # logits
])
model.compile(optimizer="adam",
              loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2,
          callbacks=[keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)])
```

```python
# PyTorch：同樣的架構；fit() 的內容要自己寫，見 PyTorch 訓練迴圈
import torch
from torch import nn

model = nn.Sequential(
    nn.Linear(784, 64), nn.ReLU(), nn.Dropout(0.2),
    nn.Linear(64, 10),
)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
```

## GradientTape：Keras 的手寫訓練步

需要自訂訓練邏輯時，TensorFlow 用 `GradientTape` 記錄 forward，等同 PyTorch 的 autograd：

```python
import tensorflow as tf

x = tf.Variable(3.0)
with tf.GradientTape() as tape:
    y = x**2 + 2*x + 1
tape.gradient(y, x)                            # 8.0   dy/dx = 2x + 2

# 一步訓練
with tf.GradientTape() as tape:
    loss = loss_fn(y_true, model(x_batch, training=True))   # training=True 讓 dropout / BN 用訓練模式
grads = tape.gradient(loss, model.trainable_variables)
optimizer.apply_gradients(zip(grads, model.trainable_variables))
```

| 觀念 | PyTorch | TensorFlow |
| --- | --- | --- |
| train / eval 模式 | `model.train()` / `model.eval()` 切換整個模型 | 呼叫時傳 `training=True/False` |
| 梯度清零 | 要 `optimizer.zero_grad()` | 每次新的 tape，不需清零 |
| 生資 / 研究生態 | 多數新模型（ESM、scvi-tools、MONAI、Hugging Face）以 PyTorch 為主 | 較早期的基因體模型（如 Basenji、Enformer 原始實作）用 TensorFlow |
