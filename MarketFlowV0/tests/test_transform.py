"""Two examples of the Spark transformation, without Kafka."""

import json
from decimal import Decimal
from pathlib import Path

import pytest
from pyspark.sql import SparkSession

from query import count_trades
from transform import parse_trades


@pytest.fixture(scope="module")
def spark():
    session = (SparkSession.builder.master("local[1]").appName("v0-tests")
               .config("spark.sql.session.timeZone", "UTC").getOrCreate())
    session.sparkContext.setLogLevel("WARN")
    yield session
    session.stop()


def records(spark, trades):
    rows = [(0, offset, json.dumps(trade).encode()) for offset, trade in enumerate(trades)]
    return spark.createDataFrame(rows, "partition int, offset long, value binary")


def test_valid_trades_become_typed_rows_and_minute_counts(spark):
    inputs = json.loads(Path("fixtures/trades.json").read_text())
    trades = parse_trades(records(spark, inputs))
    rows = trades.orderBy("offset").collect()
    assert len(rows) == 3 and all(row.schema_valid for row in rows)
    assert rows[0].price == Decimal("60000.00")
    assert rows[0].size == Decimal("0.01")
    assert rows[0].raw_json == json.dumps(inputs[0])
    counts = count_trades(spark, trades).collect()
    assert [(r.product_id, r.trade_count) for r in counts] == [("BTC-USD", 2), ("ETH-USD", 1)]
    assert counts[0].minute.strftime("%H:%M:%S") == "12:00:00"


def test_bad_price_remains_visible_but_is_not_counted(spark):
    trade = json.loads(Path("fixtures/trades.json").read_text())[0]
    trade["price"] = "not-a-number"
    trades = parse_trades(records(spark, [trade]))
    row = trades.first()
    assert row.price is None and row.schema_valid is False
    assert row.offset == 0 and "not-a-number" in row.raw_json
    assert count_trades(spark, trades).count() == 0
