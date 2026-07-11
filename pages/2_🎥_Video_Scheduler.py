import streamlit as st
import datetime

st.title("📅 Production & Posting Scheduler")
st.caption("Plan your short-form content output pipeline across platforms.")

col1, col2 = st.columns(2)
with col1:
    title = st.text_input("Video Title Placeholder", "My Next Viral Short")
    platform = st.multiselect("Target Platforms", ["YouTube Shorts", "TikTok", "Instagram Reels"])
with col2:
    date = st.date_input("Scheduled Post Date", datetime.date.today())
    time = st.time_input("Target Posting Time")

if st.button("Add to Content Calendar", type="primary"):
    st.success(f"📌 '{title}' successfully mapped for upload on {date}!")
