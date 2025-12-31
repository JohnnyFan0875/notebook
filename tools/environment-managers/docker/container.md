# Docker Container

## Brief Introduction

A Docker container is a **runtime instance of a Docker image**.  
It provides an isolated execution environment where applications run withtheir own filesystem, processes, network interfaces, and resource limits.

## Container Management

### List Containers

```bash
docker ps      # List running containers only
docker ps -a   # List all containers
```

### Start Container

```bash
docker start <container_id>
```

Note:

- `docker start` runs a container in `detached` mode by default
- `docker start -ai` starts and attaches a container

### Attach Container

```bash
docker attach <container_id>
```

Note:

- `docker attach` connects the terminal to the existing STDIN/STDOUT/STDERR of the container’s `PID 1 process`
- Commonly used to re-attach to a container started in detached mode (`-d`)
- Multiple terminals can attach to the same container, but they all share the same input and output streams
- Signals (e.g. `Ctrl+C`) may be delivered to PID 1 and can stop the container
- For additional interactive sessions or debugging, prefer `docker exec -it <container_id> <command>`

### Run a container

```bash
docker run -it --name <container_id> <image_id>
```

Common options:

- `-i`: interactive (keep STDIN open)
- `-t`: allocate a pseudo-TTY
- `--name`: assign a custom container name
- `-d`: detached mode
- `--rm`: automatically remove the container when it exits
- `-p`: port mapping (`host_port:container_port`)

Note:

- image will be automatically installed if not exist
- If the image does not exist locally, Docker will pull it automatically
- `docker run` = `docker create` + `docker start` (+ attach by default)

### Log Container

```bash
docker logs <container_id>
```

Note:

- `docker logs` displays output written to the container’s STDOUT and STDERR
- Works for both running and stopped containers
- `-f` print existing log output, and continuously streams new STDOUT/STDERR entries in real time

### Remove container

```bash
docker rm <container_id>
```

Note:

- Remove a **stopped** container
- Use `docker ps -a` to check the container’s status if removal fails

### Copy Files or Folders To / From a Container

```bash
docker cp docker cp /path/on/host <container_id>:/path/in/container
docker cp <container_id>:/path/in/container /path/on/host
```

Notes:

- Works for both running and stopped containers

### Save a container as a new image

```bash
docker commit <container_id> <image_id>
```
