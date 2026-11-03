[Computing](../README.md) › [開發者工具](README.md) › 編輯器

# 編輯器：VS Code 與 Notepad++ (Editors)

VS Code 是主力編輯器：寫程式、Markdown 預覽、透過 Remote 擴充直接在 WSL / SSH 伺服器 / 容器裡開發。Notepad++ 是 Windows 上輕量的文字編輯器，適合快速開大型文字檔、用正規表達式批次取代。終端機中的編輯器（`nano`、`vim`）在伺服器上也要會基本操作。

## 換行符號與不可見字元

Windows 用 CRLF（`\r\n`）換行，Linux / macOS 用 LF（`\n`）。在 Windows 編輯的腳本拿到 Linux 執行，常出現 `$'\r': command not found` 或欄位尾端多一個 `^M`。

| 問題 | VS Code | Notepad++ | 命令列 |
| --- | --- | --- | --- |
| 看目前換行格式 | 右下狀態列顯示 `CRLF` / `LF`，點一下可切換 | 檢視 → 顯示符號 → 顯示行尾字元 | `file script.sh`（顯示 `with CRLF line terminators`） |
| 新檔預設用 LF | 設定搜尋 `files.eol` → 設為 `\n` | 設定 → 偏好設定 → 新文件 → Unix (LF) | — |
| 轉換既有檔案 | 狀態列切換後存檔 | 編輯 → 換行格式轉換 → 轉為 Unix (LF) | `dos2unix file`；`sed -i 's/\r$//' file` |
| 不換行空白 NBSP（`U+00A0`，從網頁複製常帶入） | 設定 `editor.unicodeHighlight.invisibleCharacters` 會標示 | 取代：尋找 `\x{A0}`，取代為空白，搜尋模式選「規則運算式」 | `sed -i 's/\xc2\xa0/ /g' file` |
| 移除所有換行（合併成一行） | 取代：啟用 regex，尋找 `\r?\n` | 取代：尋找 `\r\n`，規則運算式 | `tr -d '\r\n' < in > out` |

> Git 可以在提交時統一換行：`git config --global core.autocrlf input`（Linux / WSL / macOS），或在 repo 放 `.gitattributes`（`* text=auto eol=lf`），見 [Git](../version-control/git.md)。

## VS Code

### 常用快捷鍵（Windows / Linux；macOS 把 `Ctrl` 換成 `Cmd`）

| 按鍵 | 作用 |
| --- | --- |
| `Ctrl + Shift + P` | 命令選擇區：所有功能都能從這裡搜尋 |
| `Ctrl + P` | 依檔名快速開檔 |
| `` Ctrl + ` `` | 開關整合終端機 |
| `Ctrl + Shift + F` | 全專案搜尋 / 取代（支援 regex） |
| `Ctrl + D` | 選取下一個相同字串（多游標） |
| `Alt + 點擊` | 新增游標 |
| `Shift + Alt + F` | 格式化文件 |
| `F2` | 重新命名符號（跨檔案） |
| `Ctrl + /` | 切換註解 |
| `Ctrl + Shift + V` / `Ctrl + K V` | Markdown 預覽 / 並排預覽 |

### 常用設定

設定介面：`Ctrl + ,`；或命令選擇區 → Preferences: Open User Settings (JSON)。

```json
{
  "files.eol": "\n",
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "editor.formatOnSave": true,
  "editor.rulers": [100],
  "editor.parameterHints.enabled": false,
  "editor.unicodeHighlight.invisibleCharacters": true,
  "[markdown]": { "editor.wordWrap": "on" }
}
```

`editor.parameterHints.enabled: false` 關閉輸入函式時跳出的參數提示（覺得干擾時；需要時按 `Ctrl + Shift + Space` 叫出）。

### 擴充套件

| 擴充 | 用途 |
| --- | --- |
| Python、Pylance、Ruff | Python 語言支援、型別檢查、lint 與格式化 |
| Jupyter | 在 VS Code 中開 `.ipynb` |
| R | R 語言支援 |
| WSL | 在 [WSL](../operating-system/windows-and-wsl.md) 中開發（`code .`） |
| Remote - SSH | 直接編輯遠端伺服器上的檔案，見 [SSH](ssh.md#vs-code-remote-ssh) |
| Dev Containers | 在 Docker 容器中開發 |
| Markdown Preview Mermaid Support | 預覽中渲染 Mermaid 圖（見 [Markdown](../../productivity/documents/markdown.md)） |
| GitLens | 檢視每行的 commit 歷史 |
| Rainbow CSV | CSV / TSV 欄位上色、對齊 |

## Notepad++

| 功能 | 位置 |
| --- | --- |
| 正規表達式取代 | `Ctrl + H` → 搜尋模式：規則運算式 |
| 顯示所有字元（空白、tab、換行） | 檢視 → 顯示符號 → 顯示所有字元 |
| 編碼轉換 | 編碼 → 轉換為 UTF-8 |
| 欄選取（矩形選取） | `Alt + 拖曳` |
| 多檔搜尋 | `Ctrl + Shift + F` → 在檔案中尋找 |

## 終端機編輯器

在沒有圖形介面的伺服器上：

| 編輯器 | 最低限度 |
| --- | --- |
| `nano` | 直接打字；`Ctrl + O` 存檔、`Ctrl + X` 離開（底部有提示） |
| `vim` | `i` 進入輸入模式；`Esc` 回到一般模式；`:w` 存檔、`:q` 離開、`:wq` 存檔離開、`:q!` 不存檔離開 |

> `git commit` 沒有 `-m` 時會開預設編輯器（常是 vim）；可設定為 nano 或 VS Code：`git config --global core.editor "code --wait"`。
