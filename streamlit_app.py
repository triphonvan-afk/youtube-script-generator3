
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import google.genai as genai
import textwrap
import os

# --- APP LAYOUT INITIALIZATION ---
st.set_page_config(page_title="Shorts Script & Thumbnail Gen", layout="wide")
st.title("🎬 Shorts Script & Thumbnail Studio")
st.caption("Generate engaging multi-scene vertical scripts and a matching YouTube thumbnail.")

# --- SIDEBAR: CONFIGURATION & CREDENTIALS ---
st.sidebar.header("🔑 Setup & Styling")
api_key = st.sidebar.text_input("Google Gemini API Key", type="password")
bg_color = st.sidebar.color_picker("Thumbnail Background Color", "#1E1E2E")
text_color = st.sidebar.color_picker("Thumbnail Text Color", "#FFCC00")

# --- MAIN FORM INPUT ---
topic = st.text_input("What is your YouTube Short about?", placeholder="e.g., 3 Hidden Features of iPhones No One Uses")
hook_style = st.selectbox("Script Tone/Hook Style", ["Dramatic & Suspenseful", "Energetic & Fast-Paced", "Educational & Casual"])

# --- CORE LOGIC: UPGRADED THUMBNAIL GENERATION ---
def generate_thumbnail(title_text, bg_hex, text_hex):
    # 1. Initialize a High-Resolution Canvas (1280x720 landscape layout)
    img = Image.new("RGB", (1280, 720), color=bg_hex)
    draw = ImageDraw.Draw(img)
    
    # 2. Add an Advanced Linear Gradient Overlap for Premium Texture
    for y in range(720):
        fade_factor = int((y / 720) * 85) 
        draw.line([(0, y), (1280, y)], fill=(0, 0, 0, fade_factor))
        
    # 3. Handle Modern Impact Styling Configurations
    try:
        font = ImageFont.truetype("impact.ttf", 95)
    except IOError:
        try:
            font = ImageFont.truetype("arialbd.ttf", 95)
        except IOError:
            font = ImageFont.load_default()

    # Clean text constraints to keep layouts punchy
    wrapped_lines = textwrap.wrap(title_text.upper(), width=16)
    
    # 4. Center Calculation Geometry
    y_offset = 360 - (len(wrapped_lines) * 55)
    
    for line in wrapped_lines:
        # Track literal bounding box coordinates to pinpoint visual canvas center
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        text_width = right - left
        x_position = (1280 - text_width) // 2
        
        # 5. Render Heavy Cinematic Drop-Shadow Border
        shadow_offset = 6
        for sx in [-shadow_offset, shadow_offset]:
            for sy in [-shadow_offset, shadow_offset]:
                draw.text((x_position + sx, y_offset + sy), line, fill="#000000", font=font)
                
        # 6. Primary Overlay Text Stamp
        draw.text((x_position, y_offset), line, fill=text_hex, font=font)
        y_offset += 115
        
    # 7. Add an Ultra-Bright Red Bottom Anchor Accent Block
    draw.rectangle([(0, 710), (1280, 720)], fill="#FF0000") 
    return img

# --- CORE LOGIC: AI SCRIPT GENERATION ---
def fetch_ai_script(prompt_topic, tone, key):
    if not key:
        return "Please input a valid Google API Key in the left sidebar configuration panel."
        
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
        st.error("Missing API Key! Please configure the sidebar settings.")
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
