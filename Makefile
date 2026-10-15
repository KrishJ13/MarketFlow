# Each target exposes one script. Use `make -n <target>` to see the actual command.
SPARK = spark-submit --master local[1]
CONNECTOR = org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0

.PHONY: build up produce inspect stream query test verify stop
build:
	docker compose build tools
up:
	docker compose up -d --wait kafka
produce: up
	docker compose run --rm tools python producer.py
inspect: up
	docker compose run --rm tools python inspect_kafka.py
stream: up
	docker compose run --rm tools $(SPARK) --packages $(CONNECTOR) stream.py
query:
	docker compose run --rm --no-deps tools $(SPARK) query.py
test:
	docker compose run --rm --no-deps tools python -m pytest tests/test_transform.py -q -p no:cacheprovider
verify: up
	docker compose run --rm -e RUN_KAFKA_TEST=1 tools python -m pytest tests/test_pipeline.py -v -s -p no:cacheprovider --basetemp=data/verification-$$(date -u +%Y%m%dT%H%M%SZ)
stop:
	docker compose stop
