# Docker

## Image Operations

- Remove image

docker rmi <image_id>

- List images

docker images

## Container Operations

- List containers

  ```bash
  docker ps    # list all processing containers
  docker ps -a # list all containers
  ```

- Run a container

  ```bash
  docker run -it --name <container_name> <image_name>
  ```

  - `-i`: interactive (keep STDIN open)
  - `-t`: allocate a pseudo-TTY
  - `--name`: optional custom name for your container
  - `-d`:optional, detach mode
  - `--rm`: automatically remove the container when it exits
  - `-p`: port
  - image will be automatically installed if not exist

- Container Lifecycle

  ```mermaid
  flowchart LR
      Image[Image]
      Created((Created))
      Running((Running))
      Paused((Paused))
      Stopped((Stopped))
      Deleted((Deleted))

      %% lifecycle
      Image -->|docker create| Created
      Created -->|docker start| Running
      Running -->|docker pause| Paused
      Paused -->|docker unpause| Running
      Running -->|docker stop| Stopped
      Stopped -->|docker start| Running
      Created -->|docker rm| Deleted
      Stopped -->|docker rm| Deleted

      %% annotation
      Image -.->|docker run = create + start + attach session| Running
  ```

  > **docker start** will return to terminal, but **docker run** will NOT.

- Terminal Interaction

  ```mermaid
  flowchart LR
      Terminal[Terminal]
      Attached[Attached Session]
      Running((Running Container))

      Terminal -->|docker attach| Attached
      Attached -->|Ctrl+P Ctrl+Q| Terminal

      Running -.->|attached to| Attached
  ```

- Other operations

  ```bash
  # Save a container as a new image
  docker commit <container ID> <image name>

  # Attach to an exited container
  docker start -i <container ID>

  # Stop a running container
  docker stop <container ID or name>

  # Detach from a container
  docker run -it -d <image name> # Run container in background mode
  Ctrl + P, Ctrl + Q # Detach from inside the container
  ```

## Build customized image

docker build .

- if any layer is changed and re-built, all the subsequent layer will be executed again

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

### List containers

docker ps -a

- `-a`: list all processing containers

### Dockerfile

```dockerfile
FROM <image>

WORKDIR /app # the folder in image will be created if not exists

COPY . /app # the destination folder in image will be created if not exists

RUN npm install

EXPOSE 80

CMD ["node", "server.js"]
```

- `RUN` is executed at build time and creates image layers.  
   `CMD` is executed at container run time and defines the default command.

> if `CMD` not specified, CMD of base image will be executed. With no base image and no CMD, you'got an error.
