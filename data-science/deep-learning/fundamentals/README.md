[Data Science](../../README.md) › [Deep Learning](../README.md) › 基礎

# 深度學習基礎 (Fundamentals)

神經網路的底層元件：資料怎麼表示、一層在算什麼、怎麼量化錯誤、梯度怎麼回傳、參數從哪裡開始、怎麼防止過擬合。這層穩了，CNN、Transformer 都只是元件的不同組合。

## 建議順序

```
tensor → linear layer → activation → loss → 反向傳播 / optimizer → 初始化 → 正則化與 normalization
(資料)    (一層的運算)   (非線性)     (目標)   (怎麼更新)            (起點)      (怎麼不過擬合、怎麼穩)
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Tensor](tensors.md) | 建立、shape / dtype / device、autograd、與 NumPy 互轉 | 資料在 PyTorch 裡長什麼樣？ |
| [線性層](linear-layer.md) | $XW^\top + b$、參數量、手算輸出 | 一層全連接在算什麼？有多少參數？ |
| [激活函數](activation-functions.md) | sigmoid、tanh、ReLU、GELU、softmax 與導數 | 為什麼需要非線性？隱藏層用哪個？ |
| [損失函數](loss-functions.md) | CrossEntropy、BCEWithLogits、MSE、輸出層搭配 | 這個任務該用哪個 loss？輸入是 logits 還是機率？ |
| [反向傳播與 Optimizer](backpropagation.md) | 鏈鎖律、autograd、學習率、SGD / Adam / AdamW | 梯度怎麼算？參數怎麼更新？ |
| [權重初始化](weight-initialization.md) | Xavier、Kaiming、預設初始化、重設層 | 為什麼初始化會讓訓練成功或失敗？ |
| [正則化與 Normalization](regularization-and-normalization.md) | dropout、weight decay、BatchNorm、LayerNorm、augmentation | 怎麼防過擬合、讓深層網路穩定？ |
| [PyTorch ↔ Keras 對照](tensorflow-and-keras-basics.md) | 兩框架的 API 對照表 | 看得懂 Keras 程式碼嗎？ |
