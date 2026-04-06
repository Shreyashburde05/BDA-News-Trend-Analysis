"""
producer.py
-----------
Kafka Producer — reads the generated CSV and streams rows to the
'news-stream' Kafka topic at a configurable rate.

Each message is JSON-encoded so the Spark consumer can parse fields easily.

Save to: src/producer.py
Usage:
    python src/producer.py
"""

import os
import json
import time
import logging
import pandas as pd
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

# ─── Logging setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [PRODUCER] %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ─── Config (env-overridable) ─────────────────────────────────────────────────
KAFKA_BROKER    = os.getenv("KAFKA_BROKER",    "localhost:9092")
KAFKA_TOPIC     = os.getenv("KAFKA_TOPIC",     "news-stream")
ROWS_PER_SECOND = int(os.getenv("ROWS_PER_SECOND", "500"))
CSV_PATH        = os.getenv("CSV_PATH", os.path.join(
                      os.path.dirname(__file__),
                      "..", "data", "news_data.csv"))

# ─── How many rows to load per CSV chunk (saves RAM for 1M-row file) ──────────
CSV_CHUNK_SIZE  = 50_000


def make_producer(retries: int = 20, delay: int = 5) -> KafkaProducer:
    """
    Create and return a KafkaProducer, retrying until Kafka is ready.
    Serialises values to UTF-8 JSON automatically.
    """
    for attempt in range(1, retries + 1):
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                # Serialise each dict as compact JSON bytes
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                # Batch small messages together for higher throughput
                batch_size=16_384,
                linger_ms=10,
                # Retry on transient send errors
                retries=5,
            )
            log.info("Connected to Kafka broker at %s", KAFKA_BROKER)
            return producer
        except NoBrokersAvailable:
            log.warning("Kafka not ready (attempt %d/%d) — retrying in %ds …",
                        attempt, retries, delay)
            time.sleep(delay)

    raise RuntimeError(f"Could not connect to Kafka at {KAFKA_BROKER} "
                       f"after {retries} attempts.")


def stream_csv(producer: KafkaProducer) -> None:
    """
    Read the CSV in chunks and publish each row as a Kafka message.
    Throttles to ROWS_PER_SECOND to simulate a realistic data stream.
    """
    if not os.path.exists(CSV_PATH):
        log.error("Dataset not found at %s. Please generate it first.", CSV_PATH)
        return

    sleep_interval = 1.0 / ROWS_PER_SECOND  # seconds between messages

    log.info("Streaming '%s' → topic '%s'  @ %d rows/s",
             CSV_PATH, KAFKA_TOPIC, ROWS_PER_SECOND)

    total_sent  = 0
    chunk_num   = 0

    # Iterate over the file in chunks to avoid loading 1M rows into RAM at once
    for chunk in pd.read_csv(CSV_PATH, chunksize=CSV_CHUNK_SIZE,
                               dtype={"id": int, "headline": str,
                                      "category": str, "timestamp": str,
                                      "source": str}):
        chunk_num += 1
        log.info("Processing chunk #%d  (%d rows)", chunk_num, len(chunk))

        for _, row in chunk.iterrows():
            # Build the message payload as a plain dict (JSON-ready)
            message = {
                "id":        int(row["id"]),
                "headline":  str(row["headline"]),
                "category":  str(row["category"]),
                "timestamp": str(row["timestamp"]),
                "source":    str(row["source"]),
            }

            # Send asynchronously — KafkaProducer batches internally
            producer.send(KAFKA_TOPIC, value=message)
            total_sent += 1

            # Throttle: sleep between messages
            time.sleep(sleep_interval)

            # Log progress every 10,000 rows
            if total_sent % 10_000 == 0:
                log.info("Sent %10d rows so far …", total_sent)

        # Flush any buffered messages at the end of each chunk
        producer.flush()

    log.info("✅ Stream complete — %d rows published to topic '%s'",
             total_sent, KAFKA_TOPIC)


def main():
    log.info("=" * 55)
    log.info("  News Kafka Producer starting …")
    log.info("  Broker : %s", KAFKA_BROKER)
    log.info("  Topic  : %s", KAFKA_TOPIC)
    log.info("  Rate   : %d rows/second", ROWS_PER_SECOND)
    log.info("=" * 55)

    producer = make_producer()
    try:
        stream_csv(producer)
    except KeyboardInterrupt:
        log.info("Interrupted by user — flushing remaining messages …")
        producer.flush()
    finally:
        producer.close()
        log.info("Producer closed.")


if __name__ == "__main__":
    main()
