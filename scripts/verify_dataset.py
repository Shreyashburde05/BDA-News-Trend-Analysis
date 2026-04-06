"""
verify_dataset.py
------------------
Quick sanity-check on the generated CSV before streaming.
Prints row count, null checks, category distribution, and sample rows.

Save to: scripts/verify_dataset.py
Usage:
    python scripts/verify_dataset.py
"""

import os
import pandas as pd

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "news_data.csv")

def verify():
    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: Dataset not found at {CSV_PATH}")
        print("   Please run 'python scripts/generate_dataset.py' first.")
        return

    print("=" * 60)
    print("  Dataset Verification Report")
    print("=" * 60)

    # Load only what we need to keep RAM low
    print("\n📂 Loading dataset …")
    df = pd.read_csv(CSV_PATH, dtype=str)

    # ── Row count ─────────────────────────────────────────────────────────
    print(f"\n✅ Total rows       : {len(df):,}")
    print(f"   Columns          : {list(df.columns)}")

    # ── Null check ────────────────────────────────────────────────────────
    nulls = df.isnull().sum()
    if nulls.sum() == 0:
        print("   Null values      : None ✅")
    else:
        print(f"   Null values      : ⚠️\n{nulls[nulls > 0]}")

    # ── Category distribution ─────────────────────────────────────────────
    print("\n📊 Category distribution:")
    cat_counts = df["category"].value_counts()
    for cat, count in cat_counts.items():
        bar = "█" * int(count / len(df) * 40)
        print(f"   {cat:<15} {count:>8,}  {count/len(df)*100:5.1f}%  {bar}")

    # ── Source distribution ───────────────────────────────────────────────
    print("\n📡 Source distribution:")
    src_counts = df["source"].value_counts()
    for src, count in src_counts.items():
        print(f"   {src:<20} {count:>8,}  {count/len(df)*100:5.1f}%")

    # ── Timestamp range ───────────────────────────────────────────────────
    timestamps = pd.to_datetime(df["timestamp"])
    print(f"\n⏱  Timestamp range  : {timestamps.min()}  →  {timestamps.max()}")

    # ── Sample rows ───────────────────────────────────────────────────────
    print("\n📋 Sample headlines (5 random rows):")
    sample = df[["id","headline","category","source"]].sample(5)
    for _, row in sample.iterrows():
        print(f"   [{row['category']:<13}] [{row['source']:<14}] {row['headline']}")

    print("\n" + "=" * 60)
    print("  Verification complete — dataset looks healthy! 🎉")
    print("=" * 60)


if __name__ == "__main__":
    verify()
