import requests
import json

from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry.avro import AvroSerializer

from get_schema import get_schema_from_schema_registry

init_string = 'data: '
source_url = 'https://stream.wikimedia.org/v2/stream/test'
kafka_url = ' '

username=" "
password=" "
schema_registry_url = f"https://{username}:{password}@ "

kafka_topic = 'ais-lab-schema'
schema_registry_subject = f"{kafka_topic}-value"

def delivery_report(errmsg, msg):
    if errmsg is not None:
        print("Delivery failed for Message: {} : {}".format(msg.key(), errmsg))
        return
    print('Message: successfully produced to Topic: {} Partition: [{}] at offset {}'.format(msg.topic(), msg.partition(), msg.offset()))

def avro_producer(source_url, kafka_url, schema_registry_url, schema_registry_subject):
    # schema registry
    sr, latest_version = get_schema_from_schema_registry(schema_registry_url, schema_registry_subject)


    value_avro_serializer = AvroSerializer(schema_registry_client = sr,
                                          schema_str = latest_version.schema.schema_str,
                                          conf={
                                              'auto.register.schemas': False
                                            }
                                          )

    # Kafka Producer
    producer = SerializingProducer({
        'bootstrap.servers': kafka_url,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': ' ',
        'sasl.password': ' ',
        'value.serializer': value_avro_serializer,
        'delivery.timeout.ms': 120000, # set it to 2 mins
        'enable.idempotence': 'true'
    })

    s = requests.Session()

    with s.get(source_url, headers=None, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
                decoded_line = line.decode()
                if decoded_line.find(init_string) >= 0:
                    decoded_line = decoded_line.replace(init_string, "")
                    # convert to json
                    decoded_json = json.loads(decoded_line)

                    try:
                        producer.produce(topic=kafka_topic, value=decoded_json['meta'], on_delivery=delivery_report)

                        events_processed = producer.poll(1)
                        print(f"events_processed: {events_processed}")

                        messages_in_queue = producer.flush(1)
                        print(f"messages_in_queue: {messages_in_queue}")
                    except Exception as e:
                        print(f"Error -> {e}")
                        
avro_producer(source_url, kafka_url, schema_registry_url, schema_registry_subject)
