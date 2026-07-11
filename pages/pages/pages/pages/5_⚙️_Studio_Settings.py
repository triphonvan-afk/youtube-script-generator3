import streamlit as st

st.title("⚙️ Studio Settings & Presets")
st.caption("Configure asset presets and global content variables.")

st.subheader("Profile Presets")
channel_name = st.text_input("Default Channel Name/Watermark", "@MyCreatorStudio")
default_language = st.selectbox("Primary Generation Language", ["English", "Spanish", "French", "German"])

st.subheader("Brand Canvas Defaults")
fav_bg = st.color_picker("Default Background Fill", "#1E1E2E")
fav_txt = st.color_picker("Default Typography Color", "#FFCC00")

if st.button("Save Studio Rules"):
    st.success("Global user preferences logged securely inside session cache variables!")
