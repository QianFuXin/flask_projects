# 构建阶段
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt gunicorn
EXPOSE 5000
CMD ["gunicorn","--workers=3","--bind=0.0.0.0:5000","app:app"]