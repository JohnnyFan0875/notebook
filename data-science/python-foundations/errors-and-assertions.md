[Data Science](../README.md) › [Python Foundations](README.md) › 錯誤處理與斷言

# 錯誤處理與斷言 (Errors & Assertions)

`try`/`except` 處理**預期中可能發生**的執行期錯誤（檔案不存在、網路逾時）；`raise` 主動拒絕不合法的輸入；`assert` 檢查**照理不該發生**的內部假設。三者用途不同，不要互相取代。

| 工具 | 回答的問題 | 例子 |
| --- | --- | --- |
| `try` / `except` | 這一層能不能合理恢復？ | 下載失敗 → 重試；缺檔 → 跳過並記錄 |
| `if ...: raise` | 呼叫端給的東西是否違反約定？ | `alpha` 不在 0–1 之間 |
| `assert` | 程式本身有沒有寫錯？ | 內部函式假設輸入已排序 |
| 測試 (`pytest`) | 功能是否符合預期？ | 見 [測試](testing.md) |

## `try` / `except`

```python
try:
    df = pd.read_csv(path)
except FileNotFoundError:
    log.warning("missing %s, skipped", path)       # 能恢復：記錄後繼續
    df = None
except (pd.errors.ParserError, UnicodeDecodeError) as e:
    raise ValueError(f"cannot parse {path}") from e  # 不能恢復：轉成更清楚的錯誤往上丟
else:
    log.info("loaded %d rows", len(df))           # 沒有例外才執行
finally:
    cleanup_tmp()                                  # 無論如何都執行（清理）
```

| 子句 | 何時執行 |
| --- | --- |
| `except X` | `try` 內發生 `X`（或其子類別） |
| `else` | `try` 完全沒出錯 |
| `finally` | 一定執行，即使 `return` 或再次丟出例外 |

> 檔案、連線的清理優先用 `with`（context manager），比 `finally` 手動關閉安全，見 [函式](function.md#context-manager)。

### 原則

| 原則 | 錯誤示範 | 原因 |
| --- | --- | --- |
| 捕捉**具體**例外 | `except:` / `except Exception:` 包一大段 | 會吞掉 `KeyboardInterrupt`、拼字錯誤造成的 `NameError` |
| `try` 區塊越小越好 | 整個函式包在 `try` 裡 | 不知道是哪一行出錯 |
| 不要靜默吞掉 | `except ValueError: pass` | 錯誤消失，結果卻是錯的 |
| 轉換例外時保留原因 | `raise NewError(...)`（沒有 `from`） | `raise ... from e` 保留原始 traceback |
| 記錄完整 traceback | `print(e)` | `log.exception(...)` 會附上 stack trace |

### 取得錯誤資訊

```python
import logging, traceback
log = logging.getLogger(__name__)

try:
    1 / 0
except ZeroDivisionError as err:
    type(err).__name__        # 'ZeroDivisionError'
    str(err)                  # 'division by zero'
    traceback.format_exc()    # 完整 traceback 字串
    tb = traceback.extract_tb(err.__traceback__)[-1]
    tb.filename, tb.lineno, tb.name   # 出錯的檔案、行號、函式名
    log.exception("division failed")  # 在 except 內使用：自動附 traceback
```

logging 設定見 [腳本與 CLI](scripting-and-cli.md)。

## `raise`：主動拒絕不合法輸入

選語意明確的例外類別，上層才能精準捕捉並分別處理。

| 例外 | 意義 |
| --- | --- |
| `TypeError` | 型別不對（傳了 str 給要 list 的參數） |
| `ValueError` | 型別對但值不合理（負的樣本數、p 值 > 1） |
| `KeyError` / `IndexError` | 缺少必要的 key / 索引超出範圍 |
| `FileNotFoundError` | 檔案不存在 |
| `NotImplementedError` | 子類別必須覆寫的方法 |
| `RuntimeError` | 其他執行期狀態錯誤 |

```python
def set_alpha(alpha: float) -> float:
    if not isinstance(alpha, (int, float)):
        raise TypeError(f"alpha must be a number, got {type(alpha).__name__}")
    if not 0 < alpha < 1:
        raise ValueError(f"alpha must be in (0, 1), got {alpha}")
    return alpha

# 自訂例外：讓呼叫端能區分「你的套件的錯」和其他錯誤
class SampleSheetError(ValueError):
    """Raised when the sample sheet is malformed."""

def check_sheet(df):
    missing = {"sample_id", "condition"} - set(df.columns)
    if missing:
        raise SampleSheetError(f"missing columns: {sorted(missing)}")
    if df["sample_id"].duplicated().any():
        raise SampleSheetError("duplicated sample_id")
```

> 在資料進入分析的**入口**做驗證（讀檔後馬上檢查欄位、重複、範圍），比在管線中段才出現奇怪的 NaN 好除錯得多。大型表格驗證可用 `pandera` 或 Great Expectations，見 [資料品質檢查](../data-engineering/data-quality-checks.md)。

## `assert`：檢查內部假設

```python
assert condition, "message shown on failure"   # 不成立就丟 AssertionError

def merge_counts(a, b):
    assert list(a.index) == list(b.index), "gene order must match"   # 程式邏輯應保證
    return a + b
```

| 用 `assert` | 不要用 `assert` |
| --- | --- |
| 「這個內部函式只會收到排序過的 list」 | 使用者輸入、外部檔案、API 回應 |
| 開發中確認中間結果的形狀（`assert X.shape[0] == len(y)`） | 正式環境必須執行的檢查 |
| 測試中的預期（`pytest` 的 `assert`） | 有副作用的運算式（`assert items.pop()`） |

> `python -O script.py` 會**移除所有 `assert`**。必須執行的檢查要用 `if ...: raise`。

## 例外階層速查

```
BaseException
├── KeyboardInterrupt, SystemExit       ← 不該被一般 except 攔下
└── Exception
    ├── ArithmeticError → ZeroDivisionError, OverflowError
    ├── LookupError → KeyError, IndexError
    ├── OSError → FileNotFoundError, PermissionError, TimeoutError
    ├── ValueError → UnicodeDecodeError
    ├── TypeError, AttributeError, NameError
    ├── RuntimeError → NotImplementedError, RecursionError
    └── AssertionError
```

捕捉父類別會一併捕捉所有子類別（`except LookupError` 同時接住 `KeyError` 與 `IndexError`）；多個 `except` 時把具體的放前面。
