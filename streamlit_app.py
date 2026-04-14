import streamlit as st
import pandas as pd
import time
import warnings
import plotly.express as px

# Silence annoying deprecation warnings from Streamlit
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*use_container_width.*")
import plotly.graph_objects as go
from datetime import datetime
import os

# ------------------------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="NewsTrends AI | Real-Time Dashboard",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------------------
# SESSION STATE FOR TREND TRACKING
# ------------------------------------------------------------------------------
if 'prev_data' not in st.session_state:
    st.session_state.prev_data = {}

# ------------------------------------------------------------------------------
# CUSTOM CSS FOR MODERN UI + TICKER
# ------------------------------------------------------------------------------
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    
    /* Breaking News Ticker */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background-color: rgba(255, 75, 75, 0.1);
        padding: 10px 0;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 75, 75, 0.2);
    }
    .ticker {
        display: inline-block;
        white-space: nowrap;
        padding-right: 100%;
        animation: ticker 30s linear infinite;
        color: #FF4B4B;
        font-weight: bold;
        font-family: monospace;
        font-size: 1.1rem;
    }
    @keyframes ticker {
        0% { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }
    
    .main-header {
        font-size: 2.5rem; font-weight: 800; color: #FFFFFF;
        background: -webkit-linear-gradient(#00C9FF, #92FE9D);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05); padding: 1.5rem;
        border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center; transition: transform 0.3s ease;
    }
    .metric-value { font-size: 2.2rem; font-weight: 700; color: #00C9FF; }
    .trend-indicator { font-size: 1rem; margin-left: 5px; }
    .trend-up { color: #92FE9D; }
    .trend-down { color: #FF4B4B; }
    
    .content-section {
        background: rgba(255, 255, 255, 0.03); padding: 1.5rem;
        border-radius: 20px; margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# DATA LOADING LOGIC
# ------------------------------------------------------------------------------
def load_data():
    paths = ["src/output.csv", "output.csv"]
    for path in paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            if not df.empty: return df
    return pd.DataFrame(columns=["Category", "Count"])

# ------------------------------------------------------------------------------
# SIDEBAR / FILTERS
# ------------------------------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2540/2540832.png", width=80)
    st.markdown("<h2 style='color: white;'>NewsTrends AI</h2>", unsafe_allow_html=True)
    st.divider()
    refresh_rate = st.slider("Auto-Refresh Rate (sec)", 2, 30, 5)
    
    raw_df = load_data()
    all_categories = raw_df["Category"].unique().tolist() if not raw_df.empty else []
    selected_cat = st.multiselect("Filter by Category", options=all_categories, default=all_categories)
    
    st.sidebar.info("📡 Kafka Stream: ACTIVE")
    st.sidebar.caption("v2.1.0 | Real-Time Trend Analytics")

# ------------------------------------------------------------------------------
# MAIN DASHBOARD CONTENT
# ------------------------------------------------------------------------------
df = raw_df.copy()
if selected_cat and not df.empty:
    df = df[df["Category"].isin(selected_cat)]

# Ticker Tape Row
if not df.empty:
    ticker_text = " • ".join([f"🔥 BREAKING: {row['Category'].upper()} trending with {row['Count']:,} articles" for _, row in df.nlargest(3, 'Count').iterrows()])
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">{ticker_text} &nbsp;&nbsp;&nbsp; {ticker_text}</div></div>', unsafe_allow_html=True)

# Header Section
col_title, col_time = st.columns([3, 1])
with col_title:
    st.markdown("<h1 class='main-header'>Real-Time Trend Analytics</h1>", unsafe_allow_html=True)
with col_time:
    st.markdown(f"<div style='text-align: right; padding-top: 15px;'><span style='color: #B0B0B0;'>SYNC: </span><span style='color: #92FE9D; font-weight: bold;'>{datetime.now().strftime('%H:%M:%S')}</span></div>", unsafe_allow_html=True)

# KPI Row with Trend Detection
if not df.empty:
    total_articles = df["Count"].sum()
    top_row = df.sort_values("Count", ascending=False).iloc[0]
    top_cat = top_row["Category"]
    top_val = top_row["Count"]
    
    # Calculate Trends
    total_trend = ""
    if 'total' in st.session_state.prev_data:
        diff = total_articles - st.session_state.prev_data['total']
        if diff > 0: total_trend = f'<span class="trend-indicator trend-up">▲ +{diff:,}</span>'
        elif diff < 0: total_trend = f'<span class="trend-indicator trend-down">▼ {diff:,}</span>'
    
    st.session_state.prev_data['total'] = total_articles
    
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total News Pipeline</div><div class="metric-value">{total_articles:,}{total_trend}</div></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">🔥 Top Category</div><div class="metric-value">{top_cat.upper()}</div></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Peak Article Count</div><div class="metric-value">{top_val:,}</div></div>', unsafe_allow_html=True)
else:
    st.warning("⚠️ Waiting for Kafka data...")

st.markdown("<br>", unsafe_allow_html=True)

# Charts Row
if not df.empty:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("<div class='content-section'>", unsafe_allow_html=True)
        st.subheader("📈 Volume Distribution")
        fig_bar = px.bar(df, x="Category", y="Count", color="Count", template="plotly_dark", color_continuous_scale="Blues")
        fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=30,b=0), height=400)
        st.plotly_chart(fig_bar, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='content-section'>", unsafe_allow_html=True)
        st.subheader("📊 Market Share")
        fig_pie = px.pie(df, values='Count', names='Category', hole=.4, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Tealgrn_r)
        fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=30,b=0), height=400)
        st.plotly_chart(fig_pie, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

# Data Table
st.markdown("<div class='content-section'>", unsafe_allow_html=True)
st.subheader("📝 Live Category Breakdown")
st.dataframe(
    df.sort_values("Count", ascending=False),
    column_config={"Count": st.column_config.ProgressColumn("Volume", format="%d", min_value=0, max_value=int(df["Count"].max()) if not df.empty else 100)},
    hide_index=True, width="stretch"
)
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<br><hr><div style='text-align: center; color: #555;'>BDA Project | Real-Time News Trend Analysis | Spark & Kafka Stream v2.1</div>", unsafe_allow_html=True)

# Auto-Refresh
with st.spinner('Syncing with Kafka...'):
    time.sleep(refresh_rate)
    st.rerun()