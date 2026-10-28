[Deep Learning](../README.md) › [表示學習](README.md) › 圖神經網路

# 圖神經網路 (Graph Neural Networks, GNN)

很多生物資料天然是圖：分子（原子 = 節點、化學鍵 = 邊）、蛋白質交互作用 (PPI) 網路、基因調控網路、空間轉錄體中相鄰的細胞。GNN 讓每個節點反覆從鄰居收集資訊，學到同時反映自身特徵與圖結構的表示。

古典網路指標（中心性、社群偵測）見 [網路分析](../../network-analysis/README.md)；那些方法不需訓練，常是 GNN 前該先做的 baseline。

## 圖的表示

| 元素 | 符號 | shape | 例子（分子） |
| --- | --- | --- | --- |
| 節點特徵 | $X$ | `(N 節點, F)` | 原子種類、電荷 |
| 邊 | `edge_index` | `(2, E)`，每欄一條邊（來源, 目標） | 化學鍵 |
| 邊特徵（可選） | `edge_attr` | `(E, F_e)` | 單鍵 / 雙鍵 |
| 標籤 | $y$ | 每節點、每邊或每張圖 | 毒性、溶解度 |

> 圖的節點沒有固定順序，所以不能直接把鄰接矩陣攤平丟進 MLP：同一張圖換個節點編號就變成不同輸入。GNN 的運算對節點順序是不變的 (permutation invariant)。

## 訊息傳遞 (Message Passing)

每一層，每個節點：

```
1. 收集：從每個鄰居 u 取得訊息 m = φ(h_u)
2. 彙整：對所有鄰居訊息做順序無關的聚合（sum / mean / max）
3. 更新：h_v ← ψ(h_v, 彙整結果)
```

疊 k 層後，每個節點的表示包含 k 步以內的鄰居資訊（類似 CNN 的感受野）。

| 模型 | 聚合方式 | 特點 |
| --- | --- | --- |
| **GCN** | 依度數正規化的鄰居平均：$H' = \sigma(\tilde D^{-1/2} \tilde A \tilde D^{-1/2} H W)$ | 簡單、強 baseline；$\tilde A = A + I$ 含自環 |
| GraphSAGE | 抽樣部分鄰居再聚合 | 可擴展到大圖、可處理新節點 (inductive) |
| **GAT** | 用 [attention](../nlp-and-transformers/transformers-and-attention.md) 學每個鄰居的權重 | 鄰居重要性不同時 |
| GIN | sum 聚合 + MLP | 分辨圖結構的能力最強，圖層級任務常用 |
| 圖 Transformer | 所有節點互相 attention + 結構編碼 | 大型分子模型 |

## 三種任務

| 層級 | 輸出 | 生資例子 | 關鍵 |
| --- | --- | --- | --- |
| 節點 | 每個節點一個預測 | PPI 網路中預測基因功能 / 疾病基因；空間轉錄體細胞類型 | 同一張大圖切 train / val 節點 |
| 邊（連結預測） | 兩節點間是否有邊 | 預測新的交互作用、藥物–標靶、藥物再利用 | 留出部分邊當測試 |
| 圖 | 每張圖一個預測 | 分子性質（毒性、溶解度、結合親和力） | 需要 readout（全域 pooling） |

## PyTorch Geometric 範例

```python
import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv, global_mean_pool

# 一張 4 節點的無向圖：每條邊兩個方向都要列
edge_index = torch.tensor([[0, 1, 1, 2, 2, 3],
                           [1, 0, 2, 1, 3, 2]])
data = Data(x=torch.randn(4, 16), edge_index=edge_index)

class GCN(torch.nn.Module):
    def __init__(self, f_in, hidden, n_out):
        super().__init__()
        self.conv1, self.conv2 = GCNConv(f_in, hidden), GCNConv(hidden, hidden)
        self.head = torch.nn.Linear(hidden, n_out)

    def forward(self, x, edge_index, batch=None):
        x = F.relu(self.conv1(x, edge_index))
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index)
        if batch is not None:                       # 圖層級任務：每張圖的節點取平均
            x = global_mean_pool(x, batch)
        return self.head(x)

GCN(16, 32, 3)(data.x, data.edge_index).shape       # torch.Size([4, 3])  節點層級
```

多張小圖（分子資料集）用 `torch_geometric.loader.DataLoader` 自動拼成一個大的不相連圖，`batch` 向量記錄每個節點屬於哪張圖。其他選擇：DGL；分子專用的 DeepChem、Chemprop。

## 常見陷阱

| 陷阱 | 說明 |
| --- | --- |
| 過度平滑 (over-smoothing) | 層數一多，所有節點表示趨於相同；GNN 通常只用 2～4 層 |
| 節點任務的資訊洩漏 | 訓練時 message passing 會用到 test 節點的特徵與邊（transductive 設定）；測試邊必須從訓練圖中移除 |
| 連結預測的負樣本 | 「沒有記錄的交互作用」不等於「不存在」，只是還沒測；隨機負樣本會讓分數虛高 |
| 網路本身的偏誤 | PPI 資料庫中研究較多的基因（如 TP53）連結特別多；模型可能只學到「度數高 = 疾病基因」——先和度數 baseline 比較 |
| 分子資料切分 | 隨機切會讓結構相似的分子跨 train / test；用 scaffold split 評估對新化學結構的泛化 |
| 不一定需要 GNN | 分子用指紋 (fingerprint) + 梯度提升樹常是很強的 baseline |
