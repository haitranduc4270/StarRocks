#!/usr/bin/env python3

from kafka import KafkaConsumer
import json

def main():
    # Tạo một consumer, kết nối tới Kafka broker
    consumer = KafkaConsumer(
        'test2',
        bootstrap_servers='192.168.0.112:9092',  # trong Docker thì là redpanda:29092
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print("Đang lắng nghe topic 'test2'...")

    for message in consumer:
        print("Nhận được message:")
        print(message.value)

if __name__ == '__main__':
    main()
