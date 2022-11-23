# RT0704-TP1

## Considerations

### Features

- Creating a video library
  - Parameters
    - Name of the file
    - Owner
  - Creation of the empty film list
- Deleting a library
  - Parameters
    - Name of the file
  - Delete file
- Display of all the films
- Search for a movie
- Add a movie
- Deleting a movie
- Search for films of an actor
- Edit a movie

## Development

```bash
# Build the docker image
docker build -t app .

# Launch docker compose
docker compose up
```

## To do

- [x] créez l'image pour le générateur de pages WEB
  - [x] décrivez l'ensemble des pages WEB ainsi que les interactions avec le gestionnaire de services REST
  - [x] décrivez la configuration système de votre conteneur
- [x] créez l'image pour le gestionnaire de services REST
  - [x] décrivez l'architecture de l'API REST, ainsi que l'ensemble des endpoints et des signatures des services
  - [x] décrivez la configuration système de votre conteneur
- [x] développez l'ensemble des services REST. Vous testerez ces services à l'aide de la commande curl
- [x] développez les pages associés aux services, comme indiqué dans les transparents du cours 7
- [ ] proposez une batterie de test pour présenter votre application

## References

- [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Docker - Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
- [Docker - Compose specification](https://docs.docker.com/compose/compose-file/)
- [Flask's documentation](https://flask.palletsprojects.com/en/2.2.x/)
- [Requests's documentation](https://requests.readthedocs.io/en/latest/api/)
- [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
