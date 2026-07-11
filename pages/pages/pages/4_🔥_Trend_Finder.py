import streamlit as st

st.title("🔥 Viral Topic & Trend Finder")
st.caption("Locate breaking search niches to target for high-traffic script retention.")

niche = st.selectbox("Your Channel Theme", ["Tech & Gadgets", "Finance & Money", "Gaming", "Life Hacks"])

st.subheader(f"Trending Frameworks in {niche}")

trends = {
    "Tech & Gadgets": ["Why 2026 Smart Devices are Failing", "Hidden Desktop Setup Features", "The Cleanest Minimal Keyboard Layouts"],
    "Finance & Money": ["High Yield Savings Accounts Secrets", "How Index Funds Work Simply", "Side Hustles to Start Tonight"],
    "Gaming": ["Secret Easter Eggs in Trending Games", "Hardware Configurations for Max FPS", "Speedrun Strategies Broken Down"],
    "Life Hacks": ["Kitchen Organization Tricks", "Travel Packaging Compressed Hacks", "Study Workflow Techniques That Work"]
}

for index, trend in enumerate(trends[niche], 1):
    st.info(f"⚡ **Trend #{index}:** {trend}")
    if st.button(f"Draft Script for #{index}", key=f"btn_{index}"):
        st.success("Topic queued! Head back to the Main Studio page to run the AI engine.")
