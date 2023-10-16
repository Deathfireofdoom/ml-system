from abc import ABC, abstractmethod
import json


class BasePubSubClient(ABC):
    @abstractmethod
    def publish(self, topic: str, message: str):
        pass


class RedisPubSubClient(BasePubSubClient):
    def __init__(self, host: str, port: str) -> None:
        import redis

        self.client = redis.Redis(host=host, port=port, db=0)

    def publish(self, topic: str, message: dict):
        self.client.publish(topic, json.dumps(message))


def get_redis_client():
    from app.utils.env.env import env

    return RedisPubSubClient(env.REDIS_HOST, env.REDIS_PORT)
