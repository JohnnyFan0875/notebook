# Python: Local Packages and Structure

當 Python 腳本開始從「單一檔案」長成一組可重用模組時，就該開始用 package 的角度思考專案結構。

這篇筆記聚焦的是本地 package 的基本組成、`__init__.py` 的角色，以及讓 package 可安裝、可攜帶的最低限度觀念。

## When a Script Wants to Become a Package

通常有幾個訊號：

- 多個檔案開始共用同一批 helper functions
- 你想把某些類別或函式集中暴露給別人 import
- 相對路徑與複製貼上越來越難維護
- 專案需要定義依賴套件與安裝方式

這時與其繼續堆一堆零散 `.py` 檔，不如把它整理成 package。

## Minimal Package Shape

最小結構通常像這樣：

```text
my_package/
    __init__.py
    utils.py
```

這樣之後就可以：

```python
import my_package
import my_package.utils
```

`__init__.py` 的存在表示這個資料夾是 package 邊界的一部分。

## `__init__.py` Controls the Public Surface

假設你有：

```python
# my_package/utils.py
def we_need_to_talk(break_up=False):
    ...
```

那你可以直接從 submodule import：

```python
import my_package.utils
my_package.utils.we_need_to_talk(break_up=True)
```

也可以在 `__init__.py` 重新暴露常用 API：

```python
from .utils import we_need_to_talk
```

這樣使用者就可以：

```python
import my_package
my_package.we_need_to_talk(break_up=False)
```

這個技巧的重點不是偷懶，而是讓 package 對外暴露的入口更穩定。

## Packages Can Expose Classes Too

例如：

```python
# my_package/my_class.py
class MyClass:
    def __init__(self, value):
        self.value = value
```

再在 `__init__.py` 中寫：

```python
from .my_class import MyClass
```

之後外部可以直接：

```python
import my_package

obj = my_package.MyClass("hello")
print(obj.value)
```

對使用者來說，這比要求他知道所有內部檔案路徑更乾淨。

## As the Package Grows, Add Submodules Deliberately

當功能變多時，可以把 package 擴成多個模組：

```text
my_package/
    __init__.py
    utils.py
    io.py
    models.py
```

切分原則通常是：

- 依責任分組
- 依穩定邊界分組
- 避免單一模組同時處理資料讀寫、模型邏輯、CLI、設定

好的 package 結構應該讓使用者大致猜得到功能會在哪裡。

## Favor Relative Imports Inside the Package

在 package 內部，常見寫法是：

```python
from .utils import normalize
from .models import ForecastModel
```

這比硬寫整條絕對專案路徑更容易搬動與重構。

## A Package Should Be Portable

所謂 portable，通常表示：

- 不依賴你本機的特殊工作目錄
- 依賴套件有明確宣告
- 安裝後能從其他位置 import

如果某個 package 只能在作者自己的資料夾結構下正常 import，通常代表結構還不夠穩。

## Declare Dependencies Explicitly

至少要把需要的外部套件版本寫清楚。

概念上常見會有：

```text
pycodestyle>=2.4.0
```

重點不是這個特定套件，而是：

- 不要讓依賴隱性存在
- 團隊與部署環境要能重建同一組執行條件

### `install_requires` vs `requirements.txt`

這兩者很容易混在一起，但用途不完全相同。

- `install_requires`: 給「使用你的 package 的人」
- `requirements.txt`: 常用來固定某個開發或部署環境

實務上可以這樣想：

- package 的最小必要依賴，寫在 packaging metadata
- 開發用工具，例如 `pytest`、`tox`、`black`、`sphinx`，常另外放在 `requirements_dev.txt` 或其他 dev requirements 檔

如果你把所有開發工具都塞進 `install_requires`，使用者會被迫安裝一堆其實不需要的東西。

## Basic Packaging Metadata

較傳統的 Python package 會用 `setup.py` 描述 package。

```python
from setuptools import setup

setup(
    name="my_package",
    version="0.0.1",
    description="Example package",
    packages=["my_package"],
    install_requires=[
        "pycodestyle>=2.4.0",
    ],
)
```

這裡最重要的觀念是：

- package 有名稱與版本
- 需要宣告包含哪些 packages
- 需要宣告依賴

今天很多專案也會改用 `pyproject.toml`，但底層觀念仍然相同。

### Version Constraints Need Deliberate Tradeoffs

依賴版本限制太寬，可能讓未測過的新版本破壞你的 package。限制太窄，則會提高安裝衝突機率。

所以原則通常是：

- 不要無限制地接受所有未來版本
- 也不要把版本鎖得比實際需要更死
- 用測試來支撐你聲稱支援的版本範圍

對 Python 本身的支援版本也是同樣思路。

## Installing the Package

安裝後，package 才能以較一致的方式被 import 與重用。

```bash
pip install .
```

安裝成功後，通常就不必依賴「剛好站在某個資料夾裡」才能 import。

對本地開發來說，也很常搭配 editable install：

```bash
pip install -e .
```

這讓你修改原始碼後，不必每次重新安裝整個 package。

## Supporting Files Matter

成熟一點的 package 通常不只是一個 package 目錄和 `setup.py`。

常見還會有：

```text
README.md
LICENSE
MANIFEST.in
requirements_dev.txt
tox.ini
docs/
tests/
```

這些檔案分別在處理不同責任：

- README: 對外說明
- LICENSE: 法律授權
- MANIFEST: 分發時要額外帶上的檔案
- dev requirements: 開發環境工具
- tox: 多版本測試
- docs: 補正式文件
- tests: 驗證行為

