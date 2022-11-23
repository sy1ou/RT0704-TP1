# RT0704-TP1

## Considerations

### Fonctions

- Creation d'une videotheque
  - Parametres
    - Nom du fichier
    - Proprietaire
  - Creation de la liste des films vide
- Suppression d'une videotheque
  - Parametres
    - Nom du fichier
  - Destruction du fichier
- Affichage de l'ensemble des films
- Recherche d'un film
- Ajout d'un film
- Suppression d'un film
- Recherche des films d'un acteur
- Modification d'un film

## Development

```bash
# Build de l'image docker
docker build -t app .

# Start docker compose
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

## Sources

- [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Docker - Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
- [Docker - Compose specification](https://docs.docker.com/compose/compose-file/)
- [Flask's documentation](https://flask.palletsprojects.com/en/2.2.x/)
- [Requests's documentation](https://requests.readthedocs.io/en/latest/api/)
- [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
