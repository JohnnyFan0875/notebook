# Docker

## Container Operations

- Run a container

  ```bash
  docker run -it --name <container_name> <image_name>
  ```

  - `-i`: interactive (keep STDIN open)
  - `-t`: allocate a pseudo-TTY
  - `--name`: optional custom name for your container
  - `-d`: optional, detach mode
  - `--rm`: automatically remove the container when it exits

- Other operations

  ```bash
  # Save a container as a new image
  docker commit <container ID> <image name>

  # Attach to a running container
  docker attach <container ID>

  # Attach to an exited container
  docker start -i <container ID>

  # Stop a running container
  docker stop <container ID or name>

  # Detach from a container
  docker run -it -d <image name> # Run container in background mode
  Ctrl + P, Ctrl + Q # Detach from inside the container
  ```

## Build with Docker Buildx

Docker Buildx extends the standard `docker build` command with advanced features, including multi-platform builds and build cache management.

- **Enable buildx** (usually included in modern Docker):

  ```bash
  docker buildx version
  ```

- **Create and use a new builder instance**:

  ```bash
  docker buildx create --name mybuilder --use
  docker buildx inspect mybuilder --bootstrap
  ```

- **Build an image for multiple platforms**:

  ```bash
  docker buildx build --platform linux/amd64,linux/arm64 \
    -t myimage:latest .
  ```

- **Push directly to registry**:

  ```bash
  docker buildx build --platform linux/amd64,linux/arm64 \
    -t myrepo/myimage:latest --push .
  ```

- **Load built image into local Docker** (works only for single-platform builds):

  ```bash
  docker buildx build --platform linux/amd64 -t myimage:local --load .
  ```

- **Remove buildx builder**:

  ```bash
  docker buildx rm mybuilder
  ```

## Other

### Clean Up & Manage Images

- `Dangling image`: an image that is not tagged and not referenced by any container.

```bash
# Show dangling images
docker images --filter "dangling=true"

# Remove dangling images
docker image prune -f
docker image prune --filter "dangling=true"
```

### Remove Build Cache

```bash
docker builder prune --verbose
```

### Check Docker Disk Usage

```bash
docker system df
```
