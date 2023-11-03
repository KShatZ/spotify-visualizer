FROM python:3.9.18-slim

# Prod & Dev Ports (Respectively)
EXPOSE 8000
EXPOSE 5000

SHELL ["/bin/bash", "-c"]

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD source /app/start.sh
