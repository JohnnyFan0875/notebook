[Data Science](../README.md) › [Python Foundations](README.md) › Python 套件與環境

# Python 套件與環境 (Packaging & Environments with uv)

腳本長成一組會被重複 import 的模組時，就該整理成套件 (package)：依賴明確宣告、可安裝、換台電腦能重建同樣的環境。現代做法是 **`pyproject.toml` + `uv`**；舊式的 `setup.py`、`requirements.txt`、`MANIFEST.in` 只在維護舊專案時需要。conda 與容器見 [Containers and Environments](../../computing/containers-and-env/README.md)。

## 工具選擇

| 需求 | 工具 | 備註 |
| --- | --- | --- |
| 純 Python 專案（多數分析與套件） | **uv** | 管理 Python 版本、虛擬環境、依賴、lock、build、publish；比 pip 快很多 |
| 需要非 Python 的生資工具（samtools、STAR、R） | [conda / mamba / pixi](../../computing/containers-and-env/conda.md) | bioconda channel；可在 conda 環境內再用 uv |
| 跨機器、HPC、發表時完整封裝 | [Docker / Apptainer](../../computing/containers-and-env/README.md) | 連 OS 層一起固定 |

| 舊做法 | uv 對應 |
| --- | --- |
| `python -m venv .venv` + `pip install ...` | `uv venv` / `uv add ...`（自動建 `.venv`） |
| `requirements.txt` | `pyproject.toml`（宣告）+ `uv.lock`（鎖定） |
| `requirements_dev.txt` | `[dependency-groups] dev`（`uv add --dev`） |
| `pip install -e .` | `uv sync`（專案本身預設以 editable 安裝） |
| `setup.py` / `setup.cfg` | `pyproject.toml` 的 `[project]` 表 |
| `python setup.py sdist bdist_wheel` | `uv build` |
| `twine upload dist/*` | `uv publish` |
| `pyenv install 3.12` | `uv python install 3.12` |
| `tox`（多版本測試） | `uv run --python 3.12 pytest`（或 `nox` / `tox` 搭 uv） |

## 建立專案

```bash
uv init --package mypkg          # 可安裝的套件（src layout）；只是分析專案用 uv init
cd mypkg
uv add numpy pandas "scipy>=1.13"  # 執行期依賴 → 寫進 pyproject.toml 並更新 uv.lock
uv add --dev pytest ruff         # 開發工具 → dependency-groups，使用者安裝時不會裝
uv run pytest                    # 在專案環境中執行（自動同步環境）
uv run mypkg                     # 執行 [project.scripts] 定義的指令
uv sync                          # 依 uv.lock 重建環境（clone 後第一件事）
uv lock --upgrade-package pandas # 只升級某個套件
uv tree                          # 依賴樹
```

`uv init --package` 產生的結構：

```
mypkg/
├── .python-version              # 專案使用的 Python 版本
├── pyproject.toml
├── README.md
└── src/mypkg/__init__.py
```

加入程式與測試後：

```
mypkg/
├── pyproject.toml
├── uv.lock                      # 進 git：鎖定所有套件的確切版本與 hash
├── src/mypkg/
│   ├── __init__.py              # 對外 API
│   ├── io.py                    # 讀寫
│   ├── normalize.py             # 純轉換
│   └── cli.py                   # 命令列入口
└── tests/
    └── test_normalize.py
```

> 用 **src layout**（程式放 `src/mypkg/`）：測試一定是對「安裝後的套件」跑，不會因為剛好站在專案根目錄而 import 成功、裝到別處卻失敗。

## `pyproject.toml`

```toml
[project]
name = "mypkg"
version = "0.1.0"
description = "RNA-seq count utilities"
readme = "README.md"
requires-python = ">=3.11"
license = "MIT"
dependencies = [                 # 使用者需要的最小依賴：給下限，不要鎖死
    "numpy>=1.26",
    "pandas>=2.1",
]

[project.optional-dependencies]  # 使用者可選：pip install "mypkg[plot]"
plot = ["matplotlib>=3.8"]

[project.scripts]                # 安裝後產生的命令列指令
mypkg = "mypkg.cli:main"

[dependency-groups]              # 只給開發者，不會發佈出去
dev = ["pytest>=8", "ruff>=0.5"]

[build-system]
requires = ["uv_build>=0.12,<0.13"]   # uv init 自動產生；也可用 hatchling、setuptools
build-backend = "uv_build"

[tool.pytest.ini_options]        # 各工具的設定也集中在這裡
testpaths = ["tests"]
```

