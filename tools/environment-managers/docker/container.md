- List containers

  ```bash
  docker ps    # list all processing containers
  docker ps -a # list all containers
  ```

### List containers

docker ps -a

- `-a`: list all processing containers

- Run a container

  ```bash
  docker run -it --name <container_name> <image_name>
  ```

  - `-i`: interactive (keep STDIN open)
  - `-t`: allocate a pseudo-TTY
  - `--name`: optional custom name for your container
  - `-d`:optional, detach mode
  - `--rm`: automatically remove the container when it exits
  - `-p`: port
  - image will be automatically installed if not exist

- Save container as a new image

  ```bash
  docker commit <container ID> <image name>
  ```