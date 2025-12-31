- Container Lifecycle

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

  > **docker start** will return to terminal, but **docker run** will NOT.

- Terminal Interaction

  ```mermaid
  flowchart LR
      Terminal[Terminal]
      Attached[Attached Session]
      Running((Running Container))

      Terminal -->|docker attach| Attached
      Attached -->|Ctrl+P Ctrl+Q| Terminal

      Running -.->|attached to| Attached
  ```