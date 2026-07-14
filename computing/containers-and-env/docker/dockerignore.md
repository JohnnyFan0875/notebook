# .dockerignore

## Brief Introduction

`.dockerignore` is used to exclude files and directories from the Docker build context.
It works similarly to `.gitignore`, but applies **only during `docker build`**.

Using `.dockerignore` helps to:

- Reduce build context size
- Improve build performance
- Avoid leaking sensitive or unnecessary files into images

## How Docker Build Context Works

When running:

```bash
docker build .
```

Docker sends the entire build context (current directory) to the Docker daemon, except files excluded by .dockerignore

## Basic Syntax

```text
node_modules
.git
.gitignore
Dockerfile
*.log
.env
```
