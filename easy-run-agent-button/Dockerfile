# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

COPY . ./

WORKDIR ./easy-run-agent-button

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD exec gunicorn --bind :80 --workers 1 --threads 8 --timeout 0 main:app

RUN /import-agent.sh
