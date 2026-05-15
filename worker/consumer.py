from kafka import KafkaConsumer
import json
import time
import resend
import os


resend.api_key = os.getenv("RESEND_API_KEY")

def send_confirmation_email(to_email: str, task_title: str):
    resend.Emails.send({
        "from": "noreply@apitodo.com",
        "to": to_email,
        "subject": f"Task criada: {task_title}",
        "html": f"<h2>{task_title} criada com sucesso!</h2>"
    })


while True:
    try:
        consumer = KafkaConsumer(
            "tasks",
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="task-group-2"
        )

        break

    except Exception as e:
        time.sleep(5)

for message in consumer:
    event = message.value

    if event["event"] == "task_created":
        send_confirmation_email(event["email"], event["title"])
