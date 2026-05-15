from kafka import KafkaProducer
import json
import asyncio
from functools import partial
from models.user import User
import os


def get_producer():
    return KafkaProducer(
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )


def _send_sync(task):
    producer = get_producer()

    user = User(id=task.owner_id)
    if user:
        producer.send("tasks", {
            "event": "task_created",
            "id": task.id,
            "title": task.title,
            "email": user.email
        })
        producer.flush()


async def send_task_created_event(task):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, partial(_send_sync, task))
