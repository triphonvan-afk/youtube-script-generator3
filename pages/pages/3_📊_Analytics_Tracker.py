import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 Performance & Analytics Dashboard")
st.caption("Track retention metrics and view counts across your library.")

# Mock up data metrics
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['YouTube Views', 'TikTok Plays', 'Reels Reach']
)

st.subheader("Growth Momentum Trends")
st.line_chart(chart_data)

col1, col2, col3 = st.columns(3)
col1.metric("Total Library Views", "245.8K", "+12%")
col2.metric("Average Watch Retention", "84.2%", "+3.1%")
col3.metric("Subscriber Conversions", "+1,420", "+8%")
