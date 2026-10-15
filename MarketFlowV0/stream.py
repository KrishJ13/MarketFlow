"""Read the current Kafka backlog, transform it, and append Parquet files."""

from pyspark.sql import SparkSession

from settings import BOOTSTRAP, TOPIC, TRADES, CHECKPOINT
from transform import parse_trades


def main():
    spark = (SparkSession.builder.appName("marketflow-v0-stream")
             .config("spark.sql.session.timeZone", "UTC").getOrCreate())
    spark.sparkContext.setLogLevel("WARN")
    try:
        records = (spark.readStream.format("kafka")
                   .option("kafka.bootstrap.servers", BOOTSTRAP)
                   .option("subscribe", TOPIC).option("startingOffsets", "earliest")
                   .load())
        trades = parse_trades(records)
        # AvailableNow processes the backlog and exits. The checkpoint remembers offsets.
        query = (trades.writeStream.format("parquet").outputMode("append")
                 .option("checkpointLocation", str(CHECKPOINT))
                 .trigger(availableNow=True).start(str(TRADES)))
        query.awaitTermination()
        processed = sum(batch["numInputRows"] for batch in query.recentProgress)
        print(f"processed records={processed}")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
