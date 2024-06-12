# flask_projects

一些基于flask的项目

- black

```shell
black app.py
```

- pylint

```shell
pylint app.py
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
docker build -t flask_projects_flask_admin .
```
- run docker container

```shell
docker run -it -P flask_projects_flask_admin
```