import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import google.genai as genai
import textwrap
import urllib.request
import os

# --- DEFINE DYNAMIC MULTI-PAGE NAVIGATION MAP ---
main_page = st.Page("streamlit_app.py", title="🎬 Main Studio Canvas", icon="🎬")

try:
    scheduler_page = st.Page("pages/2_🎥_Video_Scheduler.py", title="Video Scheduler", icon="🎥")
    analytics_page = st.Page("pages/3_📊_Analytics_Tracker.py", title="Analytics Tracker", icon="📊")
    trend_page = st.Page("pages/4_🔥_Trend_Finder.py", title="Trend Finder", icon="🔥")
    settings_page = st.Page("pages/5_⚙️_Studio_Settings.py", title="Studio Settings", icon="⚙️")
    pg = st.navigation([main_page, scheduler_page, analytics_page, trend_page, settings_page])
except Exception:
    pg = st.navigation([main_page])

pg.run()

# --- SIDEBAR: DESIGN CONFIGURATION ---
st.sidebar.header("🎨 Styling Options")
bg_color = st.sidebar.color_picker("Thumbnail Background Color", "#1E1E2E")
text_color = st.sidebar.color_picker("Thumbnail Text Color", "#FFCC00")

# --- EXTENDED MASSIVE FONT SLIDERS ---
# Maximum font scale expanded to 300px with a huge 180px default baseline
font_size = st.sidebar.slider("Font Size", min_value=40, max_value=300, value=180, step=5)
line_width = st.sidebar.slider("Characters Per Line (Wrap)", min_value=5, max_value=25, value=10, step=1)

# --- AUTO-LOAD SECURE API KEY ---
api_key = st.secrets.get("GEMINI_API_KEY", "")

if api_key:
    st.sidebar.success("🔒 Gemini AI Connected Automatically!")
else:
    st.sidebar.warning("⚠️ No Key Found! Configure Secrets in Streamlit Settings.")

# --- MAIN FORM INPUT ---
topic = st.text_input("What is your YouTube Short about?", placeholder="e.g., 3 Hidden Features of iPhones No One Uses")
hook_style = st.selectbox("Script Tone/Hook Style", ["Dramatic & Suspenseful", "Energetic & Fast-Paced", "Educational & Casual"])

# --- CORE LOGIC: ULTRA-HEAVY WEB FONT LOADER ---
@st.cache_data
def load_heavy_font():
    """Downloads an ultra-thick, blocky viral web font directly into application root space"""
    font_path = "Anton-Regular.ttf"
    if not os.path.exists(font_path):
        url = "https://github.com"
        try:
            # Set a modern browser header to completely bypass GitHub raw access blocks
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(font_path, 'wb') as out_file:
                out_file.write(response.read())
        except Exception:
            return "impact.ttf" if os.path.exists("impact.ttf") else None
    return font_path

def generate_thumbnail(title_text, bg_hex, text_hex, selected_font_size, selected_wrap_width):
    # 1. Initialize Canvas (1280x720 standard landscape layout)
    img = Image.new("RGB", (1280, 720), color=bg_hex)
    draw = ImageDraw.Draw(img)
    
    # 2. Add Aggressive Black Gradient vignette for extreme typography pop
    for y in range(720):
        fade_factor = int((y / 720) * 140) 
        draw.line([(0, y), (1280, y)], fill=(0, 0, 0, fade_factor))
        
    # 3. Load the ultra-heavy block font asset
    font_file = load_heavy_font()
    if font_file:
        try:
            font = ImageFont.truetype(font_file, selected_font_size)
        except Exception:
            font = ImageFont.load_default()
    else:
        font = ImageFont.load_default()

    # Wrap the text tightly so massive words build a vertical structural wall
    wrapped_lines = textwrap.wrap(title_text.upper(), width=selected_wrap_width)
    
    # 4. Math Center Calculation Geometry for Giant Typography
    line_height = selected_font_size + 10
    total_text_height = len(wrapped_lines) * line_height
    y_offset = (720 - total_text_height) // 2
    
    # Complete baseline text render bypass if system falls to default tiny font
    if font.getname() == 'ImageFont':
        for line in wrapped_lines:
            draw.text((100, y_offset), line, fill=text_hex)
            y_offset += 30
        return img
    
    for line in wrapped_lines:
        # Measure structural box coordinates to lock absolute center placement
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        text_width = right - left
        x_position = (1280 - text_width) // 2
        
        # 5. Colossal 3D Drop-Shadow (Scales up as font size expands)
        shadow_offset = max(4, int(selected_font_size * 0.08))
        for sx in range(-shadow_offset, shadow_offset + 1):
            for sy in range(-shadow_offset, shadow_offset + 1):
                if abs(sx) > shadow_offset - 2 or abs(sy) > shadow_offset - 2:
                    draw.text((x_position + sx, y_offset + sy), line, fill="#000000", font=font)
                
        # 6. Primary Overlay Text Stamp
        draw.text((x_position, y_offset), line, fill=text_hex, font=font)
        y_offset += line_height
        
    # 7. Bright Bottom Accent Strip
    draw.rectangle([(0, 705), (1280, 720)], fill="#FF0000") 
    return img

# --- CORE LOGIC: AI SCRIPT GENERATION ---
def fetch_ai_script(prompt_topic, tone, key):
    if not key:
        return "Please input a valid Google API Key in your Streamlit Cloud Secrets dashboard panel."
        
    try:
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Create a 60-second viral YouTube Shorts script about: '{prompt_topic}'. The style must be {tone}.\n\nInclude a suggested 4-5 word punchy text layout to print on a thumbnail image at the very end.",
        )
        return response.text
    except Exception as e:
        return f"API Connection Error: {str(e)}"

# --- EXECUTION ACTIONS ---
if st.button("🚀 Generate Content Assets", type="primary"):
    if not topic:
        st.warning("Please type a topic prompt first!")
    elif not api_key:
        st.error("Missing API Key! Please save your key in the Streamlit Cloud Secrets dashboard.")
    else:
        with st.spinner("AI is brainstorming scripts and rendering layouts..."):
            raw_script_output = fetch_ai_script(topic, hook_style, api_key)
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📜 Generated Shorts Script")
                st.text_area("Copy Script Text", value=raw_script_output, height=450)
                
            with col2:
                st.subheader("🖼️ Generated Video Thumbnail")
                clean_title = topic[:40] + "..." if len(topic) > 40 else topic
                
                # Output mega-scale canvas configurations
                thumbnail_img = generate_thumbnail(clean_title, bg_color, text_color, font_size, line_width)
                st.image(thumbnail_img, use_container_width=True)
                
                thumbnail_img.save("temp_thumb.png")
                with open("temp_thumb.png", "rb") as file:
                    st.download_button(
                        label="💾 Download Thumbnail PNG",
                        data=file,
                        file_name="youtube_thumbnail.png",
                        mime="image/png"
                    )
