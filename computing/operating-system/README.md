[Computing](../README.md) › 作業系統

# 作業系統與命令列 (Operating System)

在 Linux 伺服器、HPC、容器與 WSL 中工作的命令列基本功。生資工具與資料大多在 Linux 上，熟悉 shell 是使用它們的前提。

## 建議順序

```text
Windows 使用者先設定 WSL → Linux 基礎指令 → 正規表達式與萬用字元 → 命令列資料處理 → Shell 腳本
```

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Windows 與 WSL](windows-and-wsl.md) | WSL 2 安裝、檔案互通、CRLF、bash vs PowerShell 對照、Windows 設定 | 在 Windows 上怎麼取得 Linux 環境？ |
| [Linux 基礎指令](linux-basics.md) | 路徑、查看檔案、`grep` / `find`、權限、程序與磁碟、套件管理 | 在伺服器上怎麼找檔案、看內容、查資源？ |
| [正規表達式與萬用字元](regex-wildcard.md) | glob vs regex、BRE / ERE / PCRE、`grep` / `sed` / `awk` / `find` 用法 | `*.txt` 和 `.*txt` 差在哪？ |
| [命令列資料處理](command-line-data-processing.md) | `cut` / `sort` / `uniq` / `awk` / `join` / `comm`、生資檔案範例、csvkit、DuckDB、`jq`、cron | 不寫程式怎麼快速篩選、統計表格？ |
| [Shell 腳本](shell-scripting.md) | `set -euo pipefail`、引號、參數展開、條件、迴圈、函式、`trap`、平行 | 怎麼把指令寫成可靠、可重複的腳本？ |

| 下一步 | 筆記 |
| --- | --- |
| 遠端連線、傳檔、終端機多工 | [開發者工具](../developer-tools/README.md) |
| 安裝軟體與隔離環境 | [Conda 與容器](../containers-and-env/README.md) |
| 多步驟流程、HPC 排程 | [工作流引擎](../workflow-engines/README.md) |
