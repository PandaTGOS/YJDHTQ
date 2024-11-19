from kafka import KafkaProducer
import json

class KafkaProducerWrapper:
    def __init__(self, kafka_server='localhost:9092', topic='seller_product_data_tp'):
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=[kafka_server],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def produce(self, key, value):
        self.producer.send(
            self.topic, key=key.encode('utf-8'), value=value
        )
        self.producer.flush()
