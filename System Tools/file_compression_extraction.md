# Compress and Extract Files

## Introduction

File compression and extraction are essential tasks for managing large files, backups, and software packaging. This document covers two popular tools:

- `tar` – Native to Unix/Linux, widely used for `.tar`, `.tar.gz` formats.
- `7z` (7-Zip) – A high-compression ratio tool, commonly used for splitting archives.

## tar

### Extract/Compress file

Extract tar.gz file

```bash
tar -zxvf inputfile.tar.gz -C /path/to/destination

# Extract specific file(s) by keyword/regex
tar -zxvf archive.tar.gz --wildcards '*pattern*'
tar -zxvf archive.tar.gz --wildcards '*data/*.csv'
```

Compress tar.gz file

```bash
tar -zcvf archive_name.tar.gz /path/to/folder
```

- `-z`: gzip compression
- `-x`: extract
- `-c`: create new archive
- `-v`: verbose (show file names)
- `-f`: specify file name
- `-C`: extract to a target directory

## 7z (7-Zip)

### Install p7zip

```bash
sudo apt-get update
sudo apt-get install p7zip-full
```

### Split & Compress Large File

```bash
7zr -v100m a archive.7z file_or_folder
```

This will generate:

```text
archive.7z.001
archive.7z.002
...
```

- `-v100m`: split into parts of 100 MB

### Merge and Extract Multi-Part Archive

```bash
7zr x archive.7z.001
```

- This automatically combines all .7z.00x parts and extracts contents

## Tips

- Prefer `tar.gz` for cross-platform - compatibility.
- Use `7z` when dealing with very large files or needing advanced compression and splitting.
- Always double-check extraction paths to avoid overwriting files.
