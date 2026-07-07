# Containerization and Virtualization

## Core Definitions

- Virtualization abstracts hardware resources so one physical machine can host multiple isolated virtual machines.
- A virtual machine (VM) behaves like a complete computer system with its own guest operating system.
- Containerization is OS-level virtualization: applications run in isolated user spaces while sharing the host kernel.
- A container packages an application together with the libraries and dependencies it needs to run consistently.

## Virtual Machines

Typical VM stack:

- Host machine
- Hypervisor or virtualization layer
- Multiple guest operating systems
- Applications running inside each guest OS

Characteristics:

- Strong isolation because each VM has its own operating system
- Flexible when different guest operating systems are required on the same host
- Higher overhead because every VM includes a full OS

## Containers

Typical container stack:

- Host machine
- Host operating system and kernel
- Container runtime
- Multiple isolated containers

Characteristics:

- Lightweight compared with VMs because containers share the host kernel
- Fast to start and stop
- Well suited for running multiple applications on the same host in reproducible environments

## Virtualization vs. Containerization

| Aspect | Virtual Machine | Container |
| --- | --- | --- |
| Isolation boundary | Full guest OS | Process and filesystem isolation on shared kernel |
| Operating system | Each VM has its own OS | Shares host kernel |
| Resource overhead | Higher | Lower |
| Startup speed | Slower | Faster |
| Common use case | Mixed OS workloads, stronger isolation | Application packaging and deployment |

## Docker and Containerization

- Docker is a widely used tool for building, shipping, and running containers.
- Docker images package application code and dependencies.
- Docker containers are running instances created from those images.
- Dockerfiles describe how an image is built in a reproducible way.

## Container Orchestration

Container orchestration manages containers across multiple machines or services.

Common orchestration concerns:

- Scheduling containers onto available compute resources
- Scaling application replicas up and down
- Restarting failed workloads
- Rolling out updates in a controlled way
- Managing service discovery and networking between containers

## Kubernetes in the Stack

- Kubernetes is a popular container orchestration platform.
- Docker helps package and run containers.
- Kubernetes helps coordinate many containers in production-like environments.

Use Docker when the main goal is packaging and local execution.
Use Kubernetes when the main goal is operating groups of containers reliably at scale.
