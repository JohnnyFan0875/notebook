# Python Testing

測試的目的不是證明程式永遠正確，而是用一組可重複執行的檢查，盡早發現行為偏差。對資料分析或資料工程腳本來說，最常見的價值是避免重構後默默改壞計算邏輯、資料篩選條件或檔案流程。

## 測試在檢查什麼

- `unit test`：驗證單一函式、方法或類別的行為。
- `integration test`：驗證多個元件之間的協作，例如 Python 與檔案系統、資料庫、API。
- `feature test`：從使用者或業務功能角度驗證整段流程。

一個實用的心智模型是：

- `unit test` 看局部規則有沒有壞。
- `integration test` 看邊界有沒有接好。
- `feature test` 看整個使用情境是否成立。

## 測試案例怎麼想

寫測試前，先列出 `test case`，也就是「輸入」與「預期輸出」。

至少先覆蓋這幾類情境：

- 正常情況
- 邊界情況
- 空值或空集合
- 異常輸入
- 重構後最怕壞掉的情況

```python
def sum_of_arr(values: list[int]) -> int:
    return sum(values)


def test_sum_regular_values():
    assert sum_of_arr([1, 2, 3]) == 6
    assert sum_of_arr([100, 150]) == 250


def test_sum_empty_list():
    assert sum_of_arr([]) == 0


def test_sum_single_value():
    assert sum_of_arr([10]) == 10
```

這類測試的重點不是語法，而是把需求拆成可驗證的案例。

## `pytest` 的基本寫法

`pytest` 是 Python 常見的測試工具，適合用函式風格快速寫測試。

```python
def is_even(n: int) -> bool:
    return n % 2 == 0


def test_is_even():
    assert is_even(4) is True
    assert is_even(5) is False
```

常見執行方式：

```bash
pytest
pytest tests/test_math.py
pytest -k even
```

如果你只是想理解 `assert` 本身的用途，可搭配 [assert.md](assert.md) 一起看。

## Feature Test 的直覺

當單一函式都正確時，整體流程還是可能出錯。這時要寫的是功能層級測試。

```python
import pandas as pd


def filter_data_by_manuf(df: pd.DataFrame, manufacturer_name: str) -> pd.DataFrame:
    return df[df["Manufacturer"] == manufacturer_name]


def test_filter_data_by_manuf_returns_only_requested_brand():
    df = pd.DataFrame(
        {"Manufacturer": ["Apple", "Dell", "Apple"]}
    )

    filtered = filter_data_by_manuf(df, "Apple")

    assert filtered["Manufacturer"].nunique() == 1
    assert list(filtered["Manufacturer"].unique()) == ["Apple"]
```

這種測試不是只檢查某行程式，而是檢查一個使用者真的在乎的功能行為。

## Fixtures

`fixture` 是為測試準備環境的機制。當很多測試都需要相同前置資料、檔案、連線或假資料時，fixture 能把 setup / cleanup 集中管理。

```python
import os
import pytest


@pytest.fixture
def temp_file():
    path = "test_file.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write("Test data")

    yield path

    os.remove(path)


def test_temp_file_exists(temp_file):
    assert os.path.exists(temp_file)
```

這裡的 `yield` 前面是 setup，後面是 cleanup。這比把建立與刪除檔案散落在每個測試裡更容易維護。

## `pytest` Markers

marker 讓你替特定測試加上額外行為。

### Skip

無條件跳過：

```python
import pytest


@pytest.mark.skip
def test_not_ready_yet():
    assert 1 == 1
```

### Skipif

條件成立時跳過：

```python
import sys
import pytest


@pytest.mark.skipif(sys.platform == "win32", reason="Linux only")
def test_linux_only_behavior():
    assert True
```

### Xfail

預期目前會失敗，但暫時保留：

```python
import pytest


@pytest.mark.xfail(reason="Known bug not fixed yet")
def test_known_bug():
    assert False
```

實務上：

- `skip` 適合環境不支援或功能尚未啟用。
- `skipif` 適合依作業系統、Python 版本或外部條件控制。
- `xfail` 適合已知缺陷，避免團隊把它誤判成新回歸問題。

## Integration Test 的例子

當你要確認「程式 + 外部系統」一起運作是否正確，可以寫整合測試。

```python
import os
import pytest


@pytest.fixture
def setup_file():
    path = "test_file.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write("Test data 1")
    yield path
    os.remove(path)


def test_file_is_created(setup_file):
    assert os.path.exists(setup_file)
```

這裡驗證的不是字串運算，而是 Python 與檔案系統的整合。

## `unittest` 的位置

`unittest` 是 Python 內建測試框架，不需要另外安裝。它採用較明顯的 OOP 風格，常見於舊專案或標準函式庫風格程式碼。

```python
import unittest


class TestSquared(unittest.TestCase):
    def test_square_of_negative_number(self):
        self.assertEqual((-3) ** 2, 9)


if __name__ == "__main__":
    unittest.main()
```

常見 assertion method：

- `self.assertEqual(a, b)`
- `self.assertNotEqual(a, b)`
- `self.assertTrue(expr)`
- `self.assertFalse(expr)`
- `self.assertRaises(SomeError)`

執行方式：

```bash
python -m unittest
python -m unittest test_example.py
python -m unittest -k Square
python -m unittest -f
python -m unittest -v
```

## `unittest` 裡的 Fixture

如果你在 `unittest` 中要做測試前後的準備與清理，通常用 `setUp()` 和 `tearDown()`。

```python
import unittest


class TestMembership(unittest.TestCase):
    def setUp(self):
        self.values = [1, 2, 3]

    def tearDown(self):
        self.values.clear()

    def test_contains_existing_value(self):
        self.assertTrue(2 in self.values)
```

`setUp()` 會在每個測試方法執行前呼叫，`tearDown()` 會在每個測試方法後呼叫。

## 實務上的取捨

- 小型資料腳本：先從 `pytest` + 幾個核心 `unit test` 開始。
- 牽涉檔案、資料庫或 API：補 `integration test`。
- 有明確業務流程：再補 `feature test`。
- 不要一開始追求覆蓋率數字，先保護最容易壞、最難人工回歸的部分。

## Summary

- 測試是在建立可重複驗證的安全網。
- `pytest` 適合快速撰寫函式風格測試。
- fixture 解決重複 setup / cleanup。
- marker 讓你管理 skip、條件跳過與預期失敗。
- `unittest` 是內建框架，常見於既有專案。
