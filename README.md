# flask_projects

实现jwt的token发布和验证

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
docker build -t flask_projects_token .
```
- run docker container

```shell
docker run -it -P flask_projects_token
```