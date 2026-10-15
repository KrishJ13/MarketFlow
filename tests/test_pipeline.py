"""One real Kafka/Spark check, running the same scripts as the learner."""

import os
import subprocess
import sys
import uuid

from kafka.admin import KafkaAdminClient, NewTopic
import pytest


@pytest.mark.skipif(os.getenv("RUN_KAFKA_TEST") != "1", reason="Run make verify with Kafka")
def test_pipeline_and_checkpoint_restart(tmp_path):
    topic = f"marketflow.v0.check.{uuid.uuid4().hex}"
    env = dict(os.environ, KAFKA_TOPIC=topic, DATA_DIR=str(tmp_path))
    admin = KafkaAdminClient(bootstrap_servers=env.get("KAFKA_BOOTSTRAP", "kafka:9092"))
    try:
        admin.create_topics([NewTopic(topic, num_partitions=1, replication_factor=1)])
    finally:
        admin.close()

    def run(label, command):
        result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=180)
        (tmp_path / f"{label}.log").write_text(result.stdout + result.stderr)
        assert result.returncode == 0, f"See {tmp_path / (label + '.log')}"
        return result.stdout

    producer = run("producer", [sys.executable, "producer.py"])
    assert producer.count("received event_id=") == 3
    assert "offset=0" in producer and "offset=2" in producer
    inspector = run("inspect", [sys.executable, "inspect_kafka.py"])
    assert "received records=3" in inspector
    stream = ["spark-submit", "--master", "local[1]", "--packages",
              "org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0", "stream.py"]
    assert "processed records=3" in run("stream", stream)
    query = ["spark-submit", "--master", "local[1]", "query.py"]
    output = run("query", query)
    assert "written records=3" in output
    assert "|BTC-USD|2026-10-1512:00:00|2|" in output.replace(" ", "")
    assert "|ETH-USD|2026-10-1512:01:00|1|" in output.replace(" ", "")
    assert "processed records=0" in run("restart", stream)
    assert "written records=3" in run("query-after-restart", query)
    print(f"PASS: 3 synthetic deliveries → 3 Parquet rows; restart stays at 3. Logs: {tmp_path}")
