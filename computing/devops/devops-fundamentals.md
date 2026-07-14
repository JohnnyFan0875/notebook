# DevOps Fundamentals

DevOps 不是單一工具，也不只是把開發與維運放在同一張組織圖。它比較像一種工作方式，目標是讓軟體從需求、開發、測試、部署到營運的整條流程更快、更穩、更可控。

## DevOps 在解決什麼

大型產品常見的問題包括：

- 系統很複雜，跨團隊協作成本高
- 需求、開發、測試、部署彼此斷開
- 每次改動都很慢，風險又大
- 上線後出了問題，很難快速定位與回滾

DevOps 的核心價值，就是把這些斷點縮短，讓 change 可以更頻繁，但風險更可管理。

## 不只是 Dev 和 Ops 靠近

如果把 DevOps 只理解成「開發也要懂維運」，會太狹窄。比較完整的理解是：

- 跨角色協作要更早發生
- 軟體交付要更多自動化
- 測試、部署、監控要變成同一條流程的一部分
- 變更管理要從手工審批轉向可驗證、可追蹤的 pipeline

## 一條簡化的 DevOps 流程

教材中的 change management model，可以整理成這樣的順序：

1. requirements
2. design
3. development
4. testing
5. deployment
6. monitoring and feedback

DevOps 並不是讓這些步驟消失，而是讓它們之間更連續，並盡量透過 automation 降低等待與手工錯誤。

## 變更管理是核心，不是附屬品

很多團隊以為 DevOps 只是 CI/CD，但其實 change management 才是底層主題。

每一次變更都在問：

- 需求有沒有對齊
- 改動是否可測
- 上線是否可回滾
- 風險是否能被觀察

如果這些問題沒有制度化，即使有自動部署，也只是把混亂更快送到 production。

## CI/CD 的角色

CI/CD 是 DevOps 裡最常被看見的一層，但它應該被理解成機制，不是目的。

### Continuous Integration

CI 的重點是：

- 頻繁整合程式碼
- 盡早跑測試
- 盡早發現衝突與缺陷

### Continuous Delivery / Deployment

CD 的重點是：

- 把可部署流程標準化
- 減少手工上線步驟
- 讓變更更小、更頻繁、更容易回滾

教材反覆提到的一個核心觀念是：CI/CD pipeline 把 build、testing、deployment 自動化，讓 change management 變得比較可控。

## Microservices 與 Monolith

DevOps 常和 architecture decision 一起出現，尤其是 monolith 與 microservices 的對比。

### Monolithic Architecture

monolith 的特徵是：

- 整體是一個較大的單位
- 概念上比較單純
- 但維護與變更風險容易集中

### Microservices Architecture

microservices 的特徵是：

- 系統拆成較小、可獨立部署的服務
- 每個服務各自處理特定功能
- 常有自己的資料與邏輯

這種架構的優點是變更邊界較清楚，但代價是協調、觀察與部署複雜度上升。

### DevOps 為什麼常和 Microservices 綁在一起

當服務被拆小之後：

- 變更次數會增加
- 整合面會增加
- 測試與部署頻率會增加
- 監控需求會增加

這就是為什麼 microservices 幾乎一定需要更成熟的 DevOps 實踐。

## Data Engineering 也受 DevOps 影響

教材裡有一條很重要的線索：DevOps 不只影響產品工程，也會影響 data engineering。

原因包括：

- data pipelines 本身也是可變更的系統
- 資料流程也需要測試、部署與監控
- 微服務化架構下，資料常分散在多個服務與私有資料庫之間

所以從 data team 的角度看，DevOps 的延伸其實很接近 DataOps 或 pipeline engineering discipline。

## Observability 不是可有可無

變更越頻繁，越需要 observability。

它的價值在於：

- 更早發現問題
- 協助定位故障來源
- 看見改動後的系統行為
- 幫助回滾與後續改善

如果團隊能自動部署，卻沒有足夠的 logs、metrics、traces 或其他可觀測訊號，那每次上線都還是在賭。

## Testing 與 Reliability

DevOps 很強調 automated testing，不只是因為省人工，而是因為頻繁變更如果沒有自動驗證，就無法穩定擴張。

可以把 testing 想成兩層：

- 上線前：避免明顯錯誤進入環境
- 上線後：透過 observability 與 feedback 判斷系統是否真的穩定

也因此，reliability 不是單靠 deployment tool 達成的，而是 testing、monitoring、rollback discipline 一起形成的。

## Data Quality 與 DevOps 的關係

第四章把焦點拉到 data quality，這很值得保留。

重點不是 DevOps 自己生出高品質資料，而是：

- 好的軟體流程更容易產生可信資料
- 自動化測試可以幫助發現資料流程錯誤
- observability 可以更早看見資料品質異常
- 並非所有資料都需要同樣等級的品質要求

這意味著 data quality 也應該被放進工程流程治理，而不只是靠事後人工檢查。

## 一個實務上的心智模型

理解 DevOps 時，可以先記四件事：

1. `flow`
   需求到上線的交付流程要更短、更順
2. `automation`
   build、test、deploy、check 都盡量制度化
3. `feedback`
   問題要能更快被看到
4. `reliability`
   變更要快，但不能靠運氣

當這四件事能一起運作時，DevOps 才算真的落地。

## 常見誤區

- 把 DevOps 等同於某一套工具鏈
- 只有部署自動化，沒有測試與 observability
- 以為 microservices 天生比較進步，忽略了治理成本
- 把 data quality 當成純資料團隊問題，而不是工程流程問題

## Related Concepts

- [Git](../version-control/git.md)
- [GitHub Concepts](../version-control/github-concepts.md)
- [Containerization and Virtualization](../containers-and-env/containerization-and-virtualization.md)
- [Deployment and Monitoring](../../data-science/machine-learning/production/deployment-and-monitoring.md)

[Back to DevOps](README.md)
