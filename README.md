# APLICACIÓN IMAGE KIT -IMAGA

Aplicación que permite utilizar las APIS de IMAGEKIT e IMAGGA y guardar información de imágenes en una
BBDD mysql

## APLICACIÓN

Será necesario proporcionar un fichero .env con el siguiente contenido:

### CLAVES DE IMAGEKIT
IMAGEKIT_PUBLIC_KEY=
IMAGEKIT_PRIVATE_KEY=
IMAGEKIT_ENDPOINT=


### CLAVES DE IMAGEKIT
IMAGGA_API_KEY=
IMAGGA_API_SECRET= 


### CLAVES BBDD
MY_SQL_HOST=  (mysql cuando se lance con waitress y localhost cuando se lance con flask)
MY_SQL_USER=
MY_SQL_PASSWORD=


Para inicializar la aplicación:

1. Inicializar Docker
2. Lanzar Docker Compose:
    docker system prune --volumes (OPCIONAL: para evitar problemas en el build, ver detalle error de contexto)
    docker-compose up --build

    Segunda opción si la primera diera problemas:
    docker compose build --no-cache
    docker-compose uo



NOTA: Si docker compose da error de contexto, será necesario realizar las siguientes acciones:

Make sure .dockerignore is placed in the same directory as the Dockerfile
Delete all existing containers, volumes, etc.
$ docker system prune --volumes
Build the docker container(s) from the beginning like below
$ (Run your necessary commands)
$ docker compose build --no-cache
$ docker compose up -d
$ docker ps


NOTA: las imágenes se guardan en la carpeta denomidada app/Imagenes