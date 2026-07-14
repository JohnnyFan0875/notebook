# Docker Compose

## Brief Introduction

Docker Compose defines multi-container applications in a `compose.yaml` file.
It is useful when an application needs several services, such as an API, database, and cache, started with consistent networking and configuration.

## Basic Structure

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: example

volumes:
  pgdata:

networks:
  default:
```

Notes:

- `services` defines the containers that belong to the application
- `volumes` defines reusable named volumes
- `networks` defines shared networks for service-to-service communication

## Start and Stop an Application

```bash
docker compose up
docker compose up -d
docker compose down
```

Notes:

- `up` creates and starts the application resources
- `-d` runs the application in detached mode
- `down` stops and removes the application resources created by Compose

## Common Service Configuration

### Ports

```yaml
services:
  app:
    ports:
      - "3000:3000"
```

- Maps `host_port:container_port`

### Volumes

```yaml
services:
  db:
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

- Useful for persisting database or application data

### Networks

```yaml
services:
  app:
    networks:
      - backend
  db:
    networks:
      - backend

networks:
  backend:
```

- Services on the same Compose network can usually reach each other by service name

### Dependencies

```yaml
services:
  app:
    depends_on:
      - db
```

Notes:

- `depends_on` controls startup ordering between services
- It does not guarantee that the dependency is fully ready to accept traffic

## Inspect Running Compose Applications

```bash
docker compose ls
docker compose logs
docker compose logs app
docker compose top
```

Notes:

- `logs` aggregates output across services
- `top` shows processes running inside the Compose-managed containers
