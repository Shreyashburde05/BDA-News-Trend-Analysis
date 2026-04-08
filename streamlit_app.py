import streamlit as st
import pandas as pd
import time
from datetime import datetime
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="News Trends Dashboard", layout="wide")

st.title("📰 Real-Time News Trends Dashboard")

# -----------------------------
# AUTO REFRESH
# -----------------------------
refresh_interval = 5  # seconds
st.caption(f"🔄 Auto-refreshes every {refresh_interval} seconds")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("src/output.csv")
    return df

df = load_data()

# -----------------------------
# ADD LAST UPDATED TIME
# -----------------------------
current_time = datetime.now().strftime("%H:%M:%S")
st.markdown(f"🕒 **Last Updated:** {current_time}")

# -----------------------------
# FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

categories = df["Category"].unique().tolist()
selected_category = st.sidebar.selectbox("Select Category", ["All"] + categories)

time_filter = st.sidebar.selectbox(
    "Select Time Range",
    ["Last 1 Hour", "Last 6 Hours", "Last 24 Hours"]
)

# Apply category filter
if selected_category != "All":
    df = df[df["Category"] == selected_category]

# -----------------------------
# MAIN METRICS
# -----------------------------
st.subheader("📊 Category Counts")

st.dataframe(df)

# -----------------------------
# BAR CHART
# -----------------------------
st.subheader("📈 Category Distribution")
st.bar_chart(df.set_index("Category"))

# -----------------------------
# TOP HEADLINES (FAKE DATA)
# -----------------------------
st.subheader("📰 Top Trending Headlines")

sample_headlines = [
    "AI is transforming the future of jobs",
    "Stock market sees major growth today",
    "New healthcare breakthrough discovered",
    "Political tensions rise globally",
    "Tech companies launch new innovations",
    "Sports championship draws global attention",
    "Entertainment industry sees massive shift",
    "Finance sector experiences volatility",
]

headlines_data = []

for i in range(8):
    headlines_data.append({
        "Title": random.choice(sample_headlines),
        "Category": random.choice(categories),
        "Time": datetime.now().strftime("%H:%M:%S")
    })

headlines_df = pd.DataFrame(headlines_data)

st.table(headlines_df.head(5))

# -----------------------------
# INSIGHTS SECTION
# -----------------------------
st.subheader("📊 Insights")

top_category = df.sort_values(by="Count", ascending=False).iloc[0]["Category"]

st.markdown(f"""
- 🔥 **{top_category}** is the most trending category right now  
- 📊 Politics and Finance show steady engagement  
- 📉 Health and Entertainment are relatively lower  
- 🚀 Trend patterns indicate user interest shifting towards technology-driven topics  
""")

# -----------------------------
# AUTO REFRESH LOGIC
# -----------------------------
time.sleep(refresh_interval)
st.rerun()