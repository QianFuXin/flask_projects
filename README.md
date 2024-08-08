# flask_projects

提供音乐资源的API接口
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
docker build -t music_backend .
```
- run docker container

```shell
version: '3'

services:
  music_backend:
    image: music_backend
    ports:
      - "9999:5000"
    volumes:
      - "/root/music_web/static/:/app/static/music/"
    restart: always
```
