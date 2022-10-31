import os
import redis
import pickle
from models.schemas import AlertInfoSchema
from typing import Any


r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    password=os.getenv("REDIS_PASSWORD"))


def redis_consumer(key: str):

    l = []
    while (r.llen(key)):
        l.append(pickle.loads(r.lpop(key)))
    return l


def redis_producer(data: Any, key: str):
    r.delete(key)
    for d in data:
        r.lpush(key, pickle.dumps(AlertInfoSchema(id=d.PlatformAlert.id,
                                                  username=d.PlatformAlert.username,
                                                  superproduct_ids=d.PlatformAlert.superproduct_ids,
                                                  chain_ids=d.PlatformAlert.chain_ids,
                                                  last_time_notified=d.PlatformAlert.last_time_notified,
                                                  frequency=d.PlatformAlert.frequency,
                                                  threshold=d.PlatformAlert.threshold,
                                                  kpi=d.PlatformAlert.kpi)))
