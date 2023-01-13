FROM python:3.10.8

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD uvicorn --host 0.0.0.0 --port 8080 --factory api.api:create_app