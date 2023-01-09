FROM python:3.10.8

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT python /app/main.py