[Computing](../README.md) › [容器與環境](README.md) › 虛擬機

# 虛擬機：VirtualBox (Virtual Machine)

在自己的電腦上跑一台完整的 Linux（或其他 OS）。Windows 使用者要 Linux 命令列環境時，[WSL 2](../operating-system/windows-and-wsl.md) 更輕量、整合更好；需要完整桌面環境、測試不同發行版、或要強隔離時才用 VirtualBox。概念比較見 [容器與虛擬化](containerization-and-virtualization.md)。

| 項目 | 內容 |
| --- | --- |
| 軟體 | [VirtualBox](https://www.virtualbox.org/)（免費）；替代：VMware Workstation、Hyper-V（Windows 內建）、UTM（Apple Silicon Mac） |
| 適合 | 完整 Linux 桌面、測試安裝流程、隔離不信任的軟體 |
| 不適合 | 日常命令列開發（用 WSL）、大量運算（用伺服器或雲端） |

## 常見問題

### 縮小 `.vdi` 虛擬磁碟

動態配置的磁碟刪檔後不會自動縮小。

```bash
# 1. 在 VM 內：把可用空間填零，再刪除（讓已刪除的區塊可被壓縮）
sudo dd if=/dev/zero of=/EMPTY bs=1M; sudo rm -f /EMPTY
# 2. 關閉 VM（完全關機，不是儲存狀態）
# 3. 在主機上壓縮
VBoxManage modifymedium disk /path/to/disk.vdi --compact
```

### 剪貼簿與共用資料夾

| 問題 | 處理 |
| --- | --- |
| 雙向剪貼簿 / 拖放無效 | VM 內安裝 Guest Additions（裝置 → 插入 Guest Additions CD 映像），設定 → 一般 → 進階 → 共用剪貼簿：雙向 |
| 共用資料夾無權限存取（`/media/sf_*`） | `sudo usermod -aG vboxsf $USER`，重新開機 |
| 視窗大小無法自動調整 | 安裝 Guest Additions；顯示卡控制器改 VMSVGA |

### 讓自己的帳號可以用 sudo

```bash
su -                              # 切換到 root（Debian 安裝時設定的 root 密碼）
usermod -aG sudo <username>       # Debian / Ubuntu；RHEL 系列的群組是 wheel
exit                              # 重新登入後生效
```

### 終端機打不開（Ubuntu）

常見原因是 locale 設定不完整：

```bash
# 按 Ctrl + Alt + F3 進入文字模式登入（Ctrl + Alt + F1 或 F2 回圖形介面）
sudo localectl set-locale LANG=en_US.UTF-8
sudo reboot
```
