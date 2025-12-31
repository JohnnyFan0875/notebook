# Docker Image

A Docker image is an immutable template that packages an application together with its runtime environment, system libraries, and dependencies.
Images are built in layers, cached for efficiency, and used as the blueprint
for creating containers.

## Basic Image Management

```bash
docker images          # List all images available on the local system.
```

## Remove Images

```bash
docker rmi <image_id>  # Remove image
docker image prune     # Remove dangling (untagged) images
docker image prune -a  # Remove all images not referenced by any container
```

- Images referenced by **running** or **stopped** containers cannot be removed
- Use docker `ps -a` to check for stopped containers if image removal fails
- Remove containers first, or use `docker container prune`, before pruning images

## Tag Images

```bash
docker tag <source_image>:<source_tag> <target_image>:<target_tag>
```

Note:

- `docker tag` creates a new reference (tag) pointing to the same image
- The original image and its tag are not modified or overwritten

## Push / Pull Images

```bash
docker push <repository>:<tag>   # Push an image to a container registry
docker pull <repository>:<tag>   # Pull an image from a container registry
```

Notes:

- Tags are required to uniquely identify image versions

## Build Image (Standard Build)

```bash
docker build .
```

Note:

- `-t`: Name and optionally a tag (format: "name:tag")

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
