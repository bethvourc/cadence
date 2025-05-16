FROM python:3.10-slim

WORKDIR /app

COPY uploader/ uploader/
COPY consumer/ consumer/
COPY processor/ processor/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3"]
