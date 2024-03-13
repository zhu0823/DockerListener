FROM python:3.10
LABEL authors="zhu0823"

WORKDIR /app

COPY ../DockerListener /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8010

VOLUME ["/config", "/scripts"]

CMD ["python", "main.py"]