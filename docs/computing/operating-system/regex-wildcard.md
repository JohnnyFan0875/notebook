# Regex and Wildcard Usage in Linux

This document provides a reference for using **wildcards** and **regular expressions (regex)** in Linux command-line operations.

| Feature               | Wildcards (globbing)                                                                                     | Regex (regular expressions)                                                      |      |
| --------------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ---- |
| **Who interprets it** | The **shell** (before running the command)                                                               | The **tool** (e.g., `grep`, `sed`, `awk`)                                        |      |
| **Scope**             | Matches **filenames/paths**                                                                              | Matches **text inside files/streams**                                            |      |
| **Common symbols**    | `*` (any chars), `?` (one char), `[abc]` (char set), `{1..10}` (brace expansion)                         | `.` (any char), `^` (start), `$` (end), `.*`, `[0-9]`, \`(a                      | b)\` |
| **Complexity**        | Simple, limited                                                                                          | Very powerful, supports advanced patterns                                        |      |
| **Examples**          | `ls *.txt` → matches all files ending in `.txt`                                                          | `grep '^ATG' genes.txt` → matches lines starting with `ATG`                      |      |
| **Expansion**         | Shell expands the pattern **before** running command (e.g., `ls *.txt` becomes `ls file1.txt file2.txt`) | Regex pattern is **passed to the program** (`grep`, `awk`) and interpreted there |      |
| **Use case**          | File/path matching                                                                                       | Searching/modifying text content                                                 |      |

## Wildcards (Globbing)

### Common wildcards

- `*` → matches zero or more characters
- `?` → matches exactly one character
- `[abc]` → matches any one character inside brackets (a, b, or c)
- `[0-9]` → matches any digit
- `{1..10}` → brace expansion (numbers 1 to 10)

### Examples

```bash
ls *.txt            # list all .txt files
ls file?.txt        # matches file1.txt, fileA.txt but not file10.txt
ls file{1..10}.txt  # expands to file1.txt file2.txt ... file10.txt
```

## Regex Basics

Regular expressions are patterns interpreted by tools like `grep`, `sed`, `awk`, `perl`.

### Common tokens

- `.` → any single character
- `^` → start of line
- `$` → end of line
- `.*` → zero or more characters
- `\d` → digit (in some regex engines, e.g., Perl)
- `[A-Za-z]` → any letter
- `(pattern1|pattern2)` → either pattern1 or pattern2

### Example with grep

```bash
grep '^ATG' genes.txt      # lines starting with ATG
grep 'end$' genes.txt      # lines ending with 'end'
grep -E 'cat|dog' pets.txt # matches cat or dog
```

## Using Regex and Wildcards in Commands

### grep

```bash
grep 'error' logfile               # find 'error'
grep -i 'error' logfile            # case-insensitive
grep -v 'debug' logfile            # exclude lines with 'debug'
grep -E 'error|warning' logfile    # extended regex: match error or warning
```

### sed (stream editor)

```bash
# Remove ANSI escape characters
sed 's/\x1b\[[0-9;]*m//g' filename

# Replace all digits with X
sed 's/[0-9]/X/g' file.txt
```

### awk

```bash
# Print lines where 3rd column > 20
awk '$3 > 20 {print}' file.txt

# Count lines with regex match in column 2
awk '$2 ~ /regex/ {n++} END {print n}' file.txt
```

### find

```bash
# Find .txt files recursively
find . -type f -name "*.txt"

# Regex-like with -regex
find . -regex ".*file[0-9]\\.txt"
```

## Removing ANSI Escape Characters

```bash
less filename | sed 's/\x1b\[[0-9;]*m//g'
```

This cleans color codes from log files or terminal output.

## Examples

```bash
# Match multiple keywords in one command
egrep 'keyword1|keyword2|keyword3' file.txt

# Exclude multiple patterns
egrep -iv 'conflict|error|fail' logfile

# Use wildcard in grep (requires quotes)
grep "file.*txt" list.txt
```

## Summary

- **Wildcards (globbing)** → expanded by shell (before command runs). Used in `ls`, `cp`, `mv`.
- **Regex** → interpreted by tools like `grep`, `sed`, `awk`. Much more powerful and flexible.
- Use `grep -E` (extended regex) for advanced patterns.
- Combine with tools (`find`, `sed`, `awk`) for powerful text and file operations.
