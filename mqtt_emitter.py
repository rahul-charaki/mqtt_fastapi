import pika
import time
import random
import json
from datetime import datetime
from config import RABBITMQ_HOST, EXCHANGE_NAME, ROUTING_KEY

def mqtt_emitter():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

    while True:
        status = random.randint(0, 6)
        message = {
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=ROUTING_KEY,
            body=json.dumps(message)
        )
        print(f"[MQTT Emitter] Sent: {message}")
        time.sleep(1)
