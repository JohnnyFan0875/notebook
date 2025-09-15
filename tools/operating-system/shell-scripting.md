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

### Command substitution

```bash
DATE=$(date)
echo "Today is $DATE"
```

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

## Functions

```bash
#!/bin/bash

greet() {
    echo "Hello, $1"
}

greet Alice
greet Bob
```

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
while read line; do
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

### Combining commands

```bash
mkdir logs && cd logs || exit 1
```

- `&&` → run second command if first succeeds
- `||` → run second command if first fails

## Summary

- Use `#!/bin/bash` at the top of scripts.
- Variables store values and can include command substitution.
- Control flow uses `if`, `elif`, `else`, `case`.
- Loops: `for`, `while`, `until`.
- Functions encapsulate reusable code.
- Use `$?` for exit status and `$@` for arguments.
- Scripts are made executable with `chmod +x script.sh`.
