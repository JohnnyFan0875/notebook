# Shell Scripting Basics

## Shebang

Every shell script should start with a **shebang** line to specify the interpreter:

```bash
#!/bin/bash
```

## Variables

### Assign and use variables

```bash
NAME="Alice"
echo "Hello, $NAME"
```

- No spaces around `=` during assignment.
- Quote expansions when values may contain spaces: `echo "$NAME"`.

### Command substitution

```bash
DATE=$(date)
echo "Today is $DATE"
```

Prefer `$(...)` over backticks because it is easier to read and nest.

## Arrays

### Indexed arrays

```bash
fruits=("apple" "banana" "pear")
echo "${fruits[0]}"
echo "${fruits[@]}"
echo "${#fruits[@]}"
```

- `${array[@]}` expands to all elements.
- `${#array[@]}` returns the array length.

### Associative arrays

```bash
declare -A city_details=([city_name]="New York" [population]=14000000)
echo "${city_details[city_name]}"
```

Associative arrays require `declare -A`.

## Script Arguments

- `$0` → script name
- `$1`, `$2`, ... → positional arguments
- `$@` → all arguments
- `$#` → number of arguments

```bash
#!/bin/bash

echo "Script name: $0"
echo "First argument: $1"
echo "All arguments: $@"
echo "Number of arguments: $#"
```

## Conditionals

### if / else

```bash
if [ -f file.txt ]; then
    echo "file.txt exists"
else
    echo "file.txt not found"
fi
```

### Common comparison patterns

```bash
if [ "$name" = "alice" ]; then
    echo "match"
fi

if [ "$count" -gt 10 ]; then
    echo "greater than ten"
fi
```

- Use `=` or `!=` for strings.
- Use flags such as `-eq`, `-ne`, `-gt`, `-lt`, `-ge`, `-le` for integers.
- Use quotes around variable expansions inside tests.

### elif

```bash
if [ "$1" -eq 1 ]; then
    echo "One"
elif [ "$1" -eq 2 ]; then
    echo "Two"
else
    echo "Other"
fi
```

### File-related tests

```bash
if [ -f file.txt ]; then
    echo "regular file exists"
fi

if [ -d logs ]; then
    echo "directory exists"
fi
```

Common flags:

- `-f`: regular file exists
- `-d`: directory exists
- `-e`: path exists
- `-s`: file exists and is non-empty
- `-r`, `-w`, `-x`: readable, writable, executable

### Combining conditions

```bash
if [[ -f "$file" && "$name" != "tmp" ]]; then
    echo "process file"
fi
```

`[[ ... ]]` is often safer and clearer for compound conditions.

### Using command exit status directly

```bash
if grep -q "ERROR" app.log; then
    echo "error found"
fi
```

This is usually better than wrapping the command in command substitution just to test success.

## Loops

### For loop

```bash
for i in 1 2 3 4 5; do
    echo "Number: $i"
done
```

### For loop over files

```bash
for file in *.txt; do
    echo "Processing $file"
done
```

### Loop over command output carefully

```bash
for file in ./*.csv; do
    [ -e "$file" ] || continue
    echo "Processing $file"
done
```

Prefer globbing over parsing `ls` output inside loops.

### While loop

```bash
count=1
while [ $count -le 5 ]; do
    echo "Count: $count"
    count=$((count + 1))
done
```

### Until loop

```bash
count=1
until [ $count -gt 5 ]; do
    echo "Count: $count"
    count=$((count + 1))
done
```

## Arithmetic

```bash
count=5
count=$((count + 1))
echo "$count"
```

Use arithmetic expansion for simple integer math.

## Functions

```bash
#!/bin/bash

greet() {
    echo "Hello, $1"
}

greet Alice
greet Bob
```

### Scope and local variables

Variables are global by default in Bash functions unless declared local.

```bash
greet() {
    local name="$1"
    echo "Hello, $name"
}
```

Use `local` inside functions to reduce unintended side effects.

## Exit Status

- `$?` → exit status of last command (0 = success)

```bash
ls /tmp
if [ $? -eq 0 ]; then
    echo "Command succeeded"
else
    echo "Command failed"
fi
```

## Useful Patterns

### Reading a file line by line

```bash
while IFS= read -r line; do
    echo "Line: $line"
done < filename.txt
```

### Case statement

```bash
case "$1" in
    start)
        echo "Starting..." ;;
    stop)
        echo "Stopping..." ;;
    *)
        echo "Usage: $0 {start|stop}" ;;
esac
```

`case` is often cleaner than long chains of `if` and `elif` when matching discrete modes or patterns.

### Combining commands

```bash
mkdir logs && cd logs || exit 1
```

- `&&` → run second command if first succeeds
- `||` → run second command if first fails

### Pipes for small text workflows

```bash
sort fruits.txt | uniq -c | head -n 3
cut -d "," -f 2 data.csv | sort | uniq
```

Pipes are useful when each command performs one clear transformation.

## Summary

- Use `#!/bin/bash` at the top of scripts.
- Variables store values and can include command substitution.
- Arrays and associative arrays help structure repeated values.
- Control flow uses `if`, `elif`, `else`, `case`.
- Loops: `for`, `while`, `until`.
- Functions encapsulate reusable code, and `local` helps control scope.
- Use `$?` for exit status and `$@` for arguments.
- Scripts are made executable with `chmod +x script.sh`.
