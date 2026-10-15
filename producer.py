"""Send the synthetic JSON trades to Kafka, one record per trade."""

import json
from pathlib import Path
import sys

from kafka import KafkaProducer

from settings import BOOTSTRAP, TOPIC


def publish(path):
    trades = json.loads(Path(path).read_text())
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP)
    try:
        for trade in trades:
            payload = json.dumps(trade).encode("utf-8")
            # Wait for acknowledgement so we know Kafka accepted this delivery.
            result = producer.send(TOPIC, key=trade["product_id"].encode("utf-8"),
                                   value=payload).get(timeout=10)
            print(f"received event_id={trade['event_id']} "
                  f"partition={result.partition} offset={result.offset}", flush=True)
    finally:
        producer.close()


if __name__ == "__main__":
    publish(sys.argv[1] if len(sys.argv) > 1 else "fixtures/trades.json")
