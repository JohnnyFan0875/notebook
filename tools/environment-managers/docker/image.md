# Docker Image

A Docker image is an immutable template that packages an application together with its runtime environment, system libraries, and dependencies.
Images are built in layers, cached for efficiency, and used as the blueprint
for creating containers.

## Basic Image Management

```bash
docker images          # List all images available on the local system.
docker rmi <image_id>  # Remove image
```

- use `docker ps -a` to check stopped containers if removal fails

## Build Image (Standard Build)

```bash
docker build .
```

- Build Cache Behavior

  - Build a Docker image using the Dockerfile in the current directory (if using `.`)
  - Docker builds images layer by layer
  - If any layer changes, all subsequent layers are rebuilt
  - Instruction order strongly affects build speed

- Best practices:
  - Place rarely changed steps (system dependencies) earlier
  - Place frequently changed code later

## Build Image with Docker Buildx

Docker Buildx extends the standard docker build command with advanced
capabilities such as multi-platform builds and improved cache handling.

### Create and Use a Buildx Builder

```bash
docker buildx create --name mybuilder --use
docker buildx inspect mybuilder --bootstrap
```

- `create`: create a new builder instance
- `--use`: – set it as the active builder
- `inspect --bootstrap`: initialize and verify the builder

### Build a Multi-Platform Image

The image is not loaded into local Docker by default.  
Typically paired with `--push` to upload to registry (e.g. GitHub)

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myimage:latest \
  .
```

### Build and Load Image Locally

Build and load the image into the local Docker daemon.  
Works only for single-platform builds. Cannot be used with multi-platform output

```bash
docker buildx build \
 --platform linux/amd64 \
 -t myimage:local \
 --load \
 .
```

### Remove a Buildx Builder

```bash
docker buildx rm mybuilder
```
