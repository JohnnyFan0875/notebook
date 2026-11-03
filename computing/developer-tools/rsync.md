# rsync

## Introduction

`rsync` is a powerful and efficient command-line utility used for **file synchronization and transfer**. It minimizes data transfer by sending only the differences between source and destination. It works both **locally** and over **remote connections** via SSH.

Common use cases include:

- Backing up files
- Syncing directories between systems
- Incremental file transfers

## Basic Syntax

```bash
rsync [options] <source> <destination>

rsync -avh myfile.txt /backup/
rsync -avh /home/johnny/test/ /home/amy/test/
```

### Common options

| Option     | Description                               |
| ---------- | ----------------------------------------- |
| `-a`       | Archive mode (preserves metadata)         |
| `-v`       | Verbose output                            |
| `-h`       | Human-readable sizes                      |
| `--delete` | Delete files in destination not in source |
| `-z`       | Compress file data during transfer        |
| `-e ssh`   | Use SSH for remote transfer               |

## Tips

- Add `--dry-run` to preview what will happen without making changes:
  ```bash
  rsync -avh --dry-run /source/ /dest/
  ```
- Use --exclude to skip specific files:
  ```bash
  rsync -avh --exclude='*.tmp' /source/ /dest/
  ```
- A trailing slash `/` in the source path means sync contents of the directory, not the directory itself.

  - Folder structure before:

    ```text
    src/
    ├── file1.txt
    └── file2.txt

    dest/
    ```

  - After running: `rsync -avh src dest/`

    ```text
    src/
    ├── file1.txt
    └── file2.txt

    dest/
    └── src/
        ├── file1.txt
        └── file2.txt
    ```

  - After running: `rsync -avh src/ dest/`

    ```text
    src/
    ├── file1.txt
    └── file2.txt

    dest/
    ├── file1.txt
    └── file2.txt
    ```
