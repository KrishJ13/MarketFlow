# MarketFlow — understand one complete pipeline

This is the new, minimal learning baseline. Everything needed to run it is in
this repository root; no parent project is needed.
All three input trades are **synthetic**, not live market observations.

```text
fixtures/trades.json
       │ producer.py: JSON → bytes → send
       ▼
     Kafka topic
       ├── inspect_kafka.py: print the stored messages
       │ stream.py: read → parse_trades → write
       ▼
  data/trades/ (Parquet)
       │ query.py: read files → SQL
       ▼
  BTC-USD: 2 trades in 12:00 UTC
  ETH-USD: 1 trade  in 12:01 UTC
```

Docker supplies Python, Java, Kafka and Spark. You need Docker running, Compose
and Make. You do not need an AWS account, host Python/Java or Airflow.

## Run each step yourself

Run from the repository root:

```sh
cd /Users/krish/Projects/MarketFlow
make build       # install the three Python packages in the tools image
make up          # start this project's Kafka broker
make produce     # send the three fixture trades
make inspect     # see each JSON value and its partition/offset
make stream      # process the current Kafka backlog into Parquet, then exit
make query       # count the saved deliveries per product and event-time minute
```

The producer prints three acknowledgements (`received event_id=...`). Spark
prints `processed records=3`. Query prints `written records=3` and this result:

```text
product_id | minute (UTC)        | trade_count
BTC-USD    | 2026-10-15 12:00:00 | 2
ETH-USD    | 2026-10-15 12:01:00 | 1
```

Spark also prints its own startup/stage logs. The first stream downloads the
Kafka connector; the named `spark-jars` volume caches it.

Now run `make stream` and `make query` again **without producing again**.
Expect 0 newly processed records and still 3 written rows. The checkpoint is
Spark's bookmark. `make inspect` still sees all 3: reading Kafka does not erase it.

Running `make produce` again deliberately adds three more deliveries. After
stream/query you get 6 rows and counts 4/2. V0 does not deduplicate trade IDs.

## Which file should I read?

| File/function | Input → output | Concept |
| --- | --- | --- |
| `settings.py` | a few defaults → shared connection/topic/paths | wiring |
| `producer.py: publish` | JSON file → acknowledged Kafka records | serialisation and producer |
| `inspect_kafka.py: inspect` | Kafka records → printed bytes/text and coordinates | independent consumer |
| `transform.py: parse_trades` | Kafka DataFrame → typed trade DataFrame | schema and lazy transformation |
| `stream.py: main` | Kafka backlog → Parquet files + checkpoint | Structured Streaming |
| `query.py: count_trades` | saved trade DataFrame → minute counts | SQL aggregation |

Read them in this order. [Follow one record through the program](docs/flow.md)
explains the function calls and the minimal implementations of later components.

Make is only a command shortcut: `make -n stream` shows its full command.
`docker compose run --rm tools ...` starts a temporary Python/Spark container on
the same network as Kafka, where the broker's hostname is `kafka`. No Kafka host
port is published. `compose.yaml` uses separate volumes/network so old brokers
and old project files are unaffected. Broker environment lines configure one
Kafka process as both broker and controller; keep those wiring details aside
until the basic send/read flow is clear.

## A few tests and one real verification

```sh
make test        # two real Spark examples: valid trades and one bad price
make verify      # one isolated real Kafka → Spark → files → SQL/restart check
make stop        # stop this project's services, keeping data
```

`make verify` creates its own topic and output/checkpoint under
`data/verification-<timestamp>/`. It runs the actual scripts and retains logs.
It does not add records to your practice topic or replace your practice files.
See CURRENT_STATE.md for actual performed results.

For another independent practice run, choose a fresh name for **both** the topic
and data directory. Here is the explicit pattern (use a new name each time):

```sh
docker compose run --rm -e KAFKA_TOPIC=practice-02 -e DATA_DIR=data/practice-02 tools python producer.py
docker compose run --rm -e KAFKA_TOPIC=practice-02 -e DATA_DIR=data/practice-02 tools spark-submit --master 'local[1]' --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0 stream.py
docker compose run --rm -e KAFKA_TOPIC=practice-02 -e DATA_DIR=data/practice-02 tools spark-submit --master 'local[1]' query.py
```

## Deliberate limits

This V0 uses flat fake JSON, one local Kafka broker, local Spark, a basic
non-null/type check and Parquet files. Decimal avoids floating-point price/size
approximation. Bad required values remain stored with `schema_valid=false`;
SQL excludes them. This check is not full business/domain validation.

Minutes use the input's event time in UTC, not the time you run the script.
Every valid stored delivery participates in SQL, even an older event. There is
no watermark/finality policy, business deduplication or production recovery claim.
Keep output and checkpoint together: deleting only output leaves Spark remembering
records whose files are gone. A fresh experiment uses a new topic AND directory.

## What comes next?

Review V0 before implementing V1. Explain where JSON becomes bytes, where bytes
become columns, why a second stream run adds nothing, and why producing twice
doubles counts. The eventual stack/specification is retained in PROJECT_SPEC.md;
it is not all part of this lesson. Earlier project state/learning records are
copied into docs/history/ for reference. Their old evidence paths refer to the
archived previous project, not this baseline's current data.

## Previous project archive

The old project files were removed after an independent build/test from a
temporary copy outside this repository. At the user's request, the root `.git/`
now starts a fresh local history with a single V0 baseline commit. No remote
history was changed or pushed.
`data/legacy-backup-20261015/old-project.tar.gz` contains the old source, authentic
captures and evidence; manifest.json records verified file hashes. Old virtual
environments/caches were removed; their package lists were saved alongside the
archive. Old Docker services are stopped and their volumes retained.

This backup is ignored by Git. Copy it somewhere separate before deleting this
workspace. To inspect or recover old files, extract the archive into a separate
directory, not over this new baseline.
