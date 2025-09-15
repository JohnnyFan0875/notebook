# Configuration Files

Configuration files allow programs to store settings and parameters separately from the source code. This improves flexibility, maintainability, and security (e.g., avoiding hardcoding secrets). Many real-world applications need configuration:

- **Content Management Systems** (WordPress, WikiMedia, Joomla): database credentials
- **Proprietary software**: license keys or registration info
- **Scientific software**: library paths (e.g., BLAS)

For small projects, you might hardcode variables, but this is discouraged — especially if the code is public.

## Common Configuration Formats

### 1. Python File (`.py`)

Write configs as Python code in a separate file, e.g., `config.py`.

```python
# config.py
import preprocessing

mysql = {
    "host": "localhost",
    "user": "root",
    "passwd": "my secret password",
    "db": "write-math",
}

preprocessing_queue = [
    preprocessing.scale_and_center,
    preprocessing.dot_reduction,
    preprocessing.connect_lines,
]

use_anonymous = True
```

Usage:

```python
import config as cfg
connect(cfg.mysql["host"], cfg.mysql["user"], cfg.mysql["passwd"])
```

- **Pros**: simple, full Python support
- **Cons**: mixes logic/config, not user-friendly

### 2. JSON (`.json`)

```json
{
  "mysql": {
    "host": "localhost",
    "user": "root",
    "passwd": "my secret password",
    "db": "write-math"
  },
  "other": {
    "preprocessing_queue": [
      "preprocessing.scale_and_center",
      "preprocessing.dot_reduction",
      "preprocessing.connect_lines"
    ],
    "use_anonymous": true
  }
}
```

Read in Python:

```python
import json

with open("config.json") as f:
    data = json.load(f)
```

- **Pros**: standardized, cross-language, structured
- **Cons**: no comments

### 3. YAML (`.yaml` / `.yml`)

```yaml
mysql:
  host: localhost
  user: root
  passwd: my secret password
  db: write-math

other:
  preprocessing_queue:
    - preprocessing.scale_and_center
    - preprocessing.dot_reduction
    - preprocessing.connect_lines
  use_anonymous: yes
```

Read in Python:

```python
import yaml

with open("config.yml", "r") as f:
    cfg = yaml.safe_load(f)
```

- **Pros**: human-friendly, supports comments
- **Cons**: requires `PyYAML`

### 4. INI (`.ini`, `.cfg`, `.conf`)

```ini
[mysql]
host=localhost
user=root
passwd=my secret password
db=write-math

[other]
preprocessing_queue=["preprocessing.scale_and_center", "preprocessing.dot_reduction", "preprocessing.connect_lines"]
use_anonymous=yes
```

Using ConfigParser:

```python
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

print(config["mysql"]["host"])
print(config.getboolean("other", "use_anonymous"))
```

- **Pros**: simple, stdlib support
- **Cons**: all values are strings by default

### 5. XML (`.xml`)

Less common in Python, but supported.

```xml
<config>
  <mysql>
    <host>localhost</host>
    <user>root</user>
    <passwd>my secret password</passwd>
    <db>write-math</db>
  </mysql>
  <other>
    <preprocessing_queue>
      <li>preprocessing.scale_and_center</li>
      <li>preprocessing.dot_reduction</li>
      <li>preprocessing.connect_lines</li>
    </preprocessing_queue>
    <use_anonymous value="true" />
  </other>
</config>
```

Parse with BeautifulSoup:

```python
from bs4 import BeautifulSoup

with open("config.xml") as f:
    soup = BeautifulSoup(f, "xml")

print(soup.mysql.host.text)
```

- **Pros**: structured, mature ecosystem
- **Cons**: verbose, rarely used in Python configs

## File Endings & Conventions

- `.py` → Python config
- `.json` → JSON
- `.yaml` / `.yml` → YAML
- `.ini` / `.cfg` / `.conf` → INI/config files
- `~/.myapprc` → common Linux convention (RC = "run commands")

## Comparison Table

| Format | Human-Friendly | Comments | Libraries Needed             | Typical Use             |
| ------ | -------------- | -------- | ---------------------------- | ----------------------- |
| Python | ✔️             | ✔️       | None                         | Small scripts, dev-only |
| JSON   | ➖             | ❌       | None                         | Web apps, APIs          |
| YAML   | ✔️             | ✔️       | `PyYAML`                     | Configs, CI/CD          |
| INI    | ✔️             | Limited  | None                         | Legacy, simple configs  |
| XML    | ➖             | ✔️       | `BeautifulSoup`, `xml.etree` | Legacy enterprise       |

## Resources

- [Martin Thoma](https://martin-thoma.com/configuration-files-in-python/)
