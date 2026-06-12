# Docker

Docker packages applications and their dependencies into portable images and containers. This section focuses on the container lifecycle and common terminal interaction patterns.

## Container Lifecycle

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

  > **docker start** returns to the terminal, but **docker run** will not.

## Terminal Interaction

  ```mermaid
  flowchart LR
      Terminal[Terminal]
      Attached[Attached Session]
      Running((Running Container))

      Terminal -->|docker attach| Attached
      Attached -->|Ctrl+P Ctrl+Q| Terminal

      Running -.->|attached to| Attached
  ```
