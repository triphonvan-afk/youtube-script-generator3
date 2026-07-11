import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import google.genai as genai
import textwrap
import os

# --- APP LAYOUT INITIALIZATION ---
st.set_page_config(page_title="Shorts Script & Thumbnail Gen", layout="wide")
st.title("🎬 Shorts Script & Thumbnail Studio")
st.caption("Generate engaging multi-scene vertical scripts and a matching YouTube thumbnail.")

# --- SIDEBAR: DESIGN CONFIGURATION ---
st.sidebar.header("🎨 Styling Options")
bg_color = st.sidebar.color_picker("Thumbnail Background Color", "#1E1E2E")
text_color = st.sidebar.color_picker("Thumbnail Text Color", "#FFCC00")

# --- AUTO-LOAD SECURE API KEY ---
api_key = st.secrets.get("GEMINI_API_KEY", "")

if api_key:
    st.sidebar.success("🔒 Gemini AI Connected Automatically!")
else:
    st.sidebar.warning("⚠️ No Key Found! Configure Secrets in Streamlit Settings.")

# --- MAIN FORM INPUT ---
topic = st.text_input("What is your YouTube Short about?", placeholder="e.g., 3 Hidden Features of iPhones No One Uses")
hook_style = st.selectbox("Script Tone/Hook Style", ["Dramatic & Suspenseful", "Energetic & Fast-Paced", "Educational & Casual"])

# --- CORE LOGIC: MASSIVE TYPOGRAPHY THUMBNAIL GENERATION ---
def generate_thumbnail(title_text, bg_hex, text_hex):
    # 1. Initialize Canvas (1280x720 standard landscape layout)
    img = Image.new("RGB", (1280, 720), color=bg_hex)
    draw = ImageDraw.Draw(img)
    
    # 2. Add Linear Gradient Overlap for Contrast Depth
    for y in range(720):
        fade_factor = int((y / 720) * 95) 
        draw.line([(0, y), (1280, y)], fill=(0, 0, 0, fade_factor))
        
    # 3. Load Heavy High-Impact Fonts at a Massive Size (130px)
    font_size = 130
    try:
        font = ImageFont.truetype("impact.ttf", font_size)
    except IOError:
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

    # Wrap the text tighter (width=12) so fewer big words fit per line
    wrapped_lines = textwrap.wrap(title_text.upper(), width=12)
    
    # 4. Balanced Center Calculation Geometry for Large Fonts
    line_height = font_size + 15
    total_text_height = len(wrapped_lines) * line_height
    y_offset = (720 - total_text_height) // 2 - 20
    
    for line in wrapped_lines:
        # Pinpoint visual center coordinates
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        text_width = right - left
        x_position = (1280 - text_width) // 2
        
        # 5. Heavy 8-Pixel Drop-Shadow for Instant Text Legibility
        shadow_offset = 8
        for sx in [-shadow_offset, shadow_offset]:
            for sy in [-shadow_offset, shadow_offset]:
                draw.text((x_position + sx, y_offset + sy), line, fill="#000000", font=font)
                
        # 6. Primary Text Layer Stamp
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
                
                thumbnail_img = generate_thumbnail(clean_title, bg_color, text_color)
                st.image(thumbnail_img, use_container_width=True)
                
                thumbnail_img.save("temp_thumb.png")
                with open("temp_thumb.png", "rb") as file:
                    st.download_button(
                        label="💾 Download Thumbnail PNG",
                        data=file,
                        file_name="youtube_thumbnail.png",
                        mime="image/png"
                    )
