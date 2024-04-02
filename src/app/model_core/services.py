import os
from confluent_kafka import Consumer, KafkaError
import json

from app.utils.logger import make_log
from app.dashboard.models import User
from .models import Queue


def get_consumer() -> Consumer:
    consumer = Consumer(
        {
            "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVER"),
            "group.id": os.getenv("KAFKA_GROUP_ID"),
            "auto.offset.reset": "earliest",
        }
    )

    consumer.subscribe(os.getenv("MODEL_QUEUE_TRAIN_TOPIC"))
    return consumer


def service_loop():
    consumer = get_consumer()

    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                make_log("KAFKA_MODEL", 30, "kafka_models.log", msg.error())
                break
        data = json.loads(msg.value().decode("utf-8"))
        user = data["user"]
        asset_id = data["asset"]
        model_type_id = data["model"]
        priority = User.objects.get(username=user).priority

        Queue.objects.create(
            user=user, asset_id=asset_id, model_type_id=model_type_id, priority=priority
        )

    consumer.close()


def delivery_callback(err, msg):
    if err:
        make_log(
            "KAFKA_MODEL",
            30,
            "kafka_models.log",
            f"ERROR: Message delivery failed: {err}",
        )
    else:
        make_log(
            "KAFKA_MODEL",
            20,
            "kafka_models.log",
            f"Produced event to topic {msg.topic()}, key = {msg.key().decode('utf-8')}, value = {msg.value().decode('utf-8')}",
        )
