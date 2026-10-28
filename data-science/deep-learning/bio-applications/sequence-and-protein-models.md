[Deep Learning](../README.md) › [生資應用](README.md) › 序列與蛋白模型

# 序列與蛋白模型 (DNA and Protein Sequence Models)

DNA 與蛋白質都是由固定字母組成的序列，可以直接套用 [1D CNN](../computer-vision/convolutional-neural-networks.md#1d-cnn序列也能用) 與 [Transformer](../nlp-and-transformers/transformers-and-attention.md)。實務上分兩條路：**針對任務從頭訓練**（例如預測某轉錄因子是否結合），或**使用大型預訓練模型**（蛋白質語言模型、基因體模型）抽 embedding 或直接零樣本 (zero-shot) 預測。

## 任務地圖

| 任務 | 輸入 → 輸出 | 代表方法 |
| --- | --- | --- |
| 轉錄因子結合、染色質可及性 | DNA 片段（數百 bp）→ 是否有 peak | DeepSEA、Basset（one-hot CNN） |
| 基因表現 / 表觀訊號軌跡 | 長 DNA（數十 kb 以上）→ 每個位置的 ChIP / ATAC / CAGE 訊號 | Basenji、Enformer、Borzoi |
| 剪接 (splicing) | pre-mRNA 序列 → 剪接位點機率 | SpliceAI |
| 非編碼變異效應 | 參考 vs 變異序列的預測差異 | 上述模型的 in silico mutagenesis |
| 錯義變異 (missense) 致病性 | 蛋白質序列 + 突變 → 分數 | ESM 零樣本、AlphaMissense |
| 蛋白質功能 / 定位 / 穩定性 | 蛋白質序列 → 類別或數值 | ESM embedding + 簡單分類器 |
| 蛋白質結構 | 序列 → 3D 座標 | AlphaFold2 / 3、ESMFold、RoseTTAFold |

## DNA：one-hot + CNN

```python
import numpy as np
import torch
from torch import nn

def one_hot(seq):
    """ACGT → (4, L)；N 等未知鹼基為全 0。"""
    idx = {"A": 0, "C": 1, "G": 2, "T": 3}
    x = np.zeros((4, len(seq)), dtype=np.float32)
    for i, b in enumerate(seq.upper()):
        if b in idx:
            x[idx[b], i] = 1
    return torch.from_numpy(x)

class MotifCNN(nn.Module):
    def __init__(self, n_tasks=1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(4, 128, kernel_size=19, padding="same"), nn.ReLU(),   # 第一層 kernel ≈ motif 偵測器
            nn.MaxPool1d(4),
            nn.Conv1d(128, 128, kernel_size=9, padding="same"), nn.ReLU(),  # 組合 motif（間距、共同出現）
            nn.AdaptiveMaxPool1d(1), nn.Flatten(),                          # 不論在哪裡出現都算
            nn.Linear(128, n_tasks),                                        # 多任務：多個 TF / 細胞型各一個 logit
        )
    def forward(self, x):
        return self.net(x)

x = torch.stack([one_hot("ACGT" * 250), one_hot("TTGACA" * 166 + "AAAA")])   # (2, 4, 1000)
MotifCNN(n_tasks=3)(x).shape                       # torch.Size([2, 3])  → BCEWithLogitsLoss
```

| 設計 | 理由 |
| --- | --- |
| 第一層 kernel 長 10～25 | 涵蓋一般 TF motif 長度；訓練後的 kernel 可轉成 PWM 與 JASPAR 比對 |
| 反向互補 augmentation 或平均正反兩股預測 | 多數 TF 結合沒有股別方向 |
| 多任務輸出 | 同時預測數百個 ChIP / DNase 實驗，共享特徵、資料利用更有效率 |
| 負樣本選擇 | 隨機基因體背景太容易分辨（GC 含量不同）；用 GC 配對或其他細胞型的 peak |

## 長序列基因體模型

| 模型 | 年份 | 想法 | 輸入範圍 |
| --- | --- | --- | --- |
| Basenji | 2018 | 擴張卷積 (dilated convolution) 擴大感受野 | 約 100 kb 以上 |
| **Enformer** | 2021 | CNN 縮短序列後接 Transformer，捕捉遠端增強子 | 約 200 kb |
| Borzoi | 2023 | 預測 RNA-seq 覆蓋度（含剪接、聚腺苷酸化） | 約 500 kb |
| AlphaGenome | 2025 | 多模態訊號、變異效應 | 約 1 Mb |

> 模型輸入範圍與輸出軌跡數依版本不同，使用前查原始論文與官方說明。這類模型預測的是**參考基因體**上的平均訊號；用在個人變異上時，對「哪個基因受影響、影響方向」的準確度明顯不如對 peak 位置的預測。

## DNA 語言模型

| 模型 | Tokenization | 特點 |
| --- | --- | --- |
| DNABERT / DNABERT-2 | 重疊 k-mer / BPE | BERT 式 MLM 預訓練 |
| Nucleotide Transformer | 非重疊 6-mer | 多物種、多個模型大小 |
| HyenaDNA、Caduceus | 單鹼基 | 非 attention 架構，可處理很長的序列；Caduceus 內建反向互補對稱 |
| Evo / Evo 2 | 單鹼基 | 大規模、跨原核與真核的生成式模型 |

> 多個獨立 benchmark 顯示，DNA 語言模型的 embedding 在許多調控任務上並沒有穩定勝過針對任務訓練的 CNN；蛋白質語言模型的優勢則明確得多。拿來用前，先和簡單的 one-hot CNN baseline 比較。

## 蛋白質語言模型 (ESM)

ESM-2（Meta，2022–2023）以數千萬條蛋白質序列做遮蔽語言模型預訓練，模型大小從 8M 到 15B 參數。它學到的是演化約束：哪個位置能容忍哪些胺基酸。

| 用法 | 做法 | 適合 |
| --- | --- | --- |
| 抽 embedding | 每個殘基的向量（殘基層級任務）或平均（蛋白質層級） | 功能、定位、穩定性預測；接 logistic 迴歸 / MLP |
| 零樣本變異效應 | 遮住突變位置，比較突變型與野生型的 log 機率 | 沒有標註資料時篩選錯義變異 |
| Fine-tune | 加分類頭或 LoRA | 有數千筆以上標註 |
| 結構預測 | ESMFold：單序列、不需 MSA，比 AlphaFold 快 | 大量序列、宏基因體蛋白 |

```python
import torch
from transformers import AutoTokenizer, AutoModel, EsmForMaskedLM

name = "facebook/esm2_t33_650M_UR50D"             # 測試流程可先用 esm2_t6_8M_UR50D
tok = AutoTokenizer.from_pretrained(name)

# 1. 蛋白質層級 embedding：排除 padding 後平均（含 <cls>/<eos>，要更嚴謹可一併排除）
enc = AutoModel.from_pretrained(name).eval()
batch = tok(["MKTAYIAKQRQISFVKSHFSRQ", "MKTAYIAK"], return_tensors="pt", padding=True)
with torch.no_grad():
    h = enc(**batch).last_hidden_state            # (2, L, 1280)
m = batch["attention_mask"].unsqueeze(-1)
emb = (h * m).sum(1) / m.sum(1)                   # (2, 1280) → 接 sklearn 分類器

# 2. 零樣本變異分數：log P(突變型) − log P(野生型)，越負越可能破壞功能
mlm = EsmForMaskedLM.from_pretrained(name).eval()
seq, pos, wt, mt = "MKTAYIAKQRQISFVKSHFSRQ", 5, "Y", "A"   # pos 為 1-based
ids = tok(seq, return_tensors="pt")["input_ids"]  # 開頭自動加 <cls>，所以 1-based 位置 = token 索引
ids[0, pos] = tok.mask_token_id
with torch.no_grad():
    logp = mlm(input_ids=ids).logits[0, pos].log_softmax(-1)
score = logp[tok.convert_tokens_to_ids(mt)] - logp[tok.convert_tokens_to_ids(wt)]
```

## 蛋白質結構預測 (AlphaFold)

| 工具 | 輸入 | 輸出 / 特點 |
| --- | --- | --- |
| AlphaFold2（2021） | 序列 + 多序列比對 (MSA) + 模板 | 單鏈結構；**AlphaFold DB** 已預先算好 UniProt 中兩億多條蛋白的結構 |
| AlphaFold-Multimer | 多條鏈 | 蛋白質複合體 |
| AlphaFold3（2024） | 蛋白質、DNA、RNA、配體、修飾 | 複合體與交互作用；使用條款有限制 |
| ESMFold | 單序列 | 快，準確度略低（尤其缺乏同源序列時差距較小） |
| ColabFold | 序列 | AlphaFold2 + 快速 MSA，最容易上手的執行方式 |

| 信心指標 | 意義 | 判讀 |
| --- | --- | --- |
| pLDDT（每個殘基 0～100） | 局部結構的信心 | > 90 很高；70～90 主鏈可信；< 50 多為無序區 (IDR) 或預測失敗 |
| PAE（殘基對的預期位置誤差） | 兩個區域的相對位置是否可信 | 結構域之間 PAE 高 → 各自可信，但相對擺放不可信 |
| ipTM | 複合體介面的信心 | 低時不要據此推論交互作用 |

> 預測結構是單一靜態構形：不代表構形變化、突變後的結構、或真實的結合親和力。低 pLDDT 區域常是真的無序，不是「模型不夠好」。蛋白質資料庫見 [UniProt](../../../biology/molecular-biology/molecular-databases/uniprot.md)、[InterPro](../../../biology/molecular-biology/molecular-databases/interpro.md)。

## 評估陷阱

| 陷阱 | 後果 | 正確做法 |
| --- | --- | --- |
| 隨機切分蛋白質 | 同源蛋白（序列相似度 > 30%）跨 train / test，模型只是在「查相似序列」 | 先用 MMseqs2 / CD-HIT 依相似度分群，**以群為單位切分** |
| 隨機切分基因體區段 | 相鄰、重疊的片段跨 train / test | 依染色體留出 test |
| 預訓練資料包含測試序列 | ESM、AlphaFold 訓練時見過 UniProt / PDB，test 序列可能早已被看過 | 檢查與預訓練資料的時間 / 相似度 |
| 變異 benchmark 的標籤循環 | ClinVar 的部分標籤本來就是參考計算預測分數而來 | 用 MAVE / DMS 等實驗資料（ProteinGym）評估 |
| 只報 AUROC | 正樣本極少時 AUROC 看起來很好 | 一併報 AUPRC，見 [ROC 與 AUC](../../machine-learning/evaluation/roc-auc.md) |
