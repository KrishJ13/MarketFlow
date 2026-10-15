# Follow one trade

Start with `fake-1` in fixtures/trades.json. Its product is BTC-USD, its price
is the string `"60000.00"`, and its event time is `12:00:05Z` on 2026-10-15.
`Z` means UTC. This is invented data for learning.

## 1. Python sends bytes — producer.py

`publish(path)` reads the file into a list of Python dictionaries. Inside its
ordinary loop, `json.dumps(trade).encode("utf-8")` turns one dictionary into
JSON text, then bytes. Kafka values are bytes, not Python dictionaries.

```python
result = producer.send(TOPIC, key=product_bytes, value=payload).get(timeout=10)
```

`send` queues a write; `get` waits for Kafka's acknowledgement. `result` tells
you its partition and offset. An offset is a position within one partition.
The product key groups that product's messages into a partition. The small
finally block closes the connection even if a send fails.

## 2. Kafka holds records — inspect_kafka.py

Kafka is the stored log between two programs. The producer can stop; records
remain in Kafka until retention removes them. A consumer can read them later.

`inspect()` prints each stored value plus its partition/offset. It has no consumer
group or saved bookmark, so it starts at the beginning each time. It does not
advance Spark's bookmark. The three-second idle timeout only makes this learning
script exit instead of waiting indefinitely.

## 3. Spark makes columns — transform.py

Spark's Kafka reader gives a DataFrame with columns including `value`,
`partition` and `offset`. A DataFrame describes rows and named columns.

`parse_trades(records)` returns another DataFrame:

```text
value bytes → raw_json text → trade fields → typed price/size/time → validity flag
```

`from_json` uses the short schema to give JSON fields column names. `trade.*`
opens those fields into separate columns. `withColumn` returns a new DataFrame
plan; it does not edit the old object. `try_cast` gives null if conversion fails.
The `&` in the schema check combines Spark column conditions row by row.

For fake-1 the result has Decimal price 60000, Decimal size 0.01, a timestamp,
and schema_valid=true. A price of `"not-a-number"` gives null and false; its raw
JSON/coordinates remain stored so the invalid delivery is visible.

## 4. Spark runs the plan — stream.py

`main()` connects Spark to Kafka, calls `parse_trades`, then starts a streaming
Parquet write. The earlier DataFrame operations describe the work; `start`
runs it. `awaitTermination` waits for completion before Python exits.

AvailableNow means “process the available backlog, then finish.” It uses the
streaming source/sink and checkpoint, but it is not a continuously running job.
Parquet stores typed columns. The checkpoint stores query progress, including
Kafka offsets. It belongs with these output files and this topic.

## 5. SQL counts saved rows — query.py

This is a separate Spark batch program. It reads Parquet, not Kafka.
`count_trades(spark, trades)` names the DataFrame `trades` for SQL, groups by
product and the event time rounded down to its minute, and counts valid rows.
fake-1 and fake-2 both fall in BTC's 12:00 minute, giving count 2.
`show()` executes the query and prints the result. `main()` also counts all stored
rows, including invalid ones, as the simple `written` observation.

## The other technologies, when needed

Do not implement these in V0. Each later lesson should first expose its direct,
small operation, with inputs and outputs as clear as the functions above:

| Component | First useful operation | Where it will fit |
| --- | --- | --- |
| Docker | Run a script in a container with its dependencies | Runtime around our existing programs |
| Airflow | Task A finishes before task B starts | Schedule bounded processing scripts; not a streaming engine |
| S3 | `put_object(Bucket=..., Key=..., Body=...)` | Store raw bytes as objects; ordinary PUT can replace a key |
| Delta | Change a Spark file write to a Delta table write | Add a transaction log to stored data; not yet Parquet's guarantee |
| Databricks | Run an already-understood Spark script as a job | Managed execution of the Spark logic |
| Snowflake | Load a small file, then SELECT its rows | Analytical warehouse after lake processing |
| dbt | One SQL model using a source/ref | Build and test warehouse tables/views |

For S3, some access permission is required by AWS. Start with the minimum
permission to perform the lesson's operation and keep credentials out of code.
Additional access-policy mechanisms deserve a later lesson, after the basic
connection and object operation are understood.

Explain back: which program still needs Kafka after Parquet is written? Why is
“3 deliveries stored” different from “3 distinct real market trades”? Why does
SQL group by event time even if you run this example tomorrow?
