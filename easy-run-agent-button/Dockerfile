# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

COPY . ./

WORKDIR ./easy-run-agent-button

RUN pip install -r requirements.txt

CMD [ "python", "main.py"]