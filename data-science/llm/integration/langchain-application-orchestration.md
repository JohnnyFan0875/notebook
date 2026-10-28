[LLM](../README.md) › [整合](README.md) › LangChain

# LangChain 應用編排 (LangChain Application Orchestration)

LangChain 提供統一介面，把 prompt 模板、模型、retriever、工具、output parser 串成流程。價值在於**組合與替換**：換模型供應商、重用 prompt、把檢索接進同一條 pipeline，而不必重寫膠水程式碼。單一 prompt、單一回應的任務直接呼叫 [API](llm-api-patterns.md) 更單純。

## 核心元件

| 元件 | 用途 | 例子 |
| --- | --- | --- |
| Chat model | 各供應商的統一介面 | `ChatOpenAI`、`ChatAnthropic`、`ChatOllama`（本機） |
| Prompt 模板 | 帶變數的 prompt 物件 | `ChatPromptTemplate`、`FewShotPromptTemplate` |
| Output parser | 把模型輸出轉成字串、JSON 或物件 | `StrOutputParser`、`with_structured_output()` |
| Retriever | 給問題回傳相關文件 | 向量庫的 `.as_retriever()` |
| Tool | 可被模型呼叫的函式 | `@tool` 裝飾器 |
| Document loader / splitter | 讀取與切分文件 | PDF、HTML、Markdown loader；`RecursiveCharacterTextSplitter` |

所有元件都實作 **Runnable** 介面（`invoke`、`batch`、`stream`），所以能用 `|` 串接，這就是 LCEL (LangChain Expression Language)。

## LCEL：用 `|` 串流程

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI          # 換供應商只要換這一行（langchain_anthropic、langchain_ollama…）

llm = ChatOpenAI(model=MODEL, temperature=0)

# 1. prompt → model → parser
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是{field}領域的審稿人，回答簡潔。"),
    ("user", "列出這段方法描述中可能影響可重現性的問題：\n\n{methods}"),
])
chain = prompt | llm | StrOutputParser()
chain.invoke({"field": "單細胞定序", "methods": methods_text})
chain.batch([{"field": ..., "methods": m} for m in many_methods])   # 平行處理多筆

# 2. 結構化輸出：直接回傳 pydantic 物件
from pydantic import BaseModel
class Review(BaseModel):
    issues: list[str]
    severity: str
structured = prompt | llm.with_structured_output(Review)

# 3. 串接兩步：第一步的輸出成為第二步的輸入
summarize = ChatPromptTemplate.from_template("用三句話摘要：{text}") | llm | StrOutputParser()
translate = ChatPromptTemplate.from_template("翻成英文：{summary}") | llm | StrOutputParser()
pipeline = {"summary": summarize} | translate
pipeline.invoke({"text": long_text})
```

| 好處 | 說明 |
| --- | --- |
| 每一步可單獨測試 | 失敗時知道是 prompt、模型、檢索還是解析出錯 |
| 內建 `batch`、`stream`、非同步 | 不必自己寫併發 |
| 可接 tracing（LangSmith 等） | 看到每一步的輸入輸出 |

## 檢索也是一個步驟

```python
from langchain_core.runnables import RunnablePassthrough

def format_docs(docs):
    return "\n\n".join(f"[{d.metadata['source']}]\n{d.page_content}" for d in docs)

rag_prompt = ChatPromptTemplate.from_template(
    "只根據以下資料回答，並標註來源；資料中沒有就說找不到。\n\n{context}\n\n問題：{question}")
rag_chain = ({"context": retriever | format_docs, "question": RunnablePassthrough()}
             | rag_prompt | llm | StrOutputParser())
```

完整的 RAG 流程（切分、embedding、向量庫、評估）見 [RAG Pipeline](../rag/rag-pipeline.md)。框架簡化了接線，但**不會替你選對 chunk 大小、檢索策略或資料來源**。

## Chain、Agent、Graph 的分工

| 型態 | 流程 | 用什麼 |
| --- | --- | --- |
| Chain | 固定步驟，事先已知 | LCEL |
| RAG chain | 固定步驟 + 檢索 | LCEL + retriever |
| Tool-using agent | 由模型動態決定下一步呼叫哪個工具 | [LangGraph](../agents/langgraph-agent-workflows.md) |
| 有分支、迴圈、人工核准的流程 | 明確的狀態與轉移 | [LangGraph](../agents/langgraph-agent-workflows.md) |

流程能事先寫死就用 chain；下一步取決於中間結果時才用 agent。

## 值不值得用框架

| 值得 | 不值得 |
| --- | --- |
| 要支援多個模型供應商 | 單一 prompt、單一回應 |
| prompt、retriever、parser 在多個任務重用 | 抽象層讓除錯更困難 |
| 多步驟流程、需要 tracing | 團隊不需要可攜性或元件重用 |
| 檢索與工具是流程的一部分 | 只用一家 API 的基本功能 |

> LangChain 版本演進快、套件拆分多（`langchain-core`、`langchain-openai`、`langchain-community`…），網路上的舊範例常無法執行。以官方文件當前版本為準，並在專案中鎖定版本。
