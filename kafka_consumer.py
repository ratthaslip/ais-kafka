#!/usr/bin/env python3

import sys
from random import choice
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Producer, Consumer

config = {'bootstrap.servers': '13.250.22.xxx:9092',
            'group.id': 'confluent_kafka_group',
            'default.topic.config': {
                'auto.offset.reset': 'smallest',
                'offset.store.sync.interval.ms': 5000
                }
        }

# Create Consumer instance
consumer = Consumer(config)


# Subscribe to topic
topic = "purchases"
consumer.subscribe([topic])

# Poll for new messages from Kafka and print them.
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            # Initial message consumption may take up to
            # `session.timeout.ms` for the consumer group to
            # rebalance and start consuming
            print("Waiting...")
        elif msg.error():
            print("ERROR: %s".format(msg.error()))
        else:
            # Extract the (optional) key and value, and print.

            print("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
    
except KeyboardInterrupt:
    pass
finally:
    # Leave group and commit final offsets
    consumer.close()
