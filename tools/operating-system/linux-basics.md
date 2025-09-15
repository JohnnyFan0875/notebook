# Linux Basic Commands

This document provides a quick reference for common Linux shell commands, organized by category. Useful for file operations, searching, user management, system monitoring, scripting, and history.

## File Operations

### Count rows in a file

```bash
wc -l filename
less /home/test.txt | wc -l
```

### View top/bottom rows

```bash
head -n 10 filename   # top 10 rows
tail -n 10 filename   # bottom 10 rows
```

### Read file by line (paged view)

```bash
less -S filename
```

### Merge files and read by line

```bash
cat file1.txt file2.txt | less -S
```

## Searching and Filtering

### Grep basics

```bash
grep 'keyword' filename          # match lines
grep -v 'keyword' filename       # exclude lines
```

### Grep multiple keywords

```bash
egrep 'keyword1|keyword2|keyword3' file_path
grep -e 'keyword1' -e 'keyword2' -e 'keyword3' file_path
egrep -iv 'keyword1|keyword2|keyword3' file_path            # -i ignore case, -v invert match
```

### Search compressed files

```bash
zgrep 'pattern' file.gz
zcat file.gz | grep 'pattern'
```

### Find files or directories

```bash
find /path -type f -name "*.txt"     # find files
find /path -type d -name "dirname"   # find directories
find <start_path> -name <pattern>    # recursive find
```

### Find and execute command

```bash
find . -name "*.xls" | xargs wc -l     # count rows in each file
find ./data -name "*.bam" -exec ls -lh {} \;   # list matching files with details
```

## Text Processing

### awk examples

```bash
# Count rows where column 3 > 20
awk '{if($3>20) n+=1} END {print n}' filename

# Print rows where column 3 > 20
awk '$3>20 {print}' filename | wc -l

# Exclude header, compute count and ratio
grep -v 'COV' filename | awk '{if($3>20) n+=1; m+=1} END {print n,m,n/m}'
```

## User Management

### Add user (requires sudo)

```bash
sudo useradd -m username     # -m creates home directory
sudo passwd username
```

### Modify users and groups

```bash
less /etc/group                    # list groups
usermod -a -G groupname username   # add user to group
less /etc/passwd                   # view user info
```

## System Information

### Clear terminal

```bash
ctrl+l   # same as clear
```

### Disk usage

```bash
df -h    # human-readable disk usage
du -sh * # size of each folder in current directory
```

### Memory usage

```bash
free -h
```

### Processes

```bash
top        # interactive process monitor
htop       # improved top (if installed)
ps aux     # list all running processes
```

## Shell Scripting Basics

### Simple shell script template

```bash
#!/bin/bash

# Read file line by line
while read line; do
    echo "$line"
    # do something with $line
done < filename
```

### Make script executable

```bash
chmod +x script.sh
./script.sh
```

## History and Command Recall

### Show command history

```bash
history
```

### Re-run a command by number

```bash
!2010   # runs command at history line 2010
```

### Examples

```bash
$ history | tail -3
 2009  history
 2010  echo test
 2011  history | tail -3

$ !2010
 echo test
 test
```

### Permissions

```bash
chmod 755 file   # owner rwx, group r-x, others r-x
chown user:group file
```

### Networking

```bash
ping -c 4 google.com
curl -I https://example.com   # fetch headers
wget https://example.com/file.zip
```

### Compression

```bash
tar -czvf archive.tar.gz folder/  # compress
tar -xzvf archive.tar.gz          # extract
```

### Package management (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install package_name
```
