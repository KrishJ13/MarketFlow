"""Read Kafka records directly to see what the producer stored."""

from kafka import KafkaConsumer

from settings import BOOTSTRAP, TOPIC


def inspect():
    # This reader has no group/bookmark. Each run starts at the beginning.
    consumer = KafkaConsumer(TOPIC, bootstrap_servers=BOOTSTRAP, group_id=None,
                             auto_offset_reset="earliest", enable_auto_commit=False,
                             consumer_timeout_ms=3000)
    count = 0
    try:
        for message in consumer:
            print(f"partition={message.partition} offset={message.offset} "
                  f"value={message.value.decode('utf-8')}")
            count += 1
    finally:
        consumer.close()
    print(f"received records={count}")


if __name__ == "__main__":
    inspect()
