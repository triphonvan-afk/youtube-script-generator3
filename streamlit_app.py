import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import urllib.request
import os

# --- APP LAYOUT INITIALIZATION ---
st.set_page_config(page_title="Shorts Thumbnail Studio", layout="wide")
st.title("🎨 Shorts Thumbnail Studio")
st.caption("Design ultra-high impact YouTube landscape templates locally with zero API limits.")

# --- SIDEBAR: DESIGN CONFIGURATION ---
st.sidebar.header("🎨 Styling Options")
bg_color = st.sidebar.color_picker("Thumbnail Background Color", "#1E1E2E")
text_color = st.sidebar.color_picker("Thumbnail Text Color", "#FFCC00")

# --- EXTENDED MASSIVE FONT SLIDERS ---
font_size = st.sidebar.slider("Font Size", min_value=40, max_value=300, value=180, step=5)
line_width = st.sidebar.slider("Characters Per Line (Wrap)", min_value=5, max_value=25, value=10, step=1)

# --- MAIN FORM INPUT ---
# This input prints directly to the canvas in real-time
thumbnail_text = st.text_input(
    "Type Your Thumbnail Headline Text Here:", 
    value="3 SECRET TRICKS",
    placeholder="e.g., STOP TYPING LIKE THIS!"
)

# --- CORE LOGIC: ULTRA-HEAVY WEB FONT LOADER ---
@st.cache_data
def load_heavy_font():
    """Downloads an ultra-thick, blocky viral web font directly into application root space"""
    font_path = "Anton-Regular.ttf"
    if not os.path.exists(font_path):
        url = "https://github.com"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(font_path, 'wb') as out_file:
                out_file.write(response.read())
        except Exception:
            return "impact.ttf" if os.path.exists("impact.ttf") else None
    return font_path

# --- CORE LOGIC: MASSIVE TYPOGRAPHY THUMBNAIL GENERATION ---
def generate_thumbnail(title_text, bg_hex, text_hex, selected_font_size, selected_wrap_width):
    # 1. Initialize Canvas (1280x720 standard landscape layout)
    img = Image.new("RGB", (1280, 720), color=bg_hex)
    draw = ImageDraw.Draw(img)
    
    # 2. Add Aggressive Black Gradient vignette for extreme typography pop
    for y in range(720):
        fade_factor = int((y / 720) * 140) 
        draw.line([(0, y), (1280, y)], fill=(0, 0, 0, fade_factor))
        
    # 3. Load the ultra-heavy block font asset natively
    font_file = load_heavy_font()
    if font_file:
        try:
            font = ImageFont.truetype(font_file, selected_font_size)
        except Exception:
            font = ImageFont.load_default()
    else:
        font = ImageFont.load_default()

    # Wrap the text tightly using slider criteria
    wrapped_lines = textwrap.wrap(title_text.upper(), width=selected_wrap_width)
    
    # 4. Math Center Calculation Geometry for Giant Typography
    line_height = selected_font_size + 10
    total_text_height = len(wrapped_lines) * line_height
    y_offset = (720 - total_text_height) // 2
    
    # Complete baseline fallback text render bypass if system falls to default tiny font
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

# --- EXECUTION RENDER ACTIONS ---
if st.button("🚀 Render Custom Canvas Layout", type="primary"):
    if not thumbnail_text:
        st.warning("Please type your banner title first!")
    else:
        with st.spinner("Processing raster layouts and anchoring layers..."):
            # Output mega-scale canvas configurations
            thumbnail_img = generate_thumbnail(thumbnail_text, bg_color, text_color, font_size, line_width)
            
            # Show canvas center view
            st.image(thumbnail_img, use_container_width=True)
            
            # Setup immediate image download tracking
            thumbnail_img.save("temp_thumb.png")
            with open("temp_thumb.png", "rb") as file:
                st.download_button(
                    label="💾 Download Finished Thumbnail PNG",
                    data=file,
                    file_name="youtube_thumbnail.png",
                    mime="image/png"
                )
