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