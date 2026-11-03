[Computing](../README.md) › [開發者工具](README.md) › 壓縮與封存

# 壓縮與封存 (Compression and Archiving)

封存 (archive) 把多個檔案打包成一個（`tar`），壓縮 (compression) 縮小檔案（`gzip`、`zstd`、`xz`）；`.tar.gz` 是兩者合用。生資資料幾乎都以壓縮形式存放，而且有些工具**要求特定格式**（`bgzip` 才能建索引）。

## 格式選擇

| 格式 | 指令 | 速度 / 壓縮率 | 用途 |
| --- | --- | --- | --- |
| `.gz` | `gzip` / `pigz`（多執行緒） | 中 / 中 | 最通用；FASTQ、TSV |
| `.bgz` / `.gz`（BGZF） | `bgzip`（htslib） | 中 / 中 | **VCF、BED、GFF 要用 tabix 建索引時必須用 bgzip**；與 gzip 相容可直接 `zcat` |
| `.zst` | `zstd` | 快 / 高 | 新專案的中間檔、備份 |
| `.xz` | `xz` | 慢 / 最高 | 長期封存、發佈 |
| `.bz2` | `bzip2` | 慢 / 高 | 舊資料 |
| `.zip` | `zip` / `unzip` | 中 / 中 | 與 Windows 交換 |
| `.7z` | `7z` | 慢 / 高 | 分割成多個檔案、跨平台 |
| `.tar` | `tar` | 不壓縮 | 只打包 |

> BAM、CRAM 已內建壓縮，再 gzip 幾乎沒有效果。

## tar

```bash
tar -czvf project.tar.gz project/              # c 建立、z gzip、v 顯示、f 指定檔名
tar -xzvf project.tar.gz -C /path/to/dest      # x 解開到指定目錄
tar -tzvf project.tar.gz | head                # t 只列出內容，不解開
tar -xzvf archive.tar.gz --wildcards '*data/*.csv'   # 只解開符合的檔案
tar -cvf - project/ | zstd -T8 > project.tar.zst     # 搭配其他壓縮器（多執行緒 zstd）
tar --zstd -xvf project.tar.zst                      # GNU tar 1.31+ 直接支援 zstd
```

| 選項 | 意義 |
| --- | --- |
| `-c` / `-x` / `-t` | 建立 / 解開 / 列出 |
| `-z` / `-j` / `-J` | gzip / bzip2 / xz |
| `-v` | 顯示處理中的檔名 |
| `-f` | 指定封存檔名（放在最後，後面緊接檔名） |
| `-C` | 解開到指定目錄 |
| `--exclude='*.tmp'` | 排除 |

> 解開前先用 `-t` 看內容：有些封存檔沒有最上層目錄，直接解開會把一堆檔案灑在目前目錄。

## gzip / bgzip

```bash
gzip file.txt                      # → file.txt.gz（原檔被取代）
gzip -k file.txt                   # -k：保留原檔
gunzip file.txt.gz                 # 解壓
zcat file.txt.gz | head            # 不解壓直接看
pigz -p 8 big.fastq                # 多執行緒 gzip

bgzip -@ 4 calls.vcf               # → calls.vcf.gz（BGZF 區塊壓縮）
tabix -p vcf calls.vcf.gz          # 建索引 → 可依區域快速查詢
gzip -t file.gz && echo OK         # 檢查壓縮檔是否完整（下載中斷常造成損壞）
```

一般 gzip 壓縮的 VCF 用 tabix 建索引會失敗；用 `zcat x.vcf.gz | bgzip > x.bgz.vcf.gz` 重壓。見 [tabix](../../biology/bioinformatics-tools/ngs-tools/tabix.md)。

## 7z：分割大檔

```bash
sudo apt install p7zip-full           # 安裝（提供 7z 指令）
7z a -v100m archive.7z big_folder/    # 壓縮並分割成每份 100 MB：archive.7z.001, .002, ...
7z x archive.7z.001                   # 從第一份解開，自動合併所有分割檔
7z l archive.7z                       # 列出內容
```

適合上傳有單檔大小限制的平台、或用 email / 隨身碟分批傳送。Windows 上 7-Zip 圖形介面可直接開啟 `.7z`、`.tar.gz`、`.zip`。

## 實務守則

| 守則 | 原因 |
| --- | --- |
| 壓縮後、傳輸後核對 [檢查碼](checksums.md) | 確認沒有損壞 |
| 需要索引的檔案用 bgzip | tabix、bcftools、IGV 需要 |
| 大量小檔先 `tar` 再傳 | 傳輸與檔案系統對大量小檔很慢（HPC 檔案數配額） |
| 解開前先列出內容、指定目的地 | 避免覆蓋或灑滿目前目錄 |
