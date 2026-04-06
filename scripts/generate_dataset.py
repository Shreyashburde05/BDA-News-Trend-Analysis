"""
generate_dataset.py
--------------------
Generates a realistic synthetic news dataset with 1,000,000 rows.
Uses vectorized NumPy operations for speed — typically completes in ~30 seconds.

Save to: scripts/generate_dataset.py
Output: data/news_data.csv
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os
import time

# ─── Configuration ────────────────────────────────────────────────────────────
TOTAL_ROWS   = 1_000_000
DATA_DIR     = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_PATH  = os.path.join(DATA_DIR, "news_data.csv")
CHUNK_SIZE   = 100_000          # write in chunks to keep RAM usage low
RANDOM_SEED  = 42
# ──────────────────────────────────────────────────────────────────────────────

# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR, exist_ok=True)

np.random.seed(RANDOM_SEED)

CATEGORIES = ["politics", "sports", "technology", "AI",
               "finance", "health", "entertainment", "world"]

SOURCES = ["BBC", "CNN", "Reuters", "NDTV", "Times of India"]

# Templates for realistic headlines
TEMPLATES = {
    "AI": {
        "subjects": [
            "AI model", "ChatGPT rival", "Google DeepMind", "OpenAI",
            "Anthropic Claude", "Meta AI", "AI startup", "Large language model",
            "AI-powered robot", "Generative AI tool", "AI chip maker",
            "Microsoft Copilot", "AI regulation body", "AI ethics board",
        ],
        "actions": [
            "surpasses human performance in", "raises $1B to accelerate",
            "launches new model for", "faces scrutiny over",
            "partners with government on", "disrupts traditional",
            "sets new benchmark in", "wins major contract for",
            "triggers debate about", "automates thousands of jobs in",
            "achieves breakthrough in", "announces open-source release of",
        ],
        "tails": [
            "medical diagnosis", "drug discovery", "climate modelling",
            "financial forecasting", "code generation", "creative writing",
            "legal analysis", "autonomous driving", "education",
            "cybersecurity", "customer service", "scientific research",
        ],
    },
    "politics": {
        "subjects": [
            "US President", "Prime Minister Modi", "EU Parliament",
            "Senate Democrats", "Republican lawmakers", "White House",
            "UN Secretary-General", "NATO leaders", "G7 summit",
            "Opposition party", "Electoral commission", "Supreme Court",
            "Federal Election", "State legislature",
        ],
        "actions": [
            "pushes new bill on", "calls emergency session over",
            "reaches historic deal on", "faces backlash for",
            "approves sweeping reform of", "vetoes controversial",
            "launches investigation into", "debates future of",
            "imposes sanctions over", "holds referendum on",
            "signs executive order on", "withdraws support for",
        ],
        "tails": [
            "immigration policy", "gun control", "tax reform",
            "healthcare spending", "climate legislation", "trade tariffs",
            "national security", "election integrity", "social media regulation",
            "foreign aid", "debt ceiling", "voting rights",
        ],
    },
    "sports": {
        "subjects": [
            "India cricket team", "Virat Kohli", "Rohit Sharma",
            "Manchester City", "Real Madrid", "LeBron James",
            "Novak Djokovic", "Carlos Alcaraz", "Olympics committee",
            "IPL franchise", "FIFA World Cup organizers",
            "Premier League", "NBA playoffs", "F1 championship",
        ],
        "actions": [
            "wins thrilling match against", "breaks world record in",
            "signs $200M contract with", "faces doping allegation in",
            "announces retirement from", "dominates tournament at",
            "suffers injury ahead of", "prepares for title clash in",
            "sets new season record in", "beats top-ranked rival in",
        ],
        "tails": [
            "World Cup qualifier", "Champions League final",
            "Grand Slam tournament", "T20 series", "Olympic trials",
            "Test championship", "NBA finals", "Formula 1 race",
            "Premier League title race", "Davis Cup",
        ],
    },
    "technology": {
        "subjects": [
            "Apple", "Samsung", "Tesla", "SpaceX", "Nvidia",
            "AMD", "Intel", "TSMC", "Qualcomm", "Sony",
            "Google Pixel", "OnePlus", "5G network operator",
            "Quantum computing lab",
        ],
        "actions": [
            "unveils next-gen", "launches record-breaking",
            "files patent for", "acquires startup working on",
            "recalls millions of", "partners with NASA on",
            "announces layoffs amid slowdown in", "beats earnings forecast with",
            "open-sources its", "faces antitrust probe over",
        ],
        "tails": [
            "foldable smartphone", "AR glasses", "EV battery",
            "satellite internet", "gaming chip", "quantum processor",
            "neural interface", "home robot", "solar panel technology",
            "memory chip", "5G modem", "wearable health device",
        ],
    },
    "finance": {
        "subjects": [
            "Federal Reserve", "Bitcoin", "Ethereum", "Stock market",
            "Goldman Sachs", "JPMorgan", "Sensex", "Nifty 50",
            "Crypto exchange", "Hedge fund", "RBI", "World Bank",
            "IMF", "Oil prices",
        ],
        "actions": [
            "surges to all-time high amid", "crashes 15% on fears of",
            "raises interest rates to combat", "warns investors about",
            "halts trading following", "predicts recession due to",
            "approves landmark ETF for", "freezes accounts over",
            "fines bank $500M for", "cuts growth forecast citing",
        ],
        "tails": [
            "inflation concerns", "rate hike fears", "crypto winter",
            "banking crisis", "AI investment boom", "trade war escalation",
            "geopolitical tensions", "energy price spike",
            "bond market turmoil", "dollar strength", "IPO frenzy",
        ],
    },
    "health": {
        "subjects": [
            "WHO", "CDC", "ICMR", "Moderna", "Pfizer",
            "New virus variant", "Health ministry", "Cancer researchers",
            "Mental health experts", "Global health report",
            "FDA", "Drug trial", "Pandemic watchdog", "Nutrition study",
        ],
        "actions": [
            "warns of new outbreak of", "approves revolutionary drug for",
            "launches global campaign against", "reports surge in cases of",
            "discovers genetic cause of", "calls for urgent action on",
            "raises alarm over", "recommends new vaccine for",
            "links ultra-processed food to", "issues travel advisory over",
        ],
        "tails": [
            "mpox variant", "antibiotic resistance", "childhood obesity",
            "mental health crisis", "Alzheimer's disease", "long COVID",
            "malaria resurgence", "tuberculosis", "cancer screening",
            "air pollution effects", "dengue fever", "diabetes epidemic",
        ],
    },
    "entertainment": {
        "subjects": [
            "Hollywood studio", "Netflix", "Disney+", "Bollywood star",
            "Grammy winner", "Oscar ceremony", "Streaming giant",
            "Box office record", "Taylor Swift", "BTS",
            "Cannes Film Festival", "Deepika Padukone", "Marvel Studios",
            "YouTube creator",
        ],
        "actions": [
            "breaks all-time record with", "cancels controversial",
            "announces sequel to", "wins Best Picture for",
            "faces boycott over", "signs $100M deal for",
            "drops surprise album amid", "goes viral for",
            "reunites cast of", "reveals trailer for",
        ],
        "tails": [
            "blockbuster thriller", "animated feature", "reality TV show",
            "world tour", "autobiographical film", "superhero franchise",
            "period drama series", "comedy special", "documentary",
            "music video", "limited series", "biopic",
        ],
    },
    "world": {
        "subjects": [
            "Russia", "Ukraine", "China", "Israel", "Gaza",
            "North Korea", "Iran", "Pakistan", "Myanmar rebels",
            "African Union", "ASEAN summit", "Taiwan strait",
            "Red Sea shipping", "Arctic council",
        ],
        "actions": [
            "launches military offensive in", "calls for ceasefire in",
            "imposes new sanctions on", "withdraws diplomats from",
            "signs peace agreement with", "threatens retaliation over",
            "sends humanitarian aid to", "expels ambassador of",
            "seizes disputed territory near", "warns of escalation in",
        ],
        "tails": [
            "eastern front", "disputed border region", "maritime zone",
            "civilian corridor", "occupied territory", "UN resolution",
            "peace summit", "trade route", "nuclear facility",
            "refugee camp", "demilitarized zone", "strategic islands",
        ],
    },
}

CATEGORY_WEIGHTS = [0.14, 0.12, 0.11, 0.18, 0.12, 0.10, 0.10, 0.13]


def _build_headlines_for_category(cat: str, n: int) -> np.ndarray:
    """Return n headline strings for a single category using random assembly."""
    pool = TEMPLATES[cat]
    subj_arr = np.array(pool["subjects"])
    act_arr  = np.array(pool["actions"])
    tail_arr = np.array(pool["tails"])

    subjects = subj_arr[np.random.randint(0, len(subj_arr), n)]
    actions  = act_arr [np.random.randint(0, len(act_arr),  n)]
    tails    = tail_arr[np.random.randint(0, len(tail_arr), n)]

    return np.char.add(
        np.char.add(subjects, " "),
        np.char.add(actions, np.char.add(" ", tails))
    )


def generate_chunk(start_id: int, size: int) -> pd.DataFrame:
    """Build one chunk of `size` rows and return as a DataFrame."""
    ids = np.arange(start_id, start_id + size)
    categories = np.random.choice(CATEGORIES, size=size, p=CATEGORY_WEIGHTS)
    headlines = np.empty(size, dtype=object)
    for cat in CATEGORIES:
        mask = (categories == cat)
        n_cat = int(mask.sum())
        if n_cat > 0:
            headlines[mask] = _build_headlines_for_category(cat, n_cat)

    base_ts  = datetime.now() - timedelta(days=30)
    window_s = int(timedelta(days=30).total_seconds())
    offsets  = np.random.randint(0, window_s, size=size)
    timestamps = pd.to_datetime(base_ts.timestamp() + offsets, unit="s") \
                   .strftime("%Y-%m-%d %H:%M:%S")

    sources = np.random.choice(SOURCES, size=size)

    return pd.DataFrame({
        "id":        ids,
        "headline":  headlines,
        "category":  categories,
        "timestamp": timestamps,
        "source":    sources,
    })


def main():
    print("=" * 60)
    print("  News Dataset Generator  —  1,000,000 rows")
    print("=" * 60)
    t0 = time.time()

    first_chunk  = True
    rows_written = 0

    for chunk_start in range(1, TOTAL_ROWS + 1, CHUNK_SIZE):
        chunk_size = min(CHUNK_SIZE, TOTAL_ROWS - chunk_start + 1)
        df = generate_chunk(chunk_start, chunk_size)

        df.to_csv(
            OUTPUT_PATH,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False,
        )
        first_chunk   = False
        rows_written += chunk_size

        pct     = rows_written / TOTAL_ROWS * 100
        elapsed = time.time() - t0
        print(f"  ✔  {rows_written:>10,} / {TOTAL_ROWS:,} rows  "
              f"[{pct:5.1f}%]  [{elapsed:5.1f}s]")

    elapsed = time.time() - t0
    size_mb = os.path.getsize(OUTPUT_PATH) / 1_048_576
    print("-" * 60)
    print(f"  ✅  Done!  {TOTAL_ROWS:,} rows  →  {OUTPUT_PATH}")
    print(f"      File size : {size_mb:.1f} MB")
    print(f"      Time taken: {elapsed:.1f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    main()
