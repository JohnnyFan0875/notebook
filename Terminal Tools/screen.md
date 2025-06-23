# GNU Screen

## Introduction

GNU `screen` is a terminal multiplexer that allows you to run and manage multiple terminal sessions within a single SSH session or terminal window. It is particularly useful for maintaining long-running processes on remote servers, as sessions can be detached and resumed even after disconnection.

- Run `man screen` for the full manual

## Starting and Managing Sessions

```bash
screen               # Start a new screen session
screen -S mysession  # Start a new session with a name
screen -ls           # List all existing screen sessions
screen -r <id/name>  # Reattach to a detached screen session
```

- If multiple sessions exist, use `screen -r <session_id>` to specify which one to reattach.

## Common Key Bindings (Prefix: `Ctrl+a`)

| Key Binding | Action                          |
| ----------- | ------------------------------- |
| `Ctrl+a d`  | Detach from the current session |
| `Ctrl+a c`  | Create a new window             |
| `exit`      | Exit the current window         |

> All key bindings begin with `Ctrl+a`. For example: press `Ctrl+a`, release, then press `c`.

## Closing Sessions

- Exit all windows with `exit`
- Kill a session manually:
  ```bash
  screen -X -S <session_id> quit
  ```

## Tips

- Each screen window acts like an independent terminal.
- Detaching with `Ctrl+a d` keeps your process running in the background.
- Use `screen -r` after SSH reconnect to pick up where you left off.
- Combine with long-running scripts, editors (`vim`, `nano`), or monitoring tools (`top`, `htop`, `watch`).
