# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

COPY . ./

WORKDIR ./easy-run-agent-button

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN /import-agent.sh
