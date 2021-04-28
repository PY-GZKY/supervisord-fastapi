FROM python:3.9-slim-buster
WORKDIR /app
COPY src .
ADD requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
CMD uvicorn --host 0.0.0.0 --port 5000 --factory entrypoint:create_app
