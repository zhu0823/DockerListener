FROM python:3.10
LABEL authors="zhu0823"

ENV TZ="Asia/Shanghai"
ENV UID=0
ENV GID=0
ENV UMASK=0

# 创建应用程序用户
RUN groupadd -g $GID appuser && \
    useradd -m -u $UID -g $GID -s /bin/bash appuser \

# 设置工作目录并更改权限
WORKDIR /app
RUN chown -R appuser:appuser /app && \
    chmod 755 /app

# 切换到应用程序用户
USER appuser

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8010

VOLUME ["/config", "/scripts"]

CMD ["python", "main.py"]