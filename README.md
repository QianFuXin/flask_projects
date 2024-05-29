# flask_projects

一些基于flask的项目

- black

```shell
black app.py models.py routers
```

- pylint

```shell
pylint app.py models.py routers
```

- requirements

```shell
pip freeze > requirements.txt
```

- install requirements

```shell
pip install -r requirements.txt
```

- build docker image

```shell
docker build -t flask_projects_backend .
```
- run docker container

```shell
docker run -it -P --env-flie .env flask_projects_backend
```