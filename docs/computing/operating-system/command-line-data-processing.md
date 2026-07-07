# Command-Line Data Processing

## Why Use the Shell for Data Tasks

The shell is useful when data work is lightweight, repeatable, and file-oriented. It is especially effective for:

- downloading files
- inspecting delimited text
- filtering and reshaping small to medium datasets
- chaining simple transformations
- automating recurring jobs

It is not a replacement for Python, R, or SQL in every situation, but it is often the fastest layer for glue work.

## Downloading Data

### `curl`

`curl` is a command-line client for transferring data to and from URLs.

```bash
curl -O https://example.com/data.csv
curl -L -o data.csv https://example.com/download?id=123
```

Useful habits:

- use `-O` to keep the remote filename
- use `-o <file>` to choose the output filename
- use `-L` when redirects are expected

### `wget`

`wget` is another common download tool, often convenient for recursive or resumable downloads.

```bash
wget https://example.com/data.csv
```

## CSV-Focused Tools with `csvkit`

`csvkit` is a suite of command-line tools for working with CSV files.

### Installation

```bash
pip install csvkit
```

### Common commands

| Command | Purpose |
| --- | --- |
| `csvlook` | Pretty-print CSV as a table |
| `csvcut` | Select columns |
| `csvgrep` | Filter rows |
| `csvstat` | Summarize columns |
| `csvsql` | Query CSV with SQL-like syntax |

### Examples

```bash
csvlook data.csv
csvcut -c "track_id,danceability" songs.csv
csvgrep -c artist -m "Adele" songs.csv
csvstat songs.csv
```

## SQL-Like Workflows over Files

### Querying CSV directly

`csvsql` lets you query CSV files using SQL syntax.

```bash
csvsql --query "select artist, count(*) from songs group by artist" songs.csv
```

Practical reminders:

- keep the SQL query on one line when invoking from the shell
- make sure file references line up with the query context

### Working with databases from the shell

Shell workflows often bridge into SQLite, PostgreSQL, or MySQL when flat files are no longer enough.

This is useful when:

- joins become complex
- indexing matters
- repeated querying is more important than one-off filtering

## Text and Table Processing Patterns

The most common shell data pattern is a pipeline where each tool performs one transformation.

```bash
cut -d "," -f 2 data.csv | sort | uniq -c | head
```

Typical tool roles:

| Tool | Role |
| --- | --- |
| `cut` | Select fields |
| `sort` | Order rows |
| `uniq` | Collapse repeated adjacent values |
| `head` / `tail` | Inspect the start or end |
| `wc` | Count lines, words, or bytes |
| `grep` | Filter text by pattern |
| `sed` | Apply stream edits |

## Scheduling and Automation

`cron` is a time-based scheduler commonly used to automate shell scripts and lightweight data jobs.

Example cron shape:

```bash
* * * * * /path/to/command
```

The five fields represent minute, hour, day of month, month, and day of week.

Use cron when the task is:

- periodic
- non-interactive
- stable enough to run unattended

## When to Move Beyond the Shell

Move to Python, R, or a database workflow when:

- logic becomes deeply stateful
- transformations are hard to express as pipelines
- testing and maintainability matter more than quick iteration
- the data is too large or complex for ad hoc command chains

## Practical Takeaways

- Use the shell for repeatable glue work around files and datasets.
- `curl` and `wget` cover common download tasks.
- `csvkit` gives SQL-adjacent power for CSV inspection and reshaping.
- Pipelines are strongest when each command performs one small, understandable step.
- Scheduling with `cron` turns one-off shell commands into lightweight automation.