## README and License Are Part of the Package Experience

README 不只是「附加說明」，而是很多使用者第一次接觸 package 的入口。

通常至少要回答：

- 這個 package 做什麼
- 怎麼安裝
- 最小使用範例
- 依賴與支援版本
- 哪裡看更完整文件

LICENSE 則是在說明別人能怎麼合法使用、修改、散布你的 package。

如果要公開發佈，這兩者通常都不應省略。

## `MANIFEST.in` Handles Extra Files in Distributions

不是所有你希望一起發佈的檔案，都會自動被包含在 distribution 中。

`MANIFEST.in` 常用來顯式加入額外檔案，例如：

```text
include README.md
include LICENSE
```

這在 source distribution 特別重要，因為你可能希望：

- README 被一起帶上
- LICENSE 被一起帶上
- 範例資料、模板或設定檔被一起帶上

心智模型是：package code 之外，分發還需要哪些 supporting files。

## Test the Package Like an Installed Artifact

package 測試不只是跑函式，也是在驗證：

- 安裝後能不能正常 import
- package metadata 與依賴是否正確
- 不同 Python 版本下是否仍可運作

`pytest` 是常見的測試入口，而 package 專案通常會有獨立 `tests/` 目錄：

```bash
pytest
```

如果你需要跨多個 Python 版本驗證，`tox` 是很常見的工具。

```text
[tox]
envlist = py310, py311, py312

[testenv]
deps = pytest
commands = pytest
```

`tox` 的價值在於：

- 自動建立隔離環境
- 用多個 Python 版本執行同一批測試
- 幫你驗證你聲稱支援的版本範圍是否真的成立

## Versioning Is Part of Communication

版本號不只是給機器看的，也是給使用者看的變更承諾。

常見形式：

```text
MAJOR.MINOR.PATCH
```

簡化理解：

- MAJOR: 可能有破壞性改動
- MINOR: 向下相容的新功能
- PATCH: 向下相容的修正

很多專案也會在 package 內暴露版本資訊：

```python
__version__ = "0.1.0"
```

這樣可以讓使用者或除錯流程快速確認當前安裝版本。

## Keep a Changelog / History

當 package 開始演進時，只改版本號通常不夠。

一份簡單 changelog 很有幫助，因為它能回答：

- 這版加了什麼
- 哪些 API 被移除或改名
- 哪些 Python 版本即將停止支援

這對使用者升級判斷很重要，也會讓維護者少很多重複解釋。

## Classifiers and Metadata Improve Discoverability

除了名稱和版本之外，package metadata 還可以描述：

- 支援哪些 Python 版本
- 授權類型
- 主題分類
- 專案成熟度

這些資訊通常會出現在 `classifiers` 中。它們不是核心執行邏輯，但會影響 package 在 PyPI 上的可理解性與可搜尋性。

## Build Distribution Artifacts Explicitly

安裝中的 package 和準備發佈的 distribution artifact 不是同一件事。

常見有兩種：

- source distribution, `sdist`
- wheel distribution, `bdist_wheel`

傳統 `setup.py` 流程常見命令：

```bash
python setup.py sdist bdist_wheel
```

心智模型：

- `sdist` 比較接近原始碼包
- `wheel` 是較適合安裝的建置產物

發佈前最好真的看一下 `dist/` 內出來了什麼，而不是假設所有需要的檔案都已包含。

## Publish with Care

如果要上傳 distribution，常見做法是用 `twine`。

```bash
twine upload dist/*
twine upload -r testpypi dist/*
```

實務上通常先上 `TestPyPI` 比較安全，因為：

- 可以先驗證安裝流程
- 可以先檢查 README render 與 metadata
- 可以避免正式 PyPI 留下壞版本紀錄

## Automate Repetitive Release Tasks

當 package 進入穩定維護期後，建置、測試、清理、發佈這些步驟很適合自動化。

常見方式像是：

- `Makefile`
- shell scripts
- CI workflows

例如你可能會把下列步驟固定化：

- `clean-build`
- `pytest`
- `tox`
- `sdist` / `bdist_wheel`
- `twine upload`

這樣做的重點不是炫技，而是降低手動漏步驟的風險。

## Package Design and API Surface

一個 package 不只是檔案集合，它也有對外 API。

思考方式可以是：

- 使用者最常 import 什麼
- 哪些函式或類別應該從 `__init__.py` 暴露
- 哪些內部 helper 不該成為公開承諾

如果內部結構一直變，但對外 import 路徑很穩，使用者成本就低很多。

## Practical Checklist

開始整理 package 時，可以快速檢查：

- 是否已有清楚的 package 目錄
- 是否存在 `__init__.py`
- 是否把常用 API 從 submodule 提升到 package 層
- 內部 import 是否可攜
- dependencies 是否明確宣告
- 是否能用 `pip install .` 或 `pip install -e .` 安裝
- 是否區分 runtime dependencies 與 dev dependencies
- 是否有 README、LICENSE、必要時的 `MANIFEST.in`
- 是否有測試與多版本測試策略
- 發佈前是否檢查 `dist/` 產物與版本號

## Takeaways

- package 是重用與維護邊界，不只是資料夾。
- `__init__.py` 可以幫你整理對外 API。
- package 結構應該反映責任分工，而不是作者當下的臨時方便。
- 可攜與可安裝，通常比「在我電腦上可用」更重要。
- packaging 不只包含程式碼，也包含 README、LICENSE、測試、版本與發佈流程。
