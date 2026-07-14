# Docker Volumes and Bind Mounts

## Brief Introduction

Containers are **ephemeral by design**—their filesystem changes are lost when the container is removed.
**Volumes** and **bind mounts** provide mechanisms to **persist data** and **share data** between containers and the host system.

## Bind Mount

```bash
docker run -v /host/path:/container/path IMAGE
```

Description:

- Maps a specific host filesystem path directly into the container
- Changes on the host are immediately visible inside the container

Characteristics:

- Strongly coupled to the host directory structure
- Not managed by Docker
- Commonly used for development and debugging

## Named Volume

```bash
docker run -v mydata:/container/path IMAGE
```

Description:

- Uses a Docker-managed storage location
- The actual host path is abstracted away by Docker

Characteristics:

- Data persists even after the container stops or is removed
- Can be shared across multiple containers
- Recommended for persistent application data (e.g. databases)
- Safer and more portable than bind mounts

## Anonymous Volume

Add in CLI:

```bash
docker run -v /container/path IMAGE
```

Add in dockerfile:

```dockerfile
FROM node:14

WORKDIR /app

COPY . .

VOLUME [ "/app/feedback" ]

CMD [ "node", "server.js" ]
```

Behavior:

- Docker automatically creates a volume with a random name
- The volume is not easily reusable by other containers

Notes:

- Data persists after the container stops
- If the container is started with --rm, the anonymous volume is removed automatically
- If `--rm` is not used, the anonymous volume remains after container removal
- Anonymous volumes are not reused across containers because each has a unique volume reference

Cleanup:

```bash
docker volume rm <volume_name>
docker volume prune
```

## Read-only mount (`:ro`)

All Docker mount types support a read-only option, which prevents containers from modifying mounted data.

```bash
docker run -v SOURCE:TARGET:ro IMAGE
```

## Summary

| Type             | Managed by Docker | Host Path Required | Data Persistence | Typical Use Case           |
| ---------------- | ----------------- | ------------------ | ---------------- | -------------------------- |
| Bind Mount       | ❌                | ✅                 | Yes              | Development, live editing  |
| Named Volume     | ✅                | ❌                 | Yes              | Production data, databases |
| Anonymous Volume | ✅                | ❌                 | Yes\*            | Temporary container data   |

- Removed automatically only when the container is run with `--rm`.

## Other Operations

```bash
docker volume ls
docker volume create VOL_NAME
docker volume rm VOL_NAME
docker volume prune # remove all unused volumes
```
