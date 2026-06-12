## Container-to-Host Communication

### Using `host.docker.internal` (Recommended for Development)

Inside a container, `localhost` always refers to the container itself. Therefore, containers cannot directly access host services via `localhost`.
Docker provides `host.docker.internal`, a special DNS name provided by Docker, as a stable alias that resolves to the
host gateway IP, enabling container-to-host communication.

Common use cases include:

- Accessing a database running on the host
- Calling a locally running API server
- Development and debugging workflows

Example:

```bash
curl http://host.docker.internal:8000
```

```bash
mongodb://host.docker.internal:27017/swfavorites
```

### Using Host IP via docker inspect (Not Recommended)

Another possible approach is retrieving the host or bridge IP address and hardcoding it into container configuration.

```bash
docker inspect CONTAINER_ID # Resulting in an IP such as 172.17.0.1
```

Then used in application configuration:

```bash
mongodb://172.17.0.1:27017/swfavorites
```

- Why This Is Not Recommended:
  - IP addresses are not stable
  - Breaks portability across machines and environments
  - Fragile when network configuration changes
  - Harder to understand and maintain

## Network

```bash
docker network create NETWORK_NAME
docker network ls
docker run -d --network NETWORK_NAME IMAGE_NAME
```

can use other container's name as domain

```bash
docker network create favorite-net
docker run -d --name mongodb-container --network favorite-net mongo # do not need to specify port because container favorites is within the same network
docker run -d --name favorites --network favorite-net -p 3000:3000 favorites-nodes
```

```node
# inside app.js of favorites-nodes
mongoose.connect("mongodb://mongodb-container:27017/swfavorites");
```
