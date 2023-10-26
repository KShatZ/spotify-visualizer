FROM python:3-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

CMD ["python3", "app.py"]
# ENTRYPOINT ["tail", "-f", "/dev/null"] # -- Keep container running