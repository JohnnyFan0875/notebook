[Data Science](../../README.md) › [LLM](../README.md) › Agent

# LLM Agent

Agent 是能自己決定下一步、呼叫工具、根據結果繼續執行的 LLM 系統。它比固定流程更有彈性，也更難預測、測試與控制；所以先問「真的需要 agent 嗎？」。

## 建議順序

```
Agent 基礎（何時需要、工具、guardrail）→ LangGraph（狀態、節點、條件路由）→ 多 Agent（swarm vs supervisor）
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Agent 基礎](agent-foundations.md) | 從 chatbot 到 agent、thought-action-observation 迴圈、工具設計、適用判斷、guardrail 與人工介入 | 什麼時候該用 agent？怎麼設計得安全？ |
| [LangGraph 工作流程](langgraph-agent-workflows.md) | state、node、edge、tool node、停止條件、串流、checkpoint 與人工核准 | 怎麼讓 agent 的流程可見、可控？ |
| [多 Agent 模式](multi-agent-patterns.md) | 條件路由、swarm、supervisor、共享狀態 | 什麼時候值得拆成多個 agent？ |

> 單一、範圍明確、工具精簡的 agent，通常勝過複雜的多 agent 系統。只有在任務確實需要拆分職責時才增加 agent。上線後的營運見 [LLMOps](../llmops.md#agent-系統的營運)。
