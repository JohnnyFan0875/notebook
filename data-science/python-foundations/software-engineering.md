[Data Science](../README.md) › [Python Foundations](README.md) › 軟體工程實務

# 軟體工程實務 (Software Engineering for Data Work)

讓程式在幾個月後、或交給別人時仍然可讀、可改、可重跑。對分析工作而言，目標是**可讀性、可維護性、可測試性、可重現性**。

## 從 notebook 到可維護程式

```
探索 (notebook) → 抽出函式 → 搬進模組 (src/) → 加測試 → 加 CLI 入口 → 固定環境
```

| 訊號 | 該做的事 |
| --- | --- |
| 同一段 cell 複製到第二個 notebook | 抽成函式，放進 `src/` 模組 import |
| notebook 要「從頭依序執行」才會對 | 改成腳本，或至少 Restart & Run All 確認 |
| 參數寫死在程式中（路徑、門檻） | 移到 CLI 參數或設定檔，見 [腳本與 CLI](scripting-and-cli.md) |
| 換台電腦就跑不動 | 用 `pyproject.toml` + lock 檔固定環境，見 [Python 套件與環境](python-packages.md) |

建議的專案結構：

```
project/
├── pyproject.toml        # 依賴與工具設定
├── uv.lock               # 鎖定的確切版本
├── src/mypkg/            # 可重用的函式
├── scripts/              # 入口腳本（呼叫 src 的函式）
├── notebooks/            # 探索與圖表，import src 的函式
├── tests/
├── data/raw/             # 原始資料：唯讀，不進 git
└── results/              # 產出：可由程式完整重建
```

> 原始資料永遠不覆寫；所有中間檔與結果都應能由程式從 `data/raw/` 重建。大型資料與模型版本控管見 [DVC](../machine-learning/production/dvc.md)，流程化見 [工作流引擎](../../computing/workflow-engines/README.md)。

## 風格：PEP 8 與自動化工具

PEP 8 是共同的閱讀基準，交給工具處理，不要在 review 時靠人眼檢查。

| 工具 | 作用 | 指令 |
| --- | --- | --- |
| `ruff check` | linter：未使用的 import、未定義變數、常見 bug、PEP 8 | `uv run ruff check --fix .` |
| `ruff format` | formatter（相容 black） | `uv run ruff format .` |
| `mypy` / `pyright` | 依型別註記做靜態檢查 | `uv run mypy src` |
| `pre-commit` | commit 前自動跑上述工具 | `pre-commit install` |

`ruff` 一個工具取代了 flake8、isort、pycodestyle、black，速度也快得多。

```toml
# pyproject.toml
[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]   # pycodestyle、pyflakes、import 排序、bugbear、pyupgrade
```

## 命名

| 對象 | 慣例 | 例子 |
| --- | --- | --- |
| 變數、函式 | `snake_case`，函式用動詞 | `raw_counts`、`calculate_tpm()` |
| 類別 | `CamelCase` | `SampleSheet` |
| 常數 | `UPPER_SNAKE` | `MIN_READ_LENGTH = 30` |
| 內部使用 | 前綴 `_` | `_parse_header()` |
| 布林 | `is_` / `has_` | `is_paired_end` |

| 差 | 好 |
| --- | --- |
| `x`、`data2`、`tmp_final`、`df_new_new` | `raw_counts`、`filtered_counts`、`counts_cpm` |
| `do_stuff()` | `filter_low_expression()` |
| `thr` | `min_counts_per_sample` |

> 判斷標準：兩天後只看名字還想得起它的角色嗎？

## 註解與 docstring

註解解釋**為什麼**，程式碼本身說明**做什麼**。

```python
x = x + 1  # Increment x                    ← 差：重念程式

# The API returns duplicated rows for retried events, so dedupe by event_id first.
df = df.drop_duplicates("event_id")         # ← 好：說明外部限制
```

公開函式寫 docstring：做什麼、輸入輸出、前提與副作用。常見格式為 Google style 或 NumPy style（科學套件慣用）：

```python
def scale(values: np.ndarray) -> np.ndarray:
    """Scale values to the [0, 1] range.

    Parameters
    ----------
    values : np.ndarray
        Numeric array with at least one finite value.

    Returns
    -------
    np.ndarray
        Array of the same shape; NaN stays NaN.
    """
```

## 函式與重構

| 重構訊號 | 處理 |
| --- | --- |
| 函式同時讀檔、轉換、畫圖、寫檔 | 拆開：讀取 / 純轉換 / 輸出各自一個函式，純轉換最容易測試 |
| 同一規則出現在兩三處 | 抽成函式（DRY），否則改規則時只會改到一處 |
| 函式超過一個螢幕、巢狀超過 3 層 | 拆小、提早 `return` |
| 改一個地方牽動很多處 | 邊界不清楚，重新切分模組 |

> DRY (don't repeat yourself) 是避免**邏輯**重複，不是零重複。只出現兩次、且未來可能分開演變的程式，先別抽象；過早抽象只是把簡單的問題藏起來。

class 只在有狀態、資料與行為強關聯時才用；只是一組函式就放模組。設計細節見 [類別](class.md)。

## 可重現性 (Reproducibility)

| 面向 | 做法 |
| --- | --- |
| 環境 | `pyproject.toml` + `uv.lock`；記錄 Python 版本（`.python-version`） |
| 亂數 | `rng = np.random.default_rng(seed)` 傳入函式；ML 另外固定框架 seed |
| 參數 | 寫在設定檔或 CLI 參數，跟結果一起存檔 |
| 資料 | 原始資料唯讀；記錄來源版本（參考基因組版本、資料庫釋出日期） |
| 執行紀錄 | 用 `logging` 記錄參數、版本、輸入檔，見 [腳本與 CLI](scripting-and-cli.md) |
| 程式版本 | git commit；結果檔名或 metadata 帶 commit hash |

```python
import numpy as np

def subsample(x, n, rng: np.random.Generator):
    return rng.choice(x, size=n, replace=False)

rng = np.random.default_rng(20240315)       # 新 API；不要用全域的 np.random.seed()
subsample(np.arange(100), 5, rng)
```

## 測試保護重構

有測試才敢改。至少替最重要的轉換函式寫幾個單元測試，見 [測試](testing.md)。

## 提交前檢查

| 問題 | |
| --- | --- |
| 命名能獨立傳達角色嗎？ | |
| 有重複邏輯值得抽出嗎？ | |
| 註解在解釋「為什麼」嗎？公開函式有 docstring 嗎？ | |
| `ruff check` / `ruff format` 乾淨嗎？ | |
| 測試通過嗎？這次改動有沒有測試保護？ | |
| 結果能從原始資料重建嗎？ | |
