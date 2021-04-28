FROM python:3.9-slim-buster
WORKDIR /app
ENV TZ America/Sao_Paulo
COPY src .
ADD requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN apt -y update && apt -y install tzdata
CMD uvicorn --host 0.0.0.0 --port 5000 --factory entrypoint:create_app
