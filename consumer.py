from kafka import KafkaConsumer, KafkaProducer
import json
import time
import uuid
from threading import Thread
from repo import Repo


class Worker:
    def __init__(self):
        # Initialize Kafka consumer
        self.consumer = KafkaConsumer(
            'seller_product_data_tp',
            bootstrap_servers='localhost:9092',
            group_id='worker-group',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            # enable_auto_commit=False,  # Prevent auto-committing to handle shutdown logic
            # auto_offset_reset='earliest'
        )
        self.repo = Repo()

        self.heartbeat_topic = 'worker_heartbeats'
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        # Dynamically generate worker_id
        self.worker_id = str(uuid.uuid4())
        print(f"Worker initialized with ID: {self.worker_id}")

        self.function_map = {} 
        self.running = True

    def run(self, func):
        """Register a task function."""
        self.function_map[func.__name__] = func

    def process_message(self, message):
        """Process a single message from Kafka."""
        try:
            task_data = message.value
            req_id = task_data.get('req_id')
            task_type = task_data.get('task_type')
            args = task_data.get('args', {})

            # Update status to 'Processing'
            self.repo.update_status(req_id, "Processing", task_type=task_type)

            # Check if the task type is registered
            if task_type not in self.function_map:
                self.repo.update_status(req_id, "Failed: Unknown Task", task_type=task_type)
                print(f"Task type '{task_type}' not found in registered functions.")
                return

            # Execute the registered task function with provided arguments
            result = self.function_map[task_type](**args)

            # Update status to 'Completed'
            self.repo.update_status(req_id, "Completed", task_type=task_type, result=json.dumps(result))
            print(f"Task '{task_type}' for request ID '{req_id}' completed successfully. Result: {result}")

        except Exception as e:
            # Handle any exceptions during processing
            req_id = message.value.get('req_id', 'Unknown')
            error_message = str(e)
            self.repo.update_status(req_id, f"Failed: {error_message}", task_type=task_type)
            print(f"Error processing message: {error_message}")

    def start_worker(self):
        """Start consuming messages and processing tasks."""
        print("Worker started and listening for tasks...")
        Thread(target=self.send_heartbeat, daemon=True).start()

        for message in self.consumer:
            if not self.running:  
                break
            try:
                # Process the incoming message
                self.process_message(message)
                self.consumer.commit()

                print("Message Committed\n")

            except Exception as e:
                print(f"Error during message consumption: {e}")


    def send_heartbeat(self):
        """Send periodic heartbeat messages."""
        while self.running:
            try:
                heartbeat_message = {
                    "worker_id": self.worker_id,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "status": "active"
                }
                self.producer.send(self.heartbeat_topic, value=heartbeat_message)
                # print(f"Heartbeat sent by Worker {self.worker_id}.")
            except Exception as e:
                print(f"Error sending heartbeat: {e}")
            time.sleep(10)
    

    def __del__(self):
        """Cleanup MySQL connection on object destruction."""
        if self.repo.conn.is_connected():
            self.repo.cursor.close()
            self.repo.conn.close()
            print("MySQL connection closed.")