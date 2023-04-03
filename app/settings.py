import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        case_sensitive = True

    TOPICS: dict = dict(
        payment=os.getenv("PAYMENT_TOPIC", None),
        guest=os.getenv("GUEST_TOPIC", None),
        reservation=os.getenv("RESERVATION_TOPIC", None)
    )
    KAFKA_BOOTSTRAP_SERVER: str = os.getenv("KAFKA_BOOTSTRAP_SERVER", None)
    KAFKA_SECURITY_PROTOCOL: str = os.getenv("KAFKA_SECURITY_PROTOCOL", None)
    KAFKA_GROUP_ID: str = os.getenv("KAFKA_GROUP_ID", None)
    KAFKA_SASL_MECHANISMS: str = os.getenv("KAFKA_SASL_MECHANISMS", None)
    KAFKA_SASL_USERNAME: str = os.getenv("KAFKA_SASL_USERNAME", None)
    KAFKA_SASL_PASSWORD: str = os.getenv("KAFKA_SASL_PASSWORD", None)
    KAFKA_SESSION_TIMEOUT: str = os.getenv("KAFKA_SESSION_TIMEOUT", "45000")
    KAFKA_SCHEMA_REGISTRY_URL: str = os.getenv("KAFKA_SCHEMA_REGISTRY_URL", None)
    KAFKA_SCHEMA_REGISTRY_USER: str = os.getenv("KAFKA_SCHEMA_REGISTRY_USER", None)
    HEART_BEAT_INTERVAL: int = os.getenv("HEART_BEAT_INTERVAL", 2)
    PING_INTERVAL: int = os.getenv("PING_INTERVAL", 20)


settings = Settings()
