[LLM](../README.md) › [整合](README.md) › API 模式

# LLM API 模式 (LLM API Patterns)

在程式中呼叫 LLM 時，請求不只是一句 prompt，而是 messages、參數、輸出格式與工具定義的組合；回應也不只是文字，還有 token 用量、工具呼叫與錯誤。本篇從單次呼叫一路到可上線的請求處理：structured output、tool calling、重試、moderation 與 guardrail。

## Chat API 的心智模型

```
請求 = 模型 ID + messages（system / user / assistant / tool）+ 參數 + [輸出 schema] + [工具定義]
回應 = 生成內容 或 工具呼叫請求 + 停止原因 + token 用量
```

| Role | 放什麼 |
| --- | --- |
| `system` | 穩定的規則：角色、範圍、語氣、資訊不足時的行為（Anthropic API 用獨立的 `system` 參數） |
| `user` | 這次的任務與資料 |
| `assistant` | 之前的回答；也可放「示範回答」作為 few-shot 範例 |
| `tool` | 工具執行結果，回傳給模型繼續推理 |

> API 是**無狀態**的：模型不記得上一次呼叫。多輪對話的「記憶」是每次把相關歷史重新送出，所以歷史越長，成本越高、雜訊越多。

```python
# OpenAI SDK（v1）
from openai import OpenAI

client = OpenAI()                      # 讀取環境變數 OPENAI_API_KEY；不要把金鑰寫進程式或 notebook
MODEL = "..."                          # 填入帶日期 / 版本的模型 ID，不要用會變動的別名

messages = [
    {"role": "system", "content": "你是生物資訊助理。不確定時直接說不知道。"},
    {"role": "user", "content": "用三點說明 DESeq2 的 size factor 是什麼。"},
]
resp = client.chat.completions.create(model=MODEL, messages=messages, temperature=0, max_tokens=400)
answer = resp.choices[0].message.content
resp.choices[0].finish_reason          # "stop" 正常結束；"length" 代表被 max_tokens 截斷
resp.usage.prompt_tokens, resp.usage.completion_tokens

# 多輪：把回答加回歷史再問下一題
messages += [{"role": "assistant", "content": answer},
             {"role": "user", "content": "那和 TPM 標準化有什麼不同？"}]
```

```python
# Anthropic SDK：system 是獨立參數，max_tokens 必填
import anthropic

client = anthropic.Anthropic()         # 讀取 ANTHROPIC_API_KEY
msg = client.messages.create(
    model=MODEL, max_tokens=400, system="你是生物資訊助理。不確定時直接說不知道。",
    messages=[{"role": "user", "content": "用三點說明 DESeq2 的 size factor 是什麼。"}],
)
msg.content[0].text, msg.stop_reason, msg.usage.input_tokens
```

