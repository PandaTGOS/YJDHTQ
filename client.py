import json
import uuid
from producer import KafkaProducerWrapper
from repo import Repo

class Client:
    def __init__(self):
        self.repo = Repo()
        self.producer = KafkaProducerWrapper()

    def submit_task(self, task_type, args):
        """Submit a task to the distributed queue."""
        task_id = str(uuid.uuid4())
        task_data = {
            "req_id": task_id,
            "task_type": task_type,
            "args": args,
        }

        # Write initial status to DB
        self.repo.write_status(task_id, "queued")

        # Send task to Kafka
        self.producer.produce(task_id, task_data)
        print(f"Task {task_id} submitted for task type '{task_type}'.")
        return task_id