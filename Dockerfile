FROM python:3.9

COPY ./ /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p models

EXPOSE 5020

CMD ["python", "app_home/server_postgre.py"]