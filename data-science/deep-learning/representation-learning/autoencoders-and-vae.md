[Deep Learning](../README.md) › [表示學習](README.md) › Autoencoder 與 VAE

# Autoencoder 與 VAE (Autoencoders and Variational Autoencoders)

Autoencoder 把輸入壓縮成低維的潛在表示 (latent representation) $z$，再從 $z$ 重建輸入；因為中間有瓶頸，模型被迫只保留最重要的結構。VAE 讓 $z$ 服從一個機率分布，因此能生成新樣本、潛在空間也更平滑。單細胞的 scVI、許多批次校正與資料整合方法都是 VAE。

## Autoencoder

```
x (高維，如 2,000 個基因) ─► encoder ─► z (低維，如 10) ─► decoder ─► x̂ (重建)
                                                         loss = ‖x − x̂‖²
```

| 變體 | 改了什麼 | 用途 |
| --- | --- | --- |
| 標準 (undercomplete) | 瓶頸維度 < 輸入維度 | 降維、特徵學習 |
| 去噪 (denoising) | 輸入加雜訊 / 遮蔽，目標是原始乾淨資料 | 插補 (imputation)、學到更穩健的表示 |
| 稀疏 (sparse) | 對 $z$ 加稀疏懲罰 | 可解釋的特徵 |
| 異常偵測 | 只用正常樣本訓練，重建誤差大的視為異常 | 品質控制、罕見樣本 |

> 單層線性 encoder / decoder + MSE loss 的 autoencoder，學到的子空間與 [PCA](../../machine-learning/unsupervised-learning/dimensionality-reduction/pca.md) 相同；加上非線性激活後才能捕捉非線性結構。樣本少時，PCA 往往已經夠好、更穩定也更好解釋。

## VAE：讓潛在空間有機率結構

Encoder 不輸出一個點，而是輸出常態分布的參數 $\mu, \sigma$；從中抽樣得到 $z$ 再解碼。

$$
\mathcal{L} = \underbrace{\mathbb{E}_{q(z|x)}[-\log p(x|z)]}_{\text{重建誤差}} + \beta \cdot \underbrace{D_{KL}\big(q(z|x) \,\|\, \mathcal{N}(0, I)\big)}_{\text{讓 } z \text{ 接近標準常態}}
$$

| 項目 | 說明 |
| --- | --- |
| 重建項 | 負對數似然；連續資料常用 MSE（≈ 常態似然），計數資料用負二項 / ZINB（scVI） |
| KL 項 | 把每個樣本的 $q(z \mid x)$ 拉向 $\mathcal{N}(0, I)$，潛在空間連續、可抽樣；閉式解 $-\frac{1}{2}\sum(1 + \log\sigma^2 - \mu^2 - \sigma^2)$ |
| 重參數化技巧 (reparameterization trick) | $z = \mu + \sigma \odot \epsilon,\ \epsilon \sim \mathcal{N}(0, I)$：把隨機性移到 $\epsilon$，梯度才能穿過抽樣傳回 encoder |
| β | β > 1（β-VAE）讓各維度更獨立、較好解釋，但重建變差 |
| 統計對應 | 整個 loss 是證據下界 (ELBO) 取負號，等同變分推論，見 [貝氏統計](../../statistics/bayesian-statistics/README.md) |

```python
import torch
from torch import nn
import torch.nn.functional as F

class VAE(nn.Module):
    def __init__(self, n_in, n_latent=10, hidden=128):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(n_in, hidden), nn.ReLU())
        self.mu, self.logvar = nn.Linear(hidden, n_latent), nn.Linear(hidden, n_latent)
        self.dec = nn.Sequential(nn.Linear(n_latent, hidden), nn.ReLU(), nn.Linear(hidden, n_in))

    def forward(self, x):
        h = self.enc(x)
        mu, logvar = self.mu(h), self.logvar(h)              # 輸出 log σ² 確保變異數為正
        z = mu + torch.exp(0.5 * logvar) * torch.randn_like(mu)   # 重參數化
        return self.dec(z), mu, logvar

def vae_loss(x, x_hat, mu, logvar, beta=1.0):
    recon = F.mse_loss(x_hat, x, reduction="sum") / len(x)
    kl = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp()) / len(x)
    return recon + beta * kl

model = VAE(n_in=2000)
x = torch.randn(64, 2000)                                    # 例：log 標準化後的 2,000 個高變異基因
x_hat, mu, logvar = model(x)
loss = vae_loss(x, x_hat, mu, logvar)

# 使用：取 μ 當作每個樣本的低維表示（不抽樣），再接 UMAP / 分群
model.eval()
with torch.no_grad():
    z = model.mu(model.enc(x))                               # (64, 10)
```

## 條件 VAE 與批次校正

把批次 (batch) 標籤 $s$ 同時餵給 encoder 與 decoder（conditional VAE）：decoder 已經知道批次資訊，$z$ 就不需要編碼批次差異，留下的主要是生物變異。這是 scVI 做資料整合的核心想法，見 [單細胞深度學習](../bio-applications/single-cell-deep-learning.md)。

## 常見問題

| 問題 | 說明 / 處理 |
| --- | --- |
| Posterior collapse | decoder 太強、KL 把 $z$ 壓成和輸入無關；KL annealing（β 從 0 慢慢升到 1）、減弱 decoder |
| 重建模糊 | VAE 生成的影像常偏模糊；要高品質生成改用 diffusion 模型 |
| 潛在維度怎麼選 | 依下游任務（分群、整合指標）比較 10 / 20 / 30；沒有唯一正確值 |
| 潛在空間距離的意義 | 只在訓練資料覆蓋的範圍內可信；不同 seed 的座標軸不可比，比較的是鄰近關係 |
| 過度校正 | 批次與生物條件混雜 (confounded) 時，校正可能把真實差異一起抹掉——實驗設計問題，模型救不了，見 [混雜與偏誤](../../statistics/experimental-design/confounding-bias.md) |
