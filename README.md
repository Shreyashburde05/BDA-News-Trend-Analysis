---

## 📌 Project Overview

This project builds a **real-time data pipeline** where:

* 📰 1,000,000 synthetic news records are generated
* ⚡ Data is streamed into Kafka using a Producer
* 📊 A Consumer processes the stream and extracts **top trending categories**
* 📁 Results are stored for analysis

---

## 🏗️ Tech Stack

* **Apache Kafka** – Real-time data streaming
* **Docker** – Containerized infrastructure (Kafka + Zookeeper + UI)
* **Python** – Data generation, Producer & Consumer
* **Pandas / NumPy** – Data processing

---

## 📂 Project Structure

```
.
├── docker/
│   └── docker-compose.yml      # Kafka, Zookeeper, Kafka UI
├── scripts/
│   ├── generate_dataset.py     # 1M record dataset generator
│   ├── verify_dataset.py       # Dataset validation
│   └── create_topic.py         # Kafka topic creation
├── src/
│   ├── producer.py             # Streams data into Kafka
│   └── consumer.py             # Processes data & generates insights
├── data/                       # Generated dataset (ignored in Git)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Generate Dataset

```bash
python scripts/generate_dataset.py
```

(Optional)

```bash
python scripts/verify_dataset.py
```

---

### 3. Start Kafka (Docker)

```bash
docker-compose -f docker/docker-compose.yml up -d
```

Kafka UI:
👉 http://localhost:8080

---

### 4. Create Kafka Topic

```bash
python scripts/create_topic.py
```

---

### 5. Start Producer (Streaming Data)

```bash
python src/producer.py
```

---

### 6. Run Consumer (Real-Time Analysis)

```bash
python src/consumer.py
```

---

## 📊 Sample Output

| Category      | Count |
| ------------- | ----- |
| AI            | 37070 |
| Politics      | 28729 |
| World         | 26547 |
| Finance       | 24861 |
| Sports        | 24813 |
| Technology    | 22765 |
| Entertainment | 20684 |
| Health        | 20531 |

---

## 🎯 Key Features

* ⚡ Real-time streaming pipeline
* 📈 Category-wise trend detection
* 🧠 Handles large-scale data (1M records)
* 🔍 Kafka UI monitoring
* 📂 Clean modular architecture

---

## 🧠 What I Learned

* Setting up Kafka using Docker
* Building Producer-Consumer architecture
* Streaming large datasets efficiently
* Real-time data processing concepts

---

## 🚀 Future Improvements

* 📊 Live dashboard (Streamlit)
* ⏱ Window-based trend analysis
* 🧠 Sentiment analysis on headlines
* ☁️ Deployment on cloud (AWS/GCP)

---
