# Python argparse

```python
import argparse

parser = argparse.ArgumentParser(
    description='Comprehensive argparse demo script',
    formatter_class=argparse.RawDescriptionHelpFormatter
)

# Positional argument
parser.add_argument("filename", help="input file path")

# Optional arguments with types and defaults
parser.add_argument("-p", "--port", type=int, default=5432, help="database port")
parser.add_argument("-m", "--mode", choices=["fast", "slow"], default="fast", help="execution mode")

# Boolean flags
parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity")
parser.add_argument("--quiet", action="store_true", help="suppress output")

# Multiple values
parser.add_argument("--names", nargs="+", help="list of names")

# Boolean option (Python 3.9+ style)
try:
    parser.add_argument("--feature", action=argparse.BooleanOptionalAction, help="enable/disable feature")
except Exception:
    parser.add_argument("--feature", action="store_true", help="enable feature")

# Required option
parser.add_argument("--config", required=True, help="config file path")

# Store constant
parser.add_argument("--debug", action="store_const", const=2, default=0, help="set debug level")

# Append values
parser.add_argument("--tag", action="append", help="add multiple tags")

# Subcommands
subparsers = parser.add_subparsers(dest="command", help="sub-commands")

# Subcommand: add
parser_add = subparsers.add_parser("add", help="add something")
parser_add.add_argument("--ip", help="target IP")

# Subcommand: remove
parser_remove = subparsers.add_parser("remove", help="remove something")
parser_remove.add_argument("--id", type=int, help="item ID")

args = parser.parse_args()

# Example usage of parsed args
print("Filename:", args.filename)
print("Port:", args.port)
print("Mode:", args.mode)
print("Verbosity level:", args.verbose)
print("Quiet mode:", args.quiet)
print("Names:", args.names)
print("Feature enabled:", args.feature)
print("Config file:", args.config)
print("Debug level:", args.debug)
print("Tags:", args.tag)

if args.command == "add":
    print("Subcommand add with IP:", args.ip)
elif args.command == "remove":
    print("Subcommand remove with ID:", args.id)
```

Run examples:

```bash
python script.py data.csv --config settings.yaml -p 3306 -m slow -vv --names Alice Bob --feature --tag alpha --tag beta add --ip 192.168.0.1
python script.py data.csv --config settings.yaml remove --id 42 --quiet
```
