import sys
import time
import json
import os
import threading
import pandas as pd
from kafka import KafkaProducer

# Config
BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC_MAPPING = {
    'D:\starrocks\data\customer.csv': 'customer',
    'D:\\starrocks\\data\\product.csv': 'product',
    'D:/starrocks/data/transactions.csv': 'transaction',
    'D:\starrocks\data\click_stream.csv': 'click_stream'
}

def get_producer():
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def stream_file_to_kafka(producer, file_path, topic):
    print(f"[{topic}] Streaming from {file_path}")

    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path, on_bad_lines='skip')
    elif file_path.endswith('.json'):
        df = pd.read_json(file_path, lines=True)
    else:
        print(f"[{topic}] Unsupported format: {file_path}")
        return

    for _, row in df.iterrows():
        try:
            data = row.to_dict()
            producer.send(topic, value=data)
            print(file_path, data)
            time.sleep(0.1)  # Giả lập thời gian gửi
        except Exception as e:
            print(f"[{topic}] Error sending record: {e}")
    
    print(f"[{topic}] ✅ Done streaming.")

def main():
    producer = get_producer()
    threads = []

    for name, topic in TOPIC_MAPPING.items():
        file_path = name
        if os.path.exists(file_path):
            t = threading.Thread(target=stream_file_to_kafka, args=(producer, file_path, topic))
            t.start()
            threads.append(t)
        else:
            print(f"[{topic}] ❌ File not found: {file_path}")

    # Chờ tất cả thread kết thúc
    for t in threads:
        t.join()

    print("🎉 All files streamed in parallel.")

if __name__ == '__main__':
    main()


