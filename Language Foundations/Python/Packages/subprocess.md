# Python `subprocess` Module

The `subprocess` module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes. It is the preferred way to run external commands in Python.

## 1. Basic Usage

### Run a simple shell command

```python
import subprocess

# Executes a command and waits for it to complete
subprocess.run(["ls", "-l"])
```

### With `shell=True` (string command)

```python
subprocess.run("ls -l", shell=True)
```

> 🔸 Use `shell=True` with caution due to security implications when using untrusted input.

## 2. Capturing Output

```python
result = subprocess.run(["echo", "hello"], capture_output=True, text=True)
print(result.stdout)  # prints 'hello\n'
```

### With older Python versions

```python
result = subprocess.run(["echo", "hello"], stdout=subprocess.PIPE)
print(result.stdout.decode())
```

## 3. Getting the Return Code

- Exit status of the command (int)
- Check if command succeeded

```python
completed = subprocess.run(["ls", "nonexistent"], capture_output=True)
print(completed.returncode)  # Non-zero indicates failure
```

## 4. Redirecting stdout/stderr

```python
with open("output.txt", "w") as f:
    subprocess.run(["ls", "-l"], stdout=f)
```

### Redirect stderr to stdout

```python
subprocess.run(["ls", "nonexistent"], stderr=subprocess.STDOUT)
```

## 5. Using `Popen` for Advanced Control

```python
from subprocess import Popen, PIPE

process = Popen(["grep", "foo"], stdin=PIPE, stdout=PIPE, text=True)
stdout, stderr = process.communicate(input="foo\nbar\nbaz")
print(stdout)  # prints 'foo\n'
```

## 6. Common Parameters

| Parameter         | Description                                  |
| ----------------- | -------------------------------------------- |
| `args`            | List or string of command and arguments      |
| `shell`           | Run through the shell (e.g., `/bin/sh`)      |
| `capture_output`  | Shortcut for capturing stdout and stderr     |
| `stdout`/`stderr` | Redirect output streams                      |
| `cwd`             | Set the working directory for the subprocess |
| `env`             | Pass custom environment variables            |
| `timeout`         | Time to wait before killing process          |
| `check`           | Raise error if returncode != 0               |

## 7. Raise Exception on Failure

```python
subprocess.run(["false"], check=True)  # Raises CalledProcessError
```

## 8. Security Notes

- Avoid `shell=True` when passing untrusted input.
- Prefer `list` over `str` for `args`.
- Validate all inputs when building dynamic command lines.

## 9. Use Cases

- Run shell scripts or CLI tools (e.g., `ffmpeg`, `bcftools`, `aws cli`)
- Automate data preprocessing pipelines
- Chain multiple commands using pipes (`Popen`)
- Invoke bioinformatics tools from within Python workflows
