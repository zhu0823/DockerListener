FROM python:3.10
LABEL authors="zhu0823"

# 设置工作目录并更改权限
WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y rsync
RUN pip install --no-cache-dir -r requirements.txt

ENV TZ="Asia/Shanghai"
ENV UID=0
ENV GID=0
ENV UMASK=022

EXPOSE 8010

VOLUME ["/config", "/scripts", "/logs"]

CMD ["python", "main.py"]