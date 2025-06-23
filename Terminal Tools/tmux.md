# tmux

## Introduction

`tmux` is a terminal multiplexer that allows you to manage multiple terminal sessions within a single window. It's ideal for remote work, long-running processes, and improving CLI workflow efficiency.

- Official GitHub: [https://github.com/tmux/tmux](https://github.com/tmux/tmux)
- Run `man tmux` for the full manual

## Starting and Managing Sessions

```bash
tmux                   # Start a new tmux session (default name)
tmux new -s mysession  # Start a new session with a custom name
tmux ls                # List all active tmux sessions
tmux a -t 0            # Reattach to the session with ID 0
tmux a -t mysession    # Reattach to a named session
```

## Common Key Bindings (Prefix: `Ctrl+b`)

| Key Binding | Action                             |
| ----------- | ---------------------------------- |
| `Ctrl+b c`  | Create a new window                |
| `Ctrl+b w`  | View all sessions and windows list |
| `Ctrl+b x`  | Close the current window           |
| `Ctrl+b d`  | Detach from the current session    |
| `Ctrl+d`    | Exit the current shell (window)    |

> All shortcuts must be used after pressing the prefix Ctrl+b. For example: press Ctrl and b together, release, then press c.

## Closing Sessions

```bash
exit                            # Exit the current shell (session ends when all windows close)
tmux kill-session -t mysession  # Kill a specific session
tmux kill-server                # Kill all sessions and exit tmux entirely
```

## Tips

- Rename a session:
  ```bash
  tmux rename-session -t 0 newname
  ```
  Useful when running persistent processes like: `htop`, `ssh`, `vim`, `python`, `top`, `conda`, etc.
