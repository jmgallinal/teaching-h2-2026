FROM python:3.11-alpine

WORKDIR /app

COPY server.py .

RUN pip install websockets

EXPOSE 8080

CMD ["python", "server.py"]
