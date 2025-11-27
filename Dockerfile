FROM python:3.11.9

COPY ./ ./

RUN  pip install -r requirements.txt && docker-compose up --build

