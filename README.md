# Proyecto para autentificar usuarios a traves de JWT

## Descripción

El proyecto consiste en una aplicación que utiliza JWT (JSON Web Tokens) para autenticar usuarios. La aplicación tiene un sistema de registro y login, donde los usuarios pueden registrarse y luego iniciar sesión.

El proyecto esta desarrollado con Python sobre el framework FastAPI

## How to run

1. Para ejecutar el proyecto, necesitarás tener instalado Python y pip.

El proyecto fue codificado sobre la version 3.12 de python, en caso de no contar con la version especifica, se puede utilizar este enlace para la instalacion de este mismo.

[Instala Python 3.12](https://ubuntuhandbook.org/index.php/2023/05/install-python-3-12-ubuntu/)

2. Asi mismo es necesario poder crear ambientes virtuales para instalar todas las dependencias necesarias del proyecto, para ello puedes seguir el siguiente enlace.

[Instala virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)

3. Una vez instalado Python 3.12 y virtualenv, puedes crear un ambiente virtual para el proyecto con los siguientes comandos:

```bash
python3.12 -m venv env
source env/bin/activate
```

4. Teniendo el ambiente virtual creado y activo, puedes instalar todas las dependencias necesarias del proyecto con el siguiente comando:

```bash
pip install -r requirements/base.txt
```

5. Es necesario crear un archivo .env con las variables de entorno para que el proyecto funcione de manera correcta, las variables de entorno necesarias son las siguientes

SECRET_KEY="your_secret_key"
ALGORITHM="HS256"
EXPIRE_TIME= time for the token duration in minutes
DATABASE_URL="sqlite:///./your_db.db"

6. Una vez instaladas todas las dependencias y generado el archivo .env, puedes ejecutar el proyecto con el siguiente comando:

```bash
fastapi dev src/main.py
```

Esto creara un servidor en el cual puedes acceder a la aplicacion. De manera predeterminada, el servidor se ejecuta en el puerto 8000, por lo que puedes ingresar al siguiente enlace [localhost](http://127.0.0.1:8000/) en donde encontraras el inicio por default del proyecto o bien puedes ingresar a la [documentacion](http://127.0.0.1:8000/docs) para poder ejecutar y revisar cada una de las API's contenidas dentro del proyecto.


