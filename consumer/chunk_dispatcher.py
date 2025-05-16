import os
import pandas as pd
from kafka import KafkaConsumer, KafkaProducer
import json
from pathlib import Path

KAFKA_BROKER = "localhost:9092"
CONSUME_TOPIC = "csv_files"
PRODUCE_TOPIC = "csv_chunks"
CHUNK_SIZE = 10000  # rows per chunk
CHUNK_DIR = "data/chunks"

# Setup Kafka
consumer = KafkaConsumer(
    CONSUME_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

Path(CHUNK_DIR).mkdir(parents=True, exist_ok=True)

def chunk_csv(file_path, file_name):
    print(f"🔧 Chunking {file_path}")
    try:
        for i, chunk in enumerate(pd.read_csv(file_path, chunksize=CHUNK_SIZE)):
            chunk_file_name = f"{file_name}_chunk_{i}.csv"
            chunk_path = os.path.join(CHUNK_DIR, chunk_file_name)
            chunk.to_csv(chunk_path, index=False)
            print(f"Created: {chunk_path}")

            # publish chunk info
            producer.send(PRODUCE_TOPIC, {
                "original_file": file_name,
                "chunk_file": chunk_path,
                "chunk_index": i
            })
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def consume():
    print("Listening for CSV file messages...")
    for msg in consumer:
        data = msg.value
        file_path = data["path"]
        file_name = data["file_name"]
        chunk_csv(file_path, file_name)

if __name__ == "__main__":
    consume()
