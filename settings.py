"""The few values that connect the scripts to the same Kafka topic and files."""

import os
from pathlib import Path

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "marketflow.v0.trades")
DATA = Path(os.getenv("DATA_DIR", "data"))
TRADES = DATA / "trades"
CHECKPOINT = DATA / "checkpoint"
