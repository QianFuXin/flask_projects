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

- flask-migrate

```shell
# 如果是第一次使用或想把migrations删除重新开始，下面三步
flask db init
flask db migrate -m "initial migration"
flask db upgrade
# 如果迁移到新的数据库 下面一步
flask db upgrade
```
### 已经实现的功能
- 数据库
- redis
- 蓝图
- 跨域
- mongo