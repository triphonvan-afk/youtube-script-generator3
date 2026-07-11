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

# Interactive Sliders for Custom Text Layouts
font_size = st.sidebar.slider("Font Size", min_value=40, max_value=200, value=110, step=5)
line_width = st.sidebar.slider("Characters Per Line (Wrap)", min_value=8, max_value=25, value=12, step=1)

# --- AUTO-LOAD SECURE API KEY ---
api_key = st.secrets.get("GEMINI_API_KEY", "")

if api_key:
    st.sidebar.success("🔒 Gemini AI Connected Automatically!")
else:
    st.sidebar.warning("⚠️ No Key Found! Configure Secrets in Streamlit Settings.")

# --- MAIN FORM INPUT ---
topic = st.text_input("What is your YouTube Short about?", placeholder="e.g., 3 Hidden Features of iPhones No One Uses")
hook_style = st.selectbox("Script Tone/Hook Style", ["Dramatic & Suspenseful", "Energetic & Fast-Paced", "Educational & Casual"])

# --- CORE LOGIC: COMPATIBLE SYSTEM FONT SELECTOR ---
def load_system_font(size):
    """Checks for standard, high-legibility bold system fonts across Linux/Windows/Mac layers"""
    font_options = [
        "arialbd.ttf",       # Windows/Mac Bold Arial
        "LiberationSans-Bold.ttf", # Standard Linux Server Bold Sans (Streamlit Native)
        "DejaVuSans-Bold.ttf", # Linux Fallback alternative
        "impact.ttf"         # Standard Impact Font
    ]
    
    for font_name in font_options:
        try:
            return ImageFont.truetype(font_name, size)
        except IOError:
            continue
            
    # Ultimate safe baseline if everything else fails
    return ImageFont.load_default()

def generate_thumbnail(title_text, bg_hex, text_hex, selected_font_size, selected_wrap_width):
    # 1. Initialize Canvas (1280x720 standard landscape layout)
    img = Image.new("RGB", (1280, 720), color=bg_hex)
    draw = ImageDraw.Draw(img)
    
    # 2. Add Linear Gradient Overlap for Contrast Depth
    for y in range(720):
        fade_factor = int((y / 720) * 110) 
        draw.line([(0, y), (1280, y)], fill=(0, 0, 0, fade_factor))
        
    # 3. Load the cross-platform bold layout font safely
    font = load_system_font(selected_font_size)

    # Wrap the text using the slider value chosen by the user
    wrapped_lines = textwrap.wrap(title_text.upper(), width=selected_wrap_width)
    
    # 4. Balanced Center Calculation Geometry
    line_height = selected_font_size + 20
    total_text_height = len(wrapped_lines) * line_height
    y_offset = (720 - total_text_height) // 2
    
    for line in wrapped_lines:
        # Pinpoint visual center coordinates
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        text_width = right - left
        x_position = (1280 - text_width) // 2
        
        # 5. Heavy Scaled Drop-Shadow proportional to the font size
        shadow_offset = max(3, int(selected_font_size * 0.07))
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
                
                # Pass sliders variables down to engine
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
