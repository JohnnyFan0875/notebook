# Git

## Download Repository from GitHub

```bash
git clone <url>
```

## Updating an Existing Local Repo

```bash
git pull origin master  # First time
git pull  # After tracking branch is set
```

## Create Local Repo and Upload to GitHub

```bash
cd <dirpath>
git init
git remote add origin <github repository ssh> # for the first time

# Track and Stage
git add . # Adds all changes (new, modified, deleted) in the current directory tree
git add <file or folder>
git add . :^<exclude folder/file>
git add -u # Adds only modified and deleted files that are already tracked

# Commit changes
git commit -m <message_title> [-m <message_description>]  # Commit indexed files
git commit -am <message_title>  # Add & commit modified/deleted files only (skip `git add`)

# Push changes
git push -u origin master  # First-time push
git push  # Subsequent pushes
```

## Stash

Temporarily store changes in working directory that are not ready to be committed. It helps keep workspace clean without discarding your modifications.

- Saves uncommitted changes (both staged and unstaged) into a special stash stack.
- Reverts working directory to the last committed state (clean working tree).

```bash
git stash
git stash save "WIP: fixing bug in login feature" # Save with a custom message
git stash list

git stash apply # restores the most recent stash but keeps it in the list.
git stash pop # restores the most recent stash and removes it from the list.

git stash clear # Clear all stashes
```

- Example

  - Need to switch branches but have uncommitted changes

  ```bash
  git stash
  git checkout feature/new-branch
  ```

  - Pull updates without losing local modifications

  ```bash
  git stash
  git pull
  git stash pop
  ```

## Branching

```bash
# Create/switch branches
git checkout <branch_name>
git diff <branch_name>  # View differences with another branch

# Push branch
git push -u origin <branch_name>  # First-time push of a branch
git push  # Subsequent pushes

# Delete branches
git branch -d <branch_name>  # Local delete
git push origin -d <branch_name>  # Remote delete

# Merge branches
git checkout master
git merge <branch_name>  # Merge branch into master
```

## Undoing Git Actions

### Undoing commit

Move the HEAD, branch pointer, and optionally the working directory and staging area (index) to a different commit

```bash
git reset [<file_or_folder>]  # Unstage files
git reset HEAD~<n>  # Undo last n commits (soft reset)

git reset --soft <commit_id> # Uncommit, keep everything staged
git reset [--mixed] <commit_id> # Default, uncommit and unstage changes
git reset --hard <commit_id> # Discard all changes
```

### Undoing file edit

| Goal                                 | Best Command                                        |
| ------------------------------------ | --------------------------------------------------- |
| Unstage a file                       | `git reset <file>` or `git restore --staged <file>` |
| Discard file changes (working dir)   | `git restore <file>` (or `git checkout <file>`)     |
| Revert both staged + working changes | `git restore --staged --worktree <file>`            |

## Tag a Specific Commit

`git tag` is used to mark specific points in your Git history—usually to label important milestones like releases, versions, or stable checkpoints.

```bash
git log --oneline

# a1b2c3d Fix bug in login flow
# 4e5f6g7 Add user authentication
# 8h9i0j1 Initial commit

git tag v1.0 4e5f6g7 # creates a lightweight tag pointing to commit 4e5f6g7
git push origin v1.0
```

```bash
git tag # list all tags
```

## Delete Files

```bash
git rm <file>  # Remove from local and remote
git rm -r <folder>  # Remove folder

git rm --cached <file>  # Deletes the file from Git only, not from computer. (stop tracking a file already in git)
git rm --cached -r <folder>
```

## Git log

view the history of commits in a repository

```bash
git log
git log --oneline # One-line summary per commit
git log -n 5 # Shows the last 5 commits

git log --oneline --graph --all --decorate --color # Graph view of branching
```

## Merge commit

![Image](reference/git_merge_rebase.jpg)
Reference: [https://bytebytego.com/guides/git-merge-vs-git-rebate/](https://bytebytego.com/guides/git-merge-vs-git-rebate/)

## Git Worktree

```bash
# Create worktree branch in separate directory
git worktree add -b <branch_name> <folder_path> <source_branch>
cd <folder_path>

# Do work and commit to that branch
git add .
git commit -m <commit message>

# Remove worktree
git worktree remove <folder_path>
git worktree prune  # Clean up

# List all worktrees
git worktree list
```

## Git config

Git uses the `git config` command to configure settings that control how Git works.

1. `--system`

   - Applies to all users on the system.
   - Linux/macOS: `/etc/gitconfig`
     Windows: `C:\ProgramData\Git\config`
   - `git config --system user.name "Your Name"`

2. `--global`

   - Applies to the current user.
   - Linux/macOS: `~/.gitconfig`
     Windows: `C:\Users\<Username>\.gitconfig`
   - `git config --global user.email "your.email@example.com"`

3. `--local`
   - Applies only to a specific Git repository.
   - `<repo>/.git/config`
   - `git config --local core.editor "vim"`

- Precedence Order

  **local > global > system**

- View Configuration
  `git config --list --show-origin`

- Common Settings

  ```bash
  git config --global user.name "Jane Doe"
  git config --global user.email "jane@example.com"
  git config --global core.editor "code --wait"
  git config --global merge.tool "meld"
  ```

## FAQ

### Create a New Branch not from HEAD

- Create a new branch starting from a specific commit or tag, instead of the current `HEAD`

1. git log --oneline

   ```bash
   f3e1bcd (HEAD -> master) Add login functionality
   a7c9e2d Fix homepage bug
   9a1b3c2 Add README file
   e2b56ac Initial commit
   ```

2. Create a branch from the Add README file commit:
   `git branch old-readme-version 9a1b3c2`

### Will Committing and Pushing a Broken Shared File Affect Other Branches?

If you commit and push a broken file (e.g. `utils.py`) to your own branch (like `test`), and this file is also used in other branches (like `main` or `dev`), other users are NOT affected as long as:

- You do not merge your branch into the shared branches.
- Other users do not switch to or pull from your branch.

Git branches are isolated by design. Your broken code will remain in your branch unless explicitly shared.

✅ Safe Scenario:

- You pushed broken code to `test`
- No one merges or checks out `test`
  > Other branches like `main` remain unaffected

⚠️ Risk Scenario:

- Someone merges or rebases your `test` branch
- Someone pulls directly from `test`
  > Now they will get the broken file

### Show Git Branch in Terminal Prompt

`vim ~/.bashrc`, and paste this function:

```bash
parse_git_branch() {
     git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}
export PS1="\u@\h \[\e[32m\]\w \[\e[91m\]\$(parse_git_branch)\[\e[00m\]$ "
```

Reload: `source ~/.bashrc`
