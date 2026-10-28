[Data Science](../README.md) › [Python Foundations](README.md) › 測試

# 測試 (Testing)

測試是一組可重複執行的檢查，用來盡早發現行為偏差。對分析腳本與管線，最大的價值是：重構或升級套件後，計算邏輯、篩選條件、檔案流程沒有被默默改壞。

## 測試的層級

| 層級 | 驗證什麼 | 例子 | 速度 |
| --- | --- | --- | --- |
| 單元測試 (unit test) | 單一函式 / 方法的規則 | `normalize_cpm()` 輸出總和為 1e6 | 毫秒 |
| 整合測試 (integration test) | 元件之間的邊界 | 讀寫檔案、資料庫、API | 秒 |
| 功能 / 端對端測試 (feature / end-to-end) | 使用者在乎的整段流程 | 小型 FASTQ 跑完整個 pipeline 產出預期表格 | 秒到分 |

先寫測試案例清單（輸入 → 預期輸出），至少涵蓋：

| 案例 | 例子 |
| --- | --- |
| 正常情況 | 一般輸入 |
| 邊界 | 只有 1 個元素、剛好等於門檻 |
| 空值 | 空 list、空 DataFrame、全是 NaN 的欄 |
| 錯誤輸入 | 應該丟出 `ValueError` 的值 |
| 已知 bug | 修過的 bug 補一個測試，避免回歸 (regression) |

## pytest 基本用法

```python
# src/mypkg/stats.py
def cpm(counts: list[int]) -> list[float]:
    total = sum(counts)
    if total == 0:
        raise ValueError("library size is zero")
    return [c / total * 1e6 for c in counts]
```

```python
# tests/test_stats.py
import pytest
from mypkg.stats import cpm

def test_cpm_sums_to_one_million():
    assert sum(cpm([10, 30, 60])) == pytest.approx(1e6)   # 浮點數比較用 approx

def test_cpm_single_gene():
    assert cpm([5]) == [1e6]

def test_cpm_zero_library_raises():
    with pytest.raises(ValueError, match="library size"):  # 驗證會丟出指定例外
        cpm([0, 0])

@pytest.mark.parametrize(                                  # 一個測試跑多組輸入
    ("counts", "expected"),
    [([1, 1], [5e5, 5e5]), ([1, 3], [2.5e5, 7.5e5])],
)
def test_cpm_values(counts, expected):
    assert cpm(counts) == pytest.approx(expected)
```

pytest 會自動收集 `test_*.py` 檔裡的 `test_*` 函式；直接用 `assert`，失敗時會顯示兩邊的值。

```bash
uv add --dev pytest pytest-cov     # 加入開發依賴（見 Python 套件與環境）
uv run pytest                      # 全部
uv run pytest tests/test_stats.py  # 單一檔案
uv run pytest -k cpm               # 名稱含 cpm 的測試
uv run pytest -x                   # 第一個失敗就停
uv run pytest --lf                 # 只重跑上次失敗的
uv run pytest --cov=mypkg          # 覆蓋率報告
```

