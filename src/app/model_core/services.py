import os
from confluent_kafka import Consumer, KafkaError, KafkaException
import json

from app.utils.logger import make_log
from app.dashboard.models import User
from .models import Queue


def get_consumer():
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
    try:
        with get_consumer() as consumer:
            while True:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        make_log(
                            "KAFKA",
                            40,
                            "models_workflow.log",
                            f"Kafka consumer error: {msg.error()}",
                        )
                        break
                try:
                    data = json.loads(msg.value().decode("utf-8"))
                    user_id = data["user"]
                    asset_id = data["asset"]
                    model_type_id = data["model"]
                except json.JSONDecodeError:
                    make_log(
                        "KAFKA",
                        40,
                        "models_workflow.log",
                        "Error decoding JSON request data",
                    )
                    continue

                priority = User.objects.get(id=user_id).priority

                try:
                    Queue.objects.create(
                        user=user_id,
                        asset_id=asset_id,
                        model_type_id=model_type_id,
                        priority=priority,
                    )
                except Exception as e:
                    make_log(
                        "DB",
                        40,
                        "models_workflow.log",
                        f"Error creating Queue object: {str(e)}",
                    )
                    continue
            consumer.close()
    except (
        KafkaException
    ) as ke:  # Propagate this error to the caller whenever I implement it
        make_log(
            "KAFKA",
            40,
            "models_workflow.log",
            f"Error getting Kafka consumer: {str(ke.args[0])}",
        )


def delivery_callback(err, msg):
    if err:
        make_log(
            "KAFKA_MODEL",
            40,
            "kafka_workflow.log",
            f"ERROR: Message delivery failed: {err}",
        )
    else:
        make_log(
            "KAFKA_MODEL",
            20,
            "kafka_workflow.log",
            f"Produced event to topic {msg.topic()}, key = {msg.key().decode('utf-8')}, value = {msg.value().decode('utf-8')}",
        )
