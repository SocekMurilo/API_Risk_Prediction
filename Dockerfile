FROM python:latest

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p models

EXPOSE 5020

CMD ["python", "/app_home/server_postgre.py"]