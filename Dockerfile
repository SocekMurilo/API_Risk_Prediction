FROM python:latest

WORKDIR /app/app_home

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p models

EXPOSE 5020

CMD ["python", "server_postgre.py"]