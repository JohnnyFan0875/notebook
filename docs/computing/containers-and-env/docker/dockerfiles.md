# Dockerfile

## Brief Introduction

A Dockerfile defines how a Docker image is built. It contains a sequence of instructions that describe:

- which base image to use
- how files are copied into the image
- how dependencies are installed
- how the container starts at runtime

## Basic Dockerfile Example

```dockerfile
FROM <image>

WORKDIR /app
# The directory inside the image will be created if it does not exist

COPY . /app
# The destination directory inside the image will be created if it does not exist

RUN npm install

EXPOSE 80

CMD ["node", "server.js"]
```

Notes

- EXPOSE is purely `documentation`/`metadata` and does not connect, open, or bind any port, either at build time or runtime.

- RUN

  - Executed at build time
  - Creates a new image layer

- CMD

  - Executed at container runtime
  - Defines the default command for the container

- Dockerfile instructions usually create image layers by changing the image filesystem or metadata
- Build cache is matched instruction by instruction, so changing one layer typically invalidates the cache for the layers after it

> If CMD is not specified, Docker uses the CMD defined in the base image.
> If there is no base image and no CMD, the container will fail to start.

## Layering and Cache-Aware Ordering

- Put rarely changing steps earlier, such as installing OS packages
- Put frequently changing steps later, such as copying application source code
- Combine related download, extract, and cleanup work into a single `RUN` instruction when the intermediate files are not needed later

```dockerfile
RUN curl -L https://example.com/archive.zip -o /tmp/archive.zip \
    && unzip /tmp/archive.zip -d /opt/app \
    && rm /tmp/archive.zip
```

This pattern keeps temporary files out of later image layers and helps reduce final image size.

## Multi-stage Builds

Multi-stage builds keep the final image small by separating build tools from runtime artifacts.

```dockerfile
FROM golang:1.22 AS build
WORKDIR /src
COPY . .
RUN go build -o /final/app ./cmd/app

FROM debian:bookworm-slim
COPY --from=build /final/app /usr/local/bin/app
CMD ["app"]
```

Notes:

- Each `FROM` starts a new build stage
- `COPY --from=<stage>` copies artifacts from an earlier stage into the final image
- Build dependencies can stay in the build stage and never reach the runtime image
- This reduces image size and attack surface

## WORKDIR and USER

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN useradd --create-home appuser
USER appuser

CMD ["python", "main.py"]
```

Notes:

- `WORKDIR` sets the default working directory for the following `RUN`, `COPY`, `ADD`, `CMD`, and `ENTRYPOINT` behavior
- If the directory does not exist yet, Docker creates it
- Overriding the container command at `docker run` time still starts from the configured `WORKDIR`
- `USER` changes the user for subsequent build steps and for the container's default runtime user
- A common pattern is to do privileged setup first as `root`, then switch to a less-privileged user near the end of the Dockerfile

## Environment/Build-time Variables with ENV/ARG

### Dockerfile

```dockerfile
# Build-time argument (usable in FROM)
ARG VERSION=3.19
FROM alpine:${VERSION}

# Re-declare ARG if needed after FROM
ARG VERSION

# Runtime environment variables
ENV APP_VERSION=${VERSION} \
    APP_ENV=production \
    APP_PORT=8080 \
    LOG_LEVEL=info

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE $APP_PORT

CMD ["/entrypoint.sh"]
```

### Bash Script Example: entrypoint.sh

```bash
#!/usr/bin/env sh

echo "Application environment : $APP_ENV"
echo "Listening port          : $APP_PORT"
echo "Log level               : $LOG_LEVEL"
```

Notes:

- Shell scripts automatically inherit Docker environment variables
- No additional configuration is required
- for python script, use `os.getenv`

> ARG must be declared again after `FROM` to be accessible.

### Build Image

```bash
docker build --build-arg VERSION=4.2 -t myimage . # Override ARG at Buildtime
```

### Run container

```bash
docker run myimage
docker run -p 3000:8080 -e APP_VERSION=4.3 myimage # Override ENV at Runtime
docker run -p 3000:8081 -e APP_PORT=8081 myimage
```

Using `.env` file

```text
PORT=8000
```

```bash
docker run -p 3000:8000 --env-file .env myimage
```

### Comparison Table

| Feature                  | ARG         | ENV               |
| ------------------------ | ----------- | ----------------- |
| Available at build time  | Yes         | Yes               |
| Available at runtime     | No          | Yes               |
| Visible inside container | No          | Yes               |
| Overridable at runtime   | No          | Yes (`-e`)        |
| Stored in image metadata | No          | Yes               |
| Used for                 | Build logic | App configuration |