專案結構與 `pyproject.toml` 設定見 [Python 套件與環境](python-packages.md)；`assert` 與例外的差別見 [錯誤處理與斷言](errors-and-assertions.md#assert檢查內部假設)。

## 測試資料科學程式

| 要比較的 | 用 | 原因 |
| --- | --- | --- |
| 浮點數 | `pytest.approx(x, rel=1e-6)` | `0.1 + 0.2 != 0.3` |
| NumPy array | `np.testing.assert_allclose(a, b)` | 逐元素容差比較，失敗訊息指出哪個元素 |
| DataFrame / Series | `pd.testing.assert_frame_equal(a, b)` | 一併檢查 dtype、index、欄位順序 |
| 隨機結果 | 固定 `np.random.default_rng(seed)` | 結果可重現 |

```python
import numpy as np
import pandas as pd

def filter_by_manufacturer(df, name):
    return df[df["Manufacturer"] == name]

def test_filter_returns_only_requested_brand():
    df = pd.DataFrame({"Manufacturer": ["Apple", "Dell", "Apple"], "price": [1, 2, 3]})
    out = filter_by_manufacturer(df, "Apple")
    expected = pd.DataFrame({"Manufacturer": ["Apple", "Apple"], "price": [1, 3]}, index=[0, 2])
    pd.testing.assert_frame_equal(out, expected)          # index 也要一致

def test_bootstrap_is_reproducible():
    a = bootstrap_mean(np.arange(10), rng=np.random.default_rng(0))
    b = bootstrap_mean(np.arange(10), rng=np.random.default_rng(0))
    np.testing.assert_allclose(a, b)
```

> 讓函式**接收** `rng` 參數（而不是在函式裡呼叫全域 `np.random.seed`），測試與平行運算時才能控制亂數。

| 值得測的地方 | 例子 |
| --- | --- |
| 資料轉換的不變量 | 正規化後總和、篩選後沒有不該出現的值、merge 後列數沒有暴增 |
| 解析器 | 檔名 regex、自訂格式讀取 |
| 邊界條件 | 全零計數、單一樣本、缺值 |
| 小型黃金資料 (golden file) | 一個極小的輸入檔 + 已人工確認的輸出 |

## Fixture：共用的前置與清理

```python
import pytest

@pytest.fixture
def counts_df():
    return pd.DataFrame({"gene": ["A", "B"], "s1": [10, 0], "s2": [5, 5]})

def test_drop_zero_rows(counts_df):           # 參數名 = fixture 名，pytest 自動注入
    assert len(drop_zero(counts_df)) == 2

@pytest.fixture
def sample_sheet(tmp_path):                   # tmp_path：pytest 內建，每個測試一個暫存資料夾
    path = tmp_path / "samples.csv"
    path.write_text("sample_id,condition\nS1,ctrl\nS2,treat\n")
    yield path                                # yield 前是 setup，後是 cleanup
    # tmp_path 會自動清理，這裡通常不用寫

def test_read_sheet(sample_sheet):
    assert read_sheet(sample_sheet).shape == (2, 2)

def test_uses_env(monkeypatch):               # monkeypatch：暫時改環境變數、屬性
    monkeypatch.setenv("DATA_DIR", "/tmp/x")
    assert get_data_dir() == "/tmp/x"
```

| 內建 fixture | 用途 |
| --- | --- |
| `tmp_path` | 暫存資料夾（`pathlib.Path`），不污染專案目錄 |
| `monkeypatch` | 替換環境變數、函式、屬性（例如把 API 呼叫換成假資料） |
| `capsys` | 擷取 `print` 輸出 |
| `caplog` | 擷取 logging 訊息 |

多個測試檔共用的 fixture 放在 `tests/conftest.py`，pytest 會自動載入；`@pytest.fixture(scope="session")` 讓昂貴的 setup（載入參考基因組索引）整個測試只做一次。

## Marker：跳過與預期失敗

```python
import sys

@pytest.mark.skip(reason="not implemented yet")
def test_future(): ...

@pytest.mark.skipif(sys.platform == "win32", reason="needs samtools")
def test_bam_index(): ...

@pytest.mark.xfail(reason="known bug #42")    # 預期失敗；若意外通過會標示 XPASS
def test_known_bug(): ...

@pytest.mark.slow                             # 自訂 marker，需在 pyproject 註冊
def test_full_pipeline(): ...
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
markers = ["slow: long-running tests"]
```

`uv run pytest -m "not slow"` 日常只跑快的；CI 再跑全部。

## unittest：內建框架

標準庫內建、不需安裝，OOP 風格，常見於舊專案。pytest 也能直接執行 `unittest` 寫的測試。

| pytest | unittest |
| --- | --- |
| `assert a == b` | `self.assertEqual(a, b)` |
| `assert x` | `self.assertTrue(x)` |
| `with pytest.raises(E):` | `with self.assertRaises(E):` |
| fixture | `setUp()` / `tearDown()`（每個測試方法前後執行） |
| `pytest -k name` | `python -m unittest -k name` |

```python
import unittest

class TestSquared(unittest.TestCase):
    def setUp(self):
        self.values = [1, 2, 3]

    def test_square_of_negative(self):
        self.assertEqual((-3) ** 2, 9)

    def test_contains(self):
        self.assertIn(2, self.values)

if __name__ == "__main__":
    unittest.main()           # python -m unittest -v
```

## 實務取捨

| 情境 | 建議 |
| --- | --- |
| 個人分析腳本 | 先把核心邏輯抽成函式，替最容易錯的 2–3 個寫單元測試 |
| 牽涉檔案、資料庫、API | 補整合測試；外部服務用 `monkeypatch` 或假資料替代 |
| 共用的套件 / pipeline | 加 CI（GitHub Actions）每次 push 自動跑，見 [DevOps](../../computing/devops/devops-fundamentals.md) |
| 覆蓋率 | 不追求數字，先保護最難人工回歸檢查的部分 |
