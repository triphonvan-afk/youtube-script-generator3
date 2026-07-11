import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import urllib.request
import datetime
import pandas as pd
import numpy as np
import os

# --- APP VIEWPORT SETUP ---
st.set_page_config(page_title="Ultimate Content Studio", layout="wide")

# --- INITIALIZE GLOBAL CACHE VARIABLES ---
if "current_page_idx" not in st.session_state:
    st.session_state.current_page_idx = 0
if "studio_theme" not in st.session_state:
    st.session_state.studio_theme = "Amethyst Dark"
if "downloaded_web_bg" not in st.session_state:
    st.session_state.downloaded_web_bg = None

# --- SIDEBAR: INTERFACE SYSTEM THEME SWITCHER ---
st.sidebar.header("⚙️ Studio Core Config")
selected_ui_theme = st.sidebar.selectbox(
    "Application Accent Theme", 
    ["Amethyst Dark", "Sapphire Neon"], 
    index=0 if st.session_state.studio_theme == "Amethyst Dark" else 1
)
st.session_state.studio_theme = selected_ui_theme

# Apply dynamic CSS buttons styling based on theme choice
if st.session_state.studio_theme == "Sapphire Neon":
    st.markdown("<style>.stButton>button{background-color: #00E5FF !important; color:black !important; font-weight:bold;}</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>.stButton>button{background-color: #9D4EDD !important; color:white !important; font-weight:bold;}</style>", unsafe_allow_html=True)

# --- SIDEBAR: INTEGRATED MULTI-PAGE MENU NAVIGATION ---
page_names = [
    "🎬 Main Studio Canvas",
    "🎥 Production Scheduler",
    "📊 Analytics Tracker",
    "🔥 Viral Trend Finder",
    "⚙️ Studio Settings"
]

st.sidebar.subheader("📱 Navigation Panel Menu")
# Sync sidebar selector with our Next/Back button indices
chosen_sidebar_page = st.sidebar.radio(
    "Go To Workspace Tab:", 
    page_names, 
    index=st.session_state.current_page_idx,
    key="sidebar_navigation_radio_key"
)

# Update state matching menu clicks
st.session_state.current_page_idx = page_names.index(chosen_sidebar_page)

# --- HELPER LOGIC FOR TEXT BUTTON NAVIGATION ---
def shift_to_next():
    if st.session_state.current_page_idx < len(page_names) - 1:
        st.session_state.current_page_idx += 1
        st.rerun()

def shift_to_back():
    if st.session_state.current_page_idx > 0:
        st.session_state.current_page_idx -= 1
        st.rerun()

# --- FONTS ENGINE MANAGEMENT ---
@st.cache_data
def fetch_font_from_web(url, target_filename):
    if not os.path.exists(target_filename):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(target_filename, 'wb') as out_file:
                out_file.write(response.read())
        except Exception:
            return None
    return target_filename

