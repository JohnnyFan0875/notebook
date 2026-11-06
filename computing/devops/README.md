[Computing](../README.md) › DevOps

# DevOps

讓軟體與資料 pipeline 的變更可以頻繁、可靠地交付：版本控制、自動化測試、CI/CD、容器、監控。

```text
DevOps 基礎（流程、CI/CD 觀念、DORA、微服務）→ GitHub Actions（實作 CI）
```

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [DevOps 基礎](devops-fundamentals.md) | 變更管理、CI vs CD、IaC、漸進式發布、DORA 指標、單體 vs 微服務、DataOps / MLOps | DevOps 在解決什麼？要做哪些事？ |
| [GitHub Actions](github-actions.md) | workflow 結構、Python 測試與矩陣、觸發條件、secrets、artifact、生資用途 | 怎麼讓每個 push / PR 自動測試？ |

| 相關 | 筆記 |
| --- | --- |
| 版本控制與 PR | [Git](../version-control/git.md)、[GitHub 協作](../version-control/github-concepts.md) |
| 容器 | [Docker](../containers-and-env/docker/README.md) |
| 測試 | [Python 測試](../../data-science/python-foundations/testing.md)、[Java 測試](../programming-languages/java/java-testing.md) |
| 模型部署與監控 | [MLOps](../../data-science/machine-learning/production/mlops-overview.md) |
