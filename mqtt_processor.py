import pika
import json
from datetime import datetime
from pymongo import MongoClient
from config import RABBITMQ_HOST, EXCHANGE_NAME, QUEUE_NAME, ROUTING_KEY, MONGO_URI, DB_NAME, COLLECTION_NAME

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

def mqtt_processor():
    def callback(ch, method, properties, body):
        message = json.loads(body)
        message["timestamp"] = datetime.fromisoformat(message["timestamp"])
        collection.insert_one(message)
        print(f"[MQTT Processor] Received and stored: {message}")

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')
    channel.queue_declare(queue=QUEUE_NAME)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=ROUTING_KEY)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    print("[MQTT Processor] Waiting for messages...")
    channel.start_consuming()
