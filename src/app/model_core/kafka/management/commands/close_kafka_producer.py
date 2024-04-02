from django.core.management.base import BaseCommand
from app.model_core.kafka.services import KafkaProducerSingleton


class Command(BaseCommand):
    help = "Gracefully shuts down Kafka producer"

    def handle(self, *args, **kwargs):
        kafka_producer = KafkaProducerSingleton()
        kafka_producer.close_producer()
        self.stdout.write(self.style.SUCCESS("Kafka producer closed successfully"))
