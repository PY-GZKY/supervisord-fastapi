FROM python:3.7-alpine as base

WORKDIR /app
COPY process-manager-api .

RUN pip3 install -r requirements.txt
RUN apk add tzdata

ENV LOGURU_LEVEL SUCCESS
EXPOSE 5000

CMD python3 run.py
