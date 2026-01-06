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

> If CMD is not specified, Docker uses the CMD defined in the base image.
> If there is no base image and no CMD, the container will fail to start.

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
