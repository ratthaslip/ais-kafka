from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry import Schema

from stream_schema import SCHEMA_STR


schema_registry_url = 'http://13.212.25.xxx:8081'
kafka_topic = 'ais-lab'
schema_registry_subject = f"{kafka_topic}-value"

username=" "
password=" "
schema_registry_url = f"https://{username}:{password}@ "

def register_schema(schema_registry_url, schema_registry_subject, schema_str):
    sr = SchemaRegistryClient({'url': schema_registry_url})
    schema = Schema(schema_str, schema_type="AVRO")
    schema_id = sr.register_schema(subject_name=schema_registry_subject, schema=schema)

    return schema_id

# def update_schema(schema_registry_url, schema_registry_subject, schema_str):
#     sr = SchemaRegistryClient({'url': schema_registry_url})
#     versions_deleted_list = sr.delete_subject(schema_registry_subject)
#     print(f"versions of schema deleted list: {versions_deleted_list}")

#     schema_id = register_schema(schema_registry_url, schema_registry_subject, schema_str)
#     return schema_id

schema_id = register_schema(schema_registry_url, schema_registry_subject, SCHEMA_STR)
print(schema_id)
