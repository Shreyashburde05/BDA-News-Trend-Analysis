import streamlit as st
import pandas as pd

st.set_page_config(page_title="News Trends Dashboard", layout="wide")

st.title("📊 Real-Time News Trends Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("src/output.csv")

df = load_data()

st.subheader("📌 Top Categories")

st.dataframe(df)

st.subheader("📊 Category Distribution")

st.bar_chart(df.set_index("Category"))

st.subheader("📈 Insights")

top_category = df.sort_values(by="Count", ascending=False).iloc[0]

st.success(f"🔥 Most Trending Category: {top_category['Category']} with {top_category['Count']} articles")

st.info("This dashboard updates when new data is processed.")