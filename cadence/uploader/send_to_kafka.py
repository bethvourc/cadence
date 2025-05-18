import os
from kafka import KafkaProducer
import json

KAFKA_TOPIC = "csv_files"
KAFKA_BROKER = "host.minikube.internal:9092"
UPLOAD_DIR = "/app/data/uploads" 

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    api_version=(2, 6),
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_files():
    for filename in os.listdir(UPLOAD_DIR):
        if filename.endswith(".csv"):
            file_path = os.path.join(UPLOAD_DIR, filename)
            message = {
                "file_name": filename,
                "path": file_path
            }
            producer.send(KAFKA_TOPIC, message)
            print(f"[✓] Sent file info to Kafka: {filename}")

if __name__ == "__main__":
    send_files()
