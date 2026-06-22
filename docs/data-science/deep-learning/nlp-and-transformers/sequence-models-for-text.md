# Sequence Models for Text

在 transformer 成為主流前，文字深度學習大量依賴 RNN、LSTM、GRU 等 sequence models。即使現在很多專案直接用 transformer，理解 sequence modeling 仍然很重要，因為它幫助你掌握「語序」與「狀態傳遞」的基本概念。

## 這類模型在做什麼

- 一次讀入一個 token
- 把前面資訊壓進 hidden state
- 再用 hidden state 影響後續預測

## 為什麼會遇到限制

- 序列太長時，早期資訊難以保留
- 訓練難以平行化
- 容易有 vanishing / exploding gradients

## LSTM / GRU 的價值

它們透過 gating 機制，讓模型比較能保留重要資訊、忘記不重要資訊，因此比最基本的 vanilla RNN 更穩定。

## 常見任務

- sentiment analysis
- text classification
- language modeling
- sequence generation

## 判讀提醒

- 若你只是做短文字分類，簡單模型未必輸 transformer 太多。
- 若資料很少，sequence model 也可能比大 transformer 更容易穩定訓練。
- 若任務需要長距離依賴，transformer 通常更有優勢。
