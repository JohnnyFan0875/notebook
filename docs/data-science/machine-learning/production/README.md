# Production

Production machine learning 不是把 `model.pkl` 存起來就結束，而是要確保輸入資料、特徵流程、模型版本、監控與重訓規則都能長期運作。

## 主題

- [Deployment and Monitoring](deployment-and-monitoring.md)
- [MLOps Overview](mlops-overview.md)

## 這一章的核心問題

- 上線後的輸入 schema 如果改了，模型會不會默默壞掉？
- 模型表現下降時，怎麼知道是資料漂移、概念漂移，還是流程 bug？
- 誰負責決定何時重訓、如何回滾、怎麼驗證新版本？

## 與前面章節的關係

- 沒有 [workflow](../workflow/README.md) 與 [pipeline](../workflow/pipeline-basic.md) 的紀律，production 幾乎一定出問題。
- 沒有 [evaluation](../evaluation/README.md) 的基準與監控指標，上線後也很難知道模型是否退化。

[Back to Machine Learning](../README.md)