def get_selected_font_object(style_string, size):
    font_urls = {
        "Ultra-Heavy Block (Anton)": "https://github.com",
        "Sleek Cyberpunk": "https://github.com",
        "Classic Geometric Bold": "https://github.com",
        "Retro Serif Bold": "https://github.com",
        "Elegant Script Modern": "https://github.com",
        "Futuristic Tech Accent": "https://github.com"
    }
    file_names = {
        "Ultra-Heavy Block (Anton)": "Anton-Regular.ttf",
        "Sleek Cyberpunk": "TechMono.ttf",
        "Classic Geometric Bold": "Kanit-Black.ttf",
        "Retro Serif Bold": "Cinzel-Black.ttf",
        "Elegant Script Modern": "Satisfy.ttf",
        "Futuristic Tech Accent": "Orbitron.ttf"
    }
    url = font_urls[style_string]
    filename = file_names[style_string]
    downloaded_path = fetch_font_from_web(url, filename)
    if downloaded_path and os.path.exists(downloaded_path):
        try:
            return ImageFont.truetype(downloaded_path, size)
        except Exception:
                if st.button("🔍 Source Background From Internet"):
        if search_query:
            with st.spinner(f"Connecting to live media indexes to fetch '{search_query}'..."):
                try:
                    # Clean spaces into commas for the public network engine
                    formatted_query = search_query.replace(" ", ",")
                    
                    # Direct unauthenticated 1280x720 video canvas landscape route
                    source_url = f"https://loremflickr.com{formatted_query}"
                    temp_img_path = "downloaded_bg.jpg"
                    
                    # Stream background pixels down into the local cache safely
                    req = urllib.request.Request(source_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response, open(temp_img_path, 'wb') as out_file:
                        out_file.write(response.read())
                        
                    st.session_state.downloaded_web_bg = temp_img_path
                    st.success("🎉 Photo successfully downloaded over public image node!")
                except Exception as e:
                    st.error(f"Network Download Blocked: {str(e)}")

        draw.rectangle([(0, max(0, start_y - banner_padding_v)), (1280, min(720, start_y + total_text_height + banner_padding_v - 10))], fill=bnr_hex)
    current_y = start_y
    for line in wrapped_lines:
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        text_width = right - left
        x_position = (1280 - text_width) // 2
        shadow_offset = max(3, int(selected_size * 0.08))
        for sx in range(-shadow_offset, shadow_offset + 1):
            for sy in range(-shadow_offset, shadow_offset + 1):
                if abs(sx) > shadow_offset - 2 or abs(sy) > shadow_offset - 2:
                    draw.text((x_position + sx, current_y + sy), line, fill=shd_hex, font=font)
        draw.text((x_position, current_y), line, fill=txt_hex, font=font)
        current_y += line_height
    draw.rectangle([(0, 705), (1280, 720)], fill="#FF0000") 
    return img


# =====================================================================
# --- RENDER LOGIC WORKSPACE SWITCH DEPOT ---
# =====================================================================

# --- WORKSPACE 1: MAIN DESIGN CANVAS STUDIO ---
if st.session_state.current_page_idx == 0:
    st.title("🎨 Pro Short-Form Thumbnail Studio")
    st.caption("Design advanced high-contrast image layouts locally with real-time vector adjustments.")
    
    st.sidebar.subheader("🎨 Canvas Controls")
    bg_color = st.sidebar.color_picker("Fallback Canvas Color", "#1E1E2E")
    text_color = st.sidebar.color_picker("Headline Text Color", "#FFCC00")
    shadow_color = st.sidebar.color_picker("3D Outline Drop-Shadow Color", "#000000")
    
    st.sidebar.subheader("📐 Custom Formatting Adjustments")
    font_choice = st.sidebar.selectbox("Headline Font Style Asset", ["Ultra-Heavy Block (Anton)", "Sleek Cyberpunk", "Classic Geometric Bold", "Retro Serif Bold", "Elegant Script Modern", "Futuristic Tech Accent"])
    font_size = st.sidebar.slider("Font Vector Size Scale", min_value=40, max_value=300, value=150, step=5)
    line_width = st.sidebar.slider("Characters Per Line (Wrap)", min_value=5, max_value=25, value=11, step=1)
    text_y_position = st.sidebar.slider("Vertical Alignment Offset", min_value=50, max_value=650, value=360, step=10)
    
    st.sidebar.subheader("🏷️ Banner Layer Accents")
    use_banner = st.sidebar.checkbox("Enable Solid Text Backdrop Accent Banner", value=False)
    banner_color = st.sidebar.color_picker("Backdrop Banner Color", "#000000")
    
    st.subheader("🌐 Live Internet Background Sourcing Core")
    search_query = st.text_input("Type an internet keyword search prompt to load a background live:", value="", placeholder="e.g., gaming setup, space galaxy, drift car")
    
    if st.button("🔍 Source Background From Internet"):
        if search_query:
            with st.spinner(f"Connecting to live media indexes to fetch '{search_query}'..."):
                try:
                    formatted_query = search_query.replace(" ", "-")
                    source_url = f"https://unsplash.com?{formatted_query}"
                    temp_img_path = "downloaded_bg.jpg"
                    req = urllib.request.Request(source_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response, open(temp_img_path, 'wb') as out_file:
                        out_file.write(response.read())
                    st.session_state.downloaded_web_bg = temp_img_path
                    st.success("🎉 Photo successfully downloaded over open web socket!")
                except Exception:
                    try:
                        default_url = "https://unsplash.com"
                        req = urllib.request.Request(default_url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req) as response, open("downloaded_bg.jpg", 'wb') as out_file:
                            out_file.write(response.read())
                        st.session_state.downloaded_web_bg = "downloaded_bg.jpg"
                        st.info("Loaded high-quality abstract vector texture background.")
                    except Exception as e:
                        st.error(f"Network Timeout Error: {str(e)}")
                        
    if st.session_state.downloaded_web_bg:
        if st.button("❌ Wipe Internet Image (Return to Fallback Color)"):
            st.session_state.downloaded_web_bg = None
            st.rerun()
            
    thumbnail_text = st.text_input("Type Your Thumbnail Headline Title Text Here:", value="SECRET TRICKS")
    
