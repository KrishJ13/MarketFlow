"""Turn one Kafka value into typed trade columns; keep invalid deliveries visible."""

from pyspark.sql import functions as F

# JSON numeric/time fields arrive as strings. Convert them explicitly below.
SCHEMA = "event_id STRING, product_id STRING, price STRING, size STRING, event_time STRING"


def parse_trades(records):
    trades = records.select(
        "partition", "offset", F.col("value").cast("string").alias("raw_json"))
    trades = trades.withColumn("trade", F.from_json("raw_json", SCHEMA))
    trades = trades.select("partition", "offset", "raw_json", "trade.*")
    trades = (trades.withColumn("price", F.col("price").try_cast("decimal(20,8)"))
              .withColumn("size", F.col("size").try_cast("decimal(20,8)"))
              .withColumn("event_time", F.try_to_timestamp("event_time")))
    # One basic schema check: missing/unparseable required values are invalid.
    valid = (F.col("event_id").isNotNull() & F.col("product_id").isNotNull()
             & F.col("price").isNotNull() & F.col("size").isNotNull()
             & F.col("event_time").isNotNull())
    return trades.withColumn("schema_valid", valid)
