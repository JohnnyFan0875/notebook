[LLM](../README.md) › [Agent](README.md) › LangGraph

# LangGraph Agent 工作流程 (LangGraph Agent Workflows)

LangGraph 把 agent 寫成一張**狀態圖**：節點 (node) 是步驟，邊 (edge) 是轉移，狀態 (state) 在節點間傳遞。價值不在「更自主」，而在流程明確：看得到走了哪條路、在哪裡停、哪一步需要人工核准。

## 核心概念

| 元件 | 意義 | 例子 |
| --- | --- | --- |
| State | 在節點間傳遞的資料（常是 message 列表 + 自訂欄位） | `MessagesState`：對話與工具結果 |
| Node | 一個步驟（函式），讀 state、回傳要更新的欄位 | 呼叫模型、執行工具、驗證輸出 |
| Edge | 固定轉移 | `tools` → `model` |
| Conditional edge | 依 state 決定下一個節點 | 模型要求工具 → `tools`；否則 → `END` |
| `START` / `END` | 流程的起點與終點 | — |
| Checkpointer | 每步保存 state | 對話記憶、中斷後恢復、人工核准 |

> 許多 agent 失敗其實是狀態設計失敗：該傳下去的資訊沒傳，後面的步驟就無法正確判斷。

## 最小的 tool-using agent

```
START → model ──(有 tool_calls)──→ tools ──→ model ……
              └─(沒有 tool_calls)──→ END
```

```python
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

@tool
def lookup_gene(symbol: str) -> str:
    """以 HGNC 符號查詢人類基因的官方名稱與 NCBI Gene ID。"""
    ...

tools = [lookup_gene]
llm = ChatOpenAI(model=MODEL, temperature=0).bind_tools(tools)

def call_model(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}   # 回傳的 messages 會被附加到 state

g = StateGraph(MessagesState)
g.add_node("model", call_model)
g.add_node("tools", ToolNode(tools))                       # 執行模型要求的工具，結果寫回 messages
g.add_edge(START, "model")
g.add_conditional_edges("model", tools_condition)          # 有 tool_calls → "tools"，否則 → END
g.add_edge("tools", "model")
app = g.compile(checkpointer=MemorySaver())

config = {"configurable": {"thread_id": "user-42"}, "recursion_limit": 10}   # thread_id 區分對話；限制步數
for state in app.stream({"messages": [("user", "TP53 的官方名稱？")]}, config, stream_mode="values"):
    state["messages"][-1].pretty_print()                    # 逐步看到模型輸出與工具呼叫
```

| 設計 | 理由 |
| --- | --- |
| 模型節點與工具節點分開 | 推理錯誤與工具錯誤不會混在一起 |
| 工具使用是**路由決策** | 可以解釋 agent 為什麼行動，而不只是看到答案 |
| `recursion_limit` | 明確的停止條件，避免無限迴圈 |
| `thread_id` + checkpointer | 同一對話延續狀態；不同使用者互不干擾 |

## 人工核准 (Human-in-the-Loop)

```python
app = g.compile(checkpointer=MemorySaver(), interrupt_before=["tools"])   # 執行工具前暫停

app.invoke({"messages": [("user", "把這 20 筆樣本標記為 QC failed")]}, config)
pending = app.get_state(config).values["messages"][-1].tool_calls      # 檢視模型想執行什麼
# 人確認後繼續；不同意則用 app.update_state(...) 修改或取消
app.invoke(None, config)
```

只對有副作用的工具暫停即可（把唯讀工具和寫入工具分在不同節點）；較新版本也可在節點內用 `interrupt()` 做更細的控制。

## 串流與可觀測性

| 可觀察 | 用途 |
| --- | --- |
| 節點轉移 | 看流程走了哪條路 |
| 模型中間輸出 | 檢查推理是否合理 |
| 工具呼叫與參數 | 確認選對工具、參數正確 |
| 每步延遲 | 找出慢的步驟 |

`stream_mode="values"` 每步輸出完整 state；`"updates"` 只輸出變更部分；`"messages"` 逐 token 串流。搭配 LangSmith 等 tracing 工具可視覺化整條路徑。

## 對話歷史管理

| 策略 | 取捨 |
| --- | --- |
| 保留全部 | 連貫，但 token 成本與雜訊增加 |
| 截斷（保留最近 N 則） | 便宜，可能遺失早期約定；注意不要把 tool call 與對應結果拆開 |
| 摘要舊訊息 | 折衷，但多一個轉換步驟且可能失真 |

## 單一 agent 還是多 agent

| 圖的結構 | 解讀 |
| --- | --- |
| 一個模型節點 + 工具 | 有狀態的單一 agent |
| 多個專職節點、固定順序 | 多步驟工作流程（不一定是 agent） |
| 多個 agent 節點 + 路由 | [多 agent 系統](multi-agent-patterns.md) |

先用圖把流程控制理清楚；只有在專業分工確實帶來價值時才增加 agent。

## 檢查清單

| 問題 | 對應 |
| --- | --- |
| State 裡傳遞了哪些資訊？是否足夠？ | 核心概念 |
| 哪些節點推理、哪些節點執行工具？ | 最小的 agent |
| 什麼條件走工具路徑？什麼條件結束？ | conditional edge、`recursion_limit` |
| 哪些動作需要人工核准？ | 人工核准 |
| 能否看到每一步的輸入、輸出與延遲？ | 串流與可觀測性 |
