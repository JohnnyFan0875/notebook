[Data Science](../../README.md) › [Deep Learning](../README.md) › 訓練流程

# 訓練流程 (Training Workflows)

模型能不能訓練成功，常常取決於流程而不是架構：資料怎麼餵、何時停、能否從中斷處恢復、能否借用預訓練權重、硬體夠不夠用。

## 建議順序

```
訓練迴圈 → 存檔與續訓 → 遷移學習 → 效率與擴展
（先能正確訓練）（能恢復）    （資料少時）  （模型 / 資料變大時）
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [PyTorch 訓練迴圈](pytorch-training-loop.md) | Dataset / DataLoader、train / eval 迴圈、指標、scheduler、early stopping、可重現性 | 一個正確的訓練迴圈長什麼樣？ |
| [模型存檔與載入](model-saving-loading.md) | `state_dict`、checkpoint、`weights_only`、跨裝置載入 | 怎麼存模型才能續訓、部署？ |
| [遷移學習](transfer-learning.md) | feature extraction vs fine-tuning、凍結層、torchvision / Hugging Face 預訓練模型 | 資料不多時怎麼借用預訓練模型？ |
| [高效訓練與擴展](efficient-training-and-scaling.md) | 混合精度、gradient accumulation、`torch.compile`、多 GPU | GPU 不夠、訓練太慢時怎麼辦？ |
