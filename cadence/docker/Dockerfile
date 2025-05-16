FROM python:3.10-slim

WORKDIR /app

COPY cadence/uploader/ uploader/
COPY cadence/consumer/ consumer/
COPY cadence/processor/ processor/
COPY cadence/data/ data/
COPY cadence/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3"]
