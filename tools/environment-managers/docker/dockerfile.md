### Dockerfile

```dockerfile
FROM <image>

WORKDIR /app # the folder in image will be created if not exists

COPY . /app # the destination folder in image will be created if not exists

RUN npm install

EXPOSE 80

CMD ["node", "server.js"]
```

- `RUN` is executed at build time and creates image layers.  
   `CMD` is executed at container run time and defines the default command.

> if `CMD` not specified, CMD of base image will be executed. With no base image and no CMD, you'got an error.