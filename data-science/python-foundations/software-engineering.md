# Python: Software Engineering Principles

寫 Python 不只是「讓它能跑」，而是讓它在幾週後、幾個月後，甚至交給別人維護時仍然可讀、可改、可測。

這篇筆記整理的不是框架細節，而是偏長期維護的基本原則。

## What This Usually Optimizes For

軟體工程實務通常在優化幾件事：

- readability
- maintainability
- testability
- change safety

如果一段程式只有原作者看得懂，那它通常還不算真的完成。

## PEP 8 Is a Shared Baseline

PEP 8 是 Python 最常見的程式風格指南。它的價值不是「形式正確」，而是降低閱讀摩擦。

常見例子：

- import 放在檔案頂部
- comment 後面保留空格
- 命名使用一致風格
- 留白與縮排保持規律

```python
# Import needed package
import numpy as np


def normalize(values):
    return np.array(values) / np.sum(values)
```

風格一致的收益通常不是單一檔案，而是整個 codebase 的可掃描性。

## Use Style Tools to Catch Low-Value Mistakes

像 `pycodestyle` 這類工具適合抓「不值得靠人眼反覆檢查」的問題。

```bash
pip install pycodestyle
pycodestyle my_script.py
```

這類工具很適合處理：

- block comment 格式
- import 位置
- 空白與縮排
- 明顯的 PEP 8 違規

它們不能取代設計判斷，但能降低 review 時的低訊號雜音。

## Good Comments Explain Why, Not What

壞註解常常只是把程式碼再念一次。

```python
# Bad
x = x + 1  # Increment x
```

比較有價值的註解通常會說明：

- 為什麼要這樣做
- 這段邏輯在保護什麼 invariant
- 哪個外部限制逼得你這樣寫

```python
# API returns duplicated rows for retried events, so dedupe by event_id first.
df = df.drop_duplicates("event_id")
```

如果程式碼本身就能清楚表達「做什麼」，註解應該優先補足「為什麼」。

## Docstrings Are for Interface-Level Understanding

當函式、類別或模組需要被重用時，docstring 很重要。

```python
def scale(values):
    """Scale numeric values to the 0-1 range.

    Assumes the input contains at least one non-null numeric value.
    """
```

好 docstring 通常會回答：

- 這個東西做什麼
- 輸入與輸出是什麼
- 有沒有重要前提或副作用

如果一段邏輯只靠看實作才能知道怎麼用，重用成本通常會很高。

## Descriptive Naming Beats Clever Naming

命名是一種壓縮過的設計文件。

差的命名：

- `x`
- `data2`
- `tmp_final`
- `do_stuff()`

比較好的命名：

- `raw_events`
- `normalized_prices`
- `daily_sales_summary`
- `calculate_retention_rate()`

一個快速判斷方式是：如果變數名在兩天後已經不能幫你回想它的角色，那多半太弱了。

## Refactor When Structure Fights Change

refactor 不只是「把程式寫漂亮」，而是降低下一次修改的成本與風險。

常見 refactor 訊號：

- 命名太模糊
- 同樣邏輯重複出現
- 函式過長
- 一個函式同時做資料讀取、轉換、輸出、紀錄
- 小改動會牽動很多地方

好的重構通常讓程式更接近：

- 每個函式只負責一件清楚的事
- 重複邏輯被收斂
- 邊界更容易測試

## DRY Means Avoid Repeated Logic, Not Zero Repetition at Any Cost

DRY, don't repeat yourself，真正要避免的是知識重複與邏輯重複。

如果你在兩三個地方都手寫同一段計算規則，未來很容易只改到其中一處。

```python
def tokenize(text):
    ...


class Document:
    def __init__(self, text):
        self.text = text
        self.tokens = tokenize(text)
```

把共同邏輯抽成函式、方法或共用元件，通常會比複製貼上更安全。

但也不要為了「完全不重複」而過度抽象。抽象太早，往往只是把簡單問題藏起來。

## Make Classes Earn Their Keep

class 最適合處理：

- 有狀態的物件
- 一組強關聯資料與行為
- 明確的抽象邊界

如果只是把幾個函式硬包進 class，不一定比較工程化。更多 OOP 設計細節可參考 [class.md](class.md)。

## Tests Protect Refactoring

良好的測試不是為了「好看」，而是讓你敢改。

至少要能回答：

- 這次改動會不會破壞原有行為
- 需求最重要的情境是否還成立
- 重構後哪裡可能偷偷壞掉

`pytest` 是很常見的起點：

```python
def test_tokenize_empty_string():
    assert tokenize("") == []
```

常見執行方式：

```bash
pytest
pytest tests/test_document.py
```

更完整的測試整理可參考 [testing.md](testing.md)。

## Keep Code Review-Friendly

從協作角度看，可維護程式通常有這些特徵：

- 單一檔案責任清楚
- 變數名能快速看出角色
- 註解不與程式碼打架
- 沒有大量低價值風格噪音
- 測試能說明關鍵行為

review 的目的不只是抓 bug，也是讓團隊更快理解變更。

## Practical Checklist

每次準備提交前，可以快速問自己：

- 這段程式是否比原本更容易讀
- 命名是否能獨立傳達角色
- 是否有重複邏輯值得抽出
- 註解是在解釋為什麼，而不是重念程式
- 是否應補 docstring
- 有沒有基本測試保護這次重構
- PEP 8 與 style 工具是否能乾淨通過

## Takeaways

- 風格一致不是形式主義，而是降低理解成本。
- 好命名、好註解、好 docstring 都是在幫未來的維護者。
- DRY 的目標是減少邏輯分叉，不是追求炫技抽象。
- 測試的最大價值，是讓重構更安全。
- 工程品質通常來自很多小而穩定的習慣，而不是單一大技巧。