| 放哪裡 | 給誰 | 版本寫法 |
| --- | --- | --- |
| `dependencies` | 所有使用者 | 寬鬆下限（`>=`），避免和使用者其他套件衝突 |
| `optional-dependencies` | 選用功能的使用者 | 同上 |
| `dependency-groups.dev` | 開發者 | 隨意 |
| `uv.lock` | 重現**這個**環境（分析專案、部署） | 自動產生的確切版本，不手改 |

> 套件：`pyproject.toml` 給範圍、讓使用者能裝。分析專案：靠 `uv.lock` 精確重現結果，論文附上 lock 檔與 commit。需要給其他工具時 `uv export --format requirements-txt > requirements.txt`。

## `__init__.py` 與 import

`__init__.py` 定義套件的對外 API：使用者 import 的路徑穩定，內部檔案怎麼重構都不影響。

```python
# src/mypkg/__init__.py
from .normalize import cpm, tpm          # 套件內部用相對 import
from .io import read_counts

__all__ = ["cpm", "tpm", "read_counts"]  # from mypkg import * 時匯出的名稱
```

```python
import mypkg
mypkg.cpm(counts)                        # 不需要知道它在 normalize.py 裡
from mypkg.normalize import cpm          # 也可以直接從子模組 import

from importlib.metadata import version
version("mypkg")                         # '0.1.0'：從安裝的 metadata 讀版本，不必手寫 __version__
```

| 原則 | 說明 |
| --- | --- |
| 依責任切模組 | `io`、`normalize`、`plot`、`cli`；讓人猜得到功能在哪 |
| 只暴露穩定的 API | 內部 helper 加 `_` 前綴，不放進 `__init__.py` |
| 不依賴工作目錄 | 讀套件內附資料用 `importlib.resources.files("mypkg") / "data/ref.tsv"`，不用相對路徑 |
| 不在 import 時做重活 | 讀大檔、連網路放進函式裡，不要寫在模組頂層 |

## 建置與發佈

```bash
uv version --bump minor          # 0.1.0 → 0.2.0（語意化版本）
uv build                         # → dist/mypkg-0.2.0.tar.gz（sdist）與 .whl（wheel）
uv publish --index testpypi      # 先上 TestPyPI 驗證（需在 pyproject 設定 [[tool.uv.index]]）
uv publish                       # 正式 PyPI（token 放環境變數 UV_PUBLISH_TOKEN）
```

| 產物 | 內容 | 用途 |
| --- | --- | --- |
| sdist (`.tar.gz`) | 原始碼 | 讓下游自行建置 |
| wheel (`.whl`) | 建置好的安裝檔 | 安裝快，`pip` / `uv` 優先使用 |

語意化版本 (semantic versioning) `MAJOR.MINOR.PATCH`：

| 位數 | 何時加 |
| --- | --- |
| MAJOR | 不相容的 API 變更 |
| MINOR | 向下相容的新功能 |
| PATCH | 向下相容的 bug 修正 |

發佈前確認：`dist/` 裡真的包含需要的檔案（解開 wheel 看）、README 在 TestPyPI 正確顯示、在乾淨環境 `uv run --with dist/*.whl python -c "import mypkg"` 能 import。另外維護一份 `CHANGELOG.md` 說明每版的新增、移除與改名。

## 單檔腳本的依賴 (PEP 723)

不值得建整個專案的小工具，把依賴寫在腳本檔頭，`uv run` 會自動建立暫時環境：

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.1", "matplotlib"]
# ///
import pandas as pd
...
```

```bash
uv add --script plot_qc.py seaborn   # 幫腳本加依賴（改寫檔頭）
uv run plot_qc.py                    # 隔離環境執行，不污染其他專案
uvx ruff check .                     # 臨時執行 CLI 工具，不必安裝（= uv tool run）
```

本筆記中的 `uv run --no-project` 也是同樣概念：在不屬於任何專案的情況下執行腳本。