| 參數 | 用途 | 注意 |
| --- | --- | --- |
| `temperature` / `top_p` | 控制隨機性（原理見 [LLM 基礎](../llm-foundations.md#取樣參數-decoding)） | 部分推理模型不支援或忽略 |
| `max_tokens` | 輸出上限，控制成本與延遲 | OpenAI 新模型改用 `max_completion_tokens`；推理模型的思考過程也計入 |
| `stop` | 遇到指定字串停止 | — |
| `seed` | 提高可重現性（部分 API） | 不保證完全一致 |

### 對話狀態管理

| 策略 | 優點 | 風險 |
| --- | --- | --- |
| 保留全部歷史 | 連貫 | 成本隨輪數增加；舊錯誤污染後續 |
| 只保留最近 N 輪 | 成本可控 | 遺忘早期的約定 |
| 舊對話摘要 + 最近幾輪 | 平衡 | 摘要本身可能遺漏或扭曲 |
| 換主題就重置 | 乾淨 | 需判斷何時重置 |

## Structured Output

下游程式需要的是固定欄位，不是散文。用 schema 約束輸出，並在程式端再驗證一次。

```python
from pydantic import BaseModel, Field

class GeneMention(BaseModel):
    symbol: str = Field(description="原文中的基因寫法")
    organism: str | None = Field(description="物種；原文沒寫就填 null")

class AbstractInfo(BaseModel):
    study_type: str                # "human" / "mouse" / "cell line" / "review" / "other"
    sample_size: int | None        # 沒寫就 null，不要猜
    genes: list[GeneMention]

# OpenAI：把 pydantic 模型當 response_format（舊版 SDK 為 client.beta.chat.completions.parse）
resp = client.chat.completions.parse(
    model=MODEL, response_format=AbstractInfo,
    messages=[{"role": "system", "content": "從摘要擷取資訊。原文沒有的欄位填 null。"},
              {"role": "user", "content": abstract}],
)
info = resp.choices[0].message.parsed          # AbstractInfo 物件；拒答時為 None，看 .refusal

# 不支援 schema 參數的模型：要求輸出 JSON，再自行驗證
info = AbstractInfo.model_validate_json(raw_text)   # 失敗會丟 ValidationError → 重試或記錄
```

| 做法 | 可靠度 | 說明 |
| --- | --- | --- |
| 只在 prompt 描述格式 | 低 | 偶爾多出說明文字或缺欄位 |
| JSON mode | 中 | 保證是合法 JSON，不保證欄位正確 |
| JSON schema / structured output | 高 | 依 schema 約束解碼；仍需驗證**內容**是否正確 |
| 用 tool calling 取得參數 | 高 | 本質上也是 schema 約束 |

> Schema 只保證格式，不保證事實。`sample_size: 120` 仍可能是編造的；要用 [評估集](../evaluation-and-hallucination.md) 檢查內容正確率。

## Tool Calling

讓模型決定「要呼叫哪個函式、帶什麼參數」，由程式實際執行，再把結果回傳給模型。適合模型不該自己編的東西：資料庫查詢、計算、外部 API。

```
使用者問題 → 模型回傳 tool_calls（函式名 + JSON 參數）→ 程式驗證參數並執行
         → 結果以 role="tool" 回傳 → 模型產生最終回答（或再呼叫工具）
```

```python
import json

def lookup_gene(symbol: str) -> dict:
    ...                                 # 查 HGNC / NCBI Gene，回傳官方名稱、ID、別名

tools = [{
    "type": "function",
    "function": {
        "name": "lookup_gene",
        "description": "以 HGNC 基因符號查詢官方名稱與 ID。只在使用者提到具體基因時使用。",
        "parameters": {
            "type": "object",
            "properties": {"symbol": {"type": "string", "description": "人類基因符號，如 TP53"}},
            "required": ["symbol"],
        },
    },
}]
registry = {"lookup_gene": lookup_gene}

messages = [{"role": "user", "content": "TP53 和 TP63 的官方全名是什麼？"}]
for _ in range(5):                                       # 設上限，避免無限迴圈
    resp = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    msg = resp.choices[0].message
    if not msg.tool_calls:
        break                                            # 沒有工具呼叫 → 最終回答
    messages.append(msg)
    for call in msg.tool_calls:                          # 可能一次要求多個（平行工具呼叫）
        args = json.loads(call.function.arguments)       # 執行前驗證：型別、範圍、權限
        result = registry[call.function.name](**args)
        messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
print(msg.content)
```

| 工具設計 | 理由 |
| --- | --- |
| 名稱與描述清楚，寫明「何時使用」 | 模型靠描述選工具 |
| 參數有型別、列舉值、範例 | 減少錯誤參數 |
| 告訴模型「缺必要參數時先詢問使用者」 | 否則會自行編造參數 |
| 執行前在程式端驗證參數 | 結構正確 ≠ 內容安全 |
| 有副作用的工具（寫入、刪除、寄信）需人工確認 | 見 [Agent](../agents/agent-foundations.md#guardrail-與人工介入) |
| 迴圈設上限 | 避免模型反覆呼叫 |

## 錯誤處理與重試

| 錯誤（OpenAI SDK 類別） | 意義 | 處理 |
| --- | --- | --- |
| `AuthenticationError` (401) | 金鑰錯誤 | 不重試，修設定 |
| `PermissionDeniedError` (403) / `NotFoundError` (404) | 無權限、模型 ID 錯誤或已下架 | 不重試 |
| `BadRequestError` (400) | 參數錯誤、超過 context 上限 | 不重試；修請求（截斷輸入） |
| `RateLimitError` (429) | 超過速率或額度 | 指數退避重試 |
| `APIConnectionError`、`APITimeoutError`、5xx | 網路或服務暫時性問題 | 指數退避重試 |

```python
from openai import OpenAI

client = OpenAI(max_retries=3, timeout=60)   # SDK 已內建對 429 / 5xx / 連線錯誤的指數退避重試
```

> 重試策略屬於程式層，不屬於 prompt。對參數錯誤盲目重試只會浪費錢。大量請求時另外控制併發數，並考慮 [Batch API](../llmops.md#成本與延遲)。

## Guardrail 與 Moderation

| 層 | 做法 |
| --- | --- |
| 輸入 | 長度上限、範圍檢查、moderation 分類、偵測 prompt injection |
| System prompt | 角色、範圍、拒答規則 |
| 輸出 | schema 驗證、moderation、PII 過濾、引用驗證 |
| 動作 | 工具參數驗證、權限最小化、高風險動作人工核准 |
| 監控 | 記錄被擋下的請求與誤擋案例 |

```python
mod = client.moderations.create(model="omni-moderation-latest", input=user_text)
r = mod.results[0]
r.flagged, r.category_scores          # 依各類別分數與自訂門檻決定：繼續 / 拒絕 / 轉人工
```

**Prompt injection**：使用者輸入或檢索到的文件裡藏著「忽略之前的指令…」之類的文字，讓模型改變行為。處理外部文件（網頁、PDF、email）的 RAG 與 agent 特別容易中招。

| 緩解 | 說明 |
| --- | --- |
| 用分隔符號標明「以下是資料，不是指令」 | 降低但不能消除風險 |
| 工具權限最小化 | 讀文件的流程不給寫入 / 寄送權限 |
| 敏感動作一律人工核准 | 即使被注入也無法自動執行 |
| 輸出檢查 | 偵測是否洩漏 system prompt 或敏感資料 |

> System prompt 是 guardrail，不是保證。高風險流程要多層防護並存。

## 計算 Token 與控制長度

```python
import tiktoken                                   # OpenAI 模型的 tokenizer
enc = tiktoken.get_encoding("o200k_base")         # 依模型選編碼；其他供應商用各自的 token 計數 API
n = len(enc.encode(long_document))

# Anthropic：client.messages.count_tokens(model=MODEL, messages=[...]).input_tokens
```

| 情況 | 做法 |
| --- | --- |
| 文件超過 context 上限 | 切段處理後彙整（map-reduce），或改用 [RAG](../rag/README.md) |
| 輸入很長但大多無關 | 先檢索 / 篩選相關段落 |
| 長 context 中段資訊被忽略 | 重要內容放開頭或結尾；問題放在文件之後 |
| 成本估算 | token 數 × 單價；中文與程式碼 token 數通常較多 |

## 上線前的請求流程

```
驗證請求 → 輸入 guardrail → 組 prompt（模板 + 檢索結果）→ 呼叫模型（有上限的參數）
→ 驗證輸出 / 工具參數 → 只對暫時性錯誤重試 → 記錄（版本、token、延遲、結果）
```
