"""
consumer.py
-----------
Kafka Consumer — reads messages from 'news-stream' topic
and performs real-time trend analysis.

Save to: src/consumer.py
Run:
    python src/consumer.py
"""

import json
import csv
from kafka import KafkaConsumer
from collections import defaultdict

# ─── Config ─────────────────────────────────────────────
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC  = "news-stream"

# ─── Kafka Consumer Setup ───────────────────────────────
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='news-group'
)

print("🚀 Consumer started... Listening to Kafka topic")

# ─── Data Structures ────────────────────────────────────
category_count = defaultdict(int)
total_messages = 0

# ─── Processing Loop ────────────────────────────────────
for message in consumer:
    data = message.value
    category = data.get("category", "unknown")

    category_count[category] += 1
    total_messages += 1

    # Print every 1000 messages
    if total_messages % 50 == 0:
        print("\n" + "="*50)
        print(f"Processed {total_messages} messages")

        # 🔥 Top Category
        top_category = max(category_count, key=category_count.get)
        print("🔥 Trending Category:", top_category)

        # 📊 Category Counts
        print("Top Categories:", dict(category_count))

        # 📊 Percentage Distribution
        total = sum(category_count.values())
        percentages = {
            k: round((v / total) * 100, 2)
            for k, v in category_count.items()
        }
        print("📊 Distribution (%):", percentages)

        # 💾 Save to CSV
        with open("src/output.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "Count"])
            for k, v in category_count.items():
                writer.writerow([k, v])

        print("💾 Data saved to output.csv")