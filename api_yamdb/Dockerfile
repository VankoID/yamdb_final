FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN pip3 install -r api_yamdb/requirements.txt --no-cache-dir

CMD ["sh", "run.sh"]

LABEL author='vanoid_relax@yandex.ru' version=1 
