from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka import Consumer
from app.settings import settings
from app.topics.guests import GuestsTopic
from app.topics.reservations import ReservationsTopic
from app.topics.payments import PaymentsTopic


class Kafka:
    def __init__(self):
        self.schema_registry = self.get_schema_registry()

    @property
    def config(self) -> dict:
        return {
            "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVER,
            "group.id": settings.KAFKA_GROUP_ID,
            "security.protocol": settings.KAFKA_SECURITY_PROTOCOL,
            "sasl.mechanisms": settings.KAFKA_SASL_MECHANISMS,
            "sasl.username": settings.KAFKA_SASL_USERNAME,
            "sasl.password": settings.KAFKA_SASL_PASSWORD,
            "auto.offset.reset": 'latest',
            "session.timeout.ms": settings.KAFKA_SESSION_TIMEOUT,
        }

    @property
    def schema_registry_config(self) -> dict:
        return {
            "url": settings.KAFKA_SCHEMA_REGISTRY_URL,
            "basic.auth.user.info": settings.KAFKA_SCHEMA_REGISTRY_USER,
        }

    def get_schema_registry(self) -> SchemaRegistryClient:
        return SchemaRegistryClient(self.schema_registry_config)

    def deserialize_key(self, topic, message) -> dict:
        key_deserializer = {
            settings.TOPICS["payment"]: AvroDeserializer(self.schema_registry, PaymentsTopic.key_schema()),
            settings.TOPICS["guest"]: AvroDeserializer(self.schema_registry, GuestsTopic.key_schema()),
            settings.TOPICS["reservation"]: AvroDeserializer(self.schema_registry, ReservationsTopic.key_schema())
        }

        return key_deserializer[topic](message.key(), None)

    def deserialize_value(self, topic, message) -> dict:
        key_deserializer = {
            settings.TOPICS["payment"]: AvroDeserializer(self.schema_registry, PaymentsTopic.value_schema()),
            settings.TOPICS["guest"]: AvroDeserializer(self.schema_registry, GuestsTopic.value_schema()),
            settings.TOPICS["reservation"]: AvroDeserializer(self.schema_registry, ReservationsTopic.value_schema())
        }

        return key_deserializer[topic](message.value(), None)

    def get_consumer(self) -> Consumer:
        consumer = Consumer(self.config)

        # Subscribe to topics
        topics = [topic for topic in settings.TOPICS.values()]
        consumer.subscribe(topics)
        return consumer
