"""
create_topic.py
----------------
Utility script to create the 'news-stream' Kafka topic.
Run this once after Kafka is up and before starting the producer.

Save to: scripts/create_topic.py
Usage:
    python scripts/create_topic.py
"""

import os
import sys
import time
import logging
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [TOPIC-MGR] %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC_NAME   = os.getenv("KAFKA_TOPIC",  "news-stream")
PARTITIONS   = int(os.getenv("KAFKA_PARTITIONS", "3"))   # 3 partitions for parallelism
REPLICATION  = int(os.getenv("KAFKA_REPLICATION", "1"))  # 1 for single-broker dev setup


def get_admin_client(retries=10, delay=5) -> KafkaAdminClient:
    """Return a connected KafkaAdminClient, retrying if necessary."""
    for attempt in range(1, retries + 1):
        try:
            return KafkaAdminClient(
                bootstrap_servers=KAFKA_BROKER,
                client_id="news-topic-manager",
            )
        except NoBrokersAvailable:
            log.warning("Kafka not ready (attempt %d/%d) — retrying in %ds …",
                        attempt, retries, delay)
            time.sleep(delay)
    
    raise RuntimeError(f"Could not connect to Kafka at {KAFKA_BROKER}")


def create_topic():
    """Create the news-stream topic if it does not already exist."""
    admin = get_admin_client()
    topic = NewTopic(
        name=TOPIC_NAME,
        num_partitions=PARTITIONS,
        replication_factor=REPLICATION,
        # Keep messages for 2 hours
        topic_configs={"retention.ms": str(2 * 60 * 60 * 1000)},
    )
    try:
        admin.create_topics([topic])
        log.info("✅ Topic '%s' created  (partitions=%d, replication=%d)",
                 TOPIC_NAME, PARTITIONS, REPLICATION)
    except TopicAlreadyExistsError:
        log.info("Topic '%s' already exists — skipping creation.", TOPIC_NAME)
    finally:
        admin.close()


if __name__ == "__main__":
    try:
        create_topic()
    except Exception as e:
        log.error("Fatal error: %s", e)
        sys.exit(1)
