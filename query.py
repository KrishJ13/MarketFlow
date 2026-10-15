"""Read the saved Parquet rows and count valid trade deliveries per UTC minute."""

from pyspark.sql import SparkSession

from settings import TRADES


def count_trades(spark, trades):
    trades.createOrReplaceTempView("trades")
    return spark.sql("""
        SELECT product_id, date_trunc('minute', event_time) AS minute,
               COUNT(*) AS trade_count
        FROM trades
        WHERE schema_valid
        GROUP BY product_id, date_trunc('minute', event_time)
        ORDER BY minute, product_id
    """)


def main():
    spark = (SparkSession.builder.appName("marketflow-v0-query")
             .config("spark.sql.session.timeZone", "UTC").getOrCreate())
    spark.sparkContext.setLogLevel("WARN")
    try:
        trades = spark.read.parquet(str(TRADES))
        print(f"written records={trades.count()}")
        count_trades(spark, trades).show(truncate=False)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
