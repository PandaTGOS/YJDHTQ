from kafka import KafkaConsumer
import json
import time
import threading

def monitor_heartbeats(kafka_server='localhost:9092', heartbeat_topic='worker_heartbeats', timeout=10, check_interval=1):
    consumer = KafkaConsumer(
        heartbeat_topic,
        bootstrap_servers=[kafka_server],
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    last_heartbeat = {}

    def check_inactive_workers():
        while True:
            time.sleep(check_interval)
            timestamp = time.time()
            inactive_workers = [
                worker for worker, last_time in last_heartbeat.items()
                if timestamp - last_time > timeout
            ]

            for worker in inactive_workers:
                print(f"Worker: {worker} | Status: INACTIVE | Last Heartbeat: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_heartbeat[worker]))}")
                del last_heartbeat[worker]

    # Start a separate thread for checking inactive workers
    threading.Thread(target=check_inactive_workers, daemon=True).start()

    print(f"Starting heartbeat monitor on topic {heartbeat_topic}...")

    for message in consumer:
        heartbeat = message.value
        worker_id = heartbeat['worker_id']
        timestamp = time.time()

        last_heartbeat[worker_id] = timestamp  
        print(f"Worker: {worker_id} | Status: ACTIVE   | Last Heartbeat: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))}")


if __name__ == "__main__":
    monitor_heartbeats()