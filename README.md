# Real-Time News Trend Detection — Person 1 (Kafka & Producer)

This repository contains the setup for **Person 1** in the "Real-Time News Trend Detection using Spark Streaming" project.

## Responsibilities
*   **Infrastructure**: Kafka, Zookeeper, and Kafka UI using Docker.
*   **Data Generation**: Generating 1,000,000 synthetic news records with realistic headlines.
*   **Producer**: Streaming the records to Kafka in real-time.

---

## Folder Structure
```
.
├── docker/
│   └── docker-compose.yml      # Kafka, Zookeeper, Kafka UI
├── scripts/
│   ├── generate_dataset.py     # 1M record synthetic dataset generator
│   ├── verify_dataset.py       # Sanity check on the dataset (row count, distribution)
│   └── create_topic.py         # Script to initialize Kafka topic 'news-stream'
├── src/
│   └── producer.py             # Kafka producer — streams messages from CSV to Kafka
├── data/                       # (Auto-generated) stores the 1M record CSV
├── requirements.txt            # Python dependencies (numpy, pandas, kafka-python)
└── README.md                   # Setup guide
```

---

## Setup Instructions

### 1. Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Generate Dataset
Generate the 1,000,000 news records (takes ~30-60 seconds):
```bash
python scripts/generate_dataset.py
```
*Verify the data (optional):*
```bash
python scripts/verify_dataset.py
```

### 3. Start Kafka Infrastructure
Launch the Docker services (Zookeeper, Kafka, Kafka UI):
```bash
docker-compose -f docker/docker-compose.yml up -d
```
*Wait ~10 seconds for Kafka to be healthy. Access Kafka UI at: http://localhost:8080*

### 4. Create Kafka Topic
Initialize the `news-stream` topic:
```bash
python scripts/create_topic.py
```

### 5. Run Producer
Start streaming the news data into Kafka:
```bash
python src/producer.py
```
*The producer is configured to stream 500 rows/second by default. You can see the messages appearing in real-time on the Kafka UI.*

---

## Configuration Variables (Producer)
You can modify the producer speed or Kafka broker settings by setting environment variables before running `src/producer.py`:
*   `ROWS_PER_SECOND`: Change streaming speed (e.g., `set ROWS_PER_SECOND=1000`)
*   `KAFKA_BROKER`: Broker address (default: `localhost:9092`)
*   `KAFKA_TOPIC`: Kafka topic name (default: `news-stream`)
