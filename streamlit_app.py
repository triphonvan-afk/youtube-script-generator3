import streamlit as st

# Define individual page modules accurately
# This isolates execution so page 1 doesn't run into a loop
page_1 = st.Page("pages/1_🎬_Main_Studio.py", title="Main Studio Canvas", icon="🎬", default=True)
page_2 = st.Page("pages/2_🎥_Video_Scheduler.py", title="Video Scheduler", icon="🎥")
page_3 = st.Page("pages/3_📊_Analytics_Tracker.py", title="Analytics Tracker", icon="📊")
page_4 = st.Page("pages/4_🔥_Trend_Finder.py", title="Trend Finder", icon="🔥")
page_5 = st.Page("pages/5_⚙️_Studio_Settings.py", title="Studio Settings", icon="⚙️")

# Build the structural sidebar map cleanly 
pg = st.navigation([page_1, page_2, page_3, page_4, page_5])

# Trigger routing cleanly
pg.run()
