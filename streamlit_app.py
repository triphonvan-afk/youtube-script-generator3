import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import urllib.request
import os

# --- APP LAYOUT INITIALIZATION ---
st.set_page_config(page_title="Pro Thumbnail Design Studio", layout="wide")
st.title("🔥 Pro Short-Form Thumbnail Studio")
st.caption("Craft highly advanced, clickable video layout vectors with layer positioning, banners, and font maps.")

# --- SIDEBAR: DESIGN GRAPHICS ENGINE ---
st.sidebar.header("🖼️ Layer Configurations")
uploaded_bg = st.sidebar.file_uploader("Upload Background Wallpaper", type=["png", "jpg", "jpeg"])

st.sidebar.subheader("🎨 Palette Controls")
text_color = st.sidebar.color_picker("Main Headline Text Color", "#FFCC00")
shadow_color = st.sidebar.color_picker("Drop-Shadow / Outline Color", "#000000")
fallback_bg = st.sidebar.color_picker("Fallback Backdrop Color (If no image uploaded)", "#1E1E2E")

st.sidebar.subheader("🏷️ Text Box Accent Banner")
use_banner = st.sidebar.checkbox("Enable Solid Text Background Banner", value=False)
banner_color = st.sidebar.color_picker("Banner Accent Color", "#000000")

st.sidebar.subheader("📐 Positioning & Typography")
# Feature 1 & 3: Interactive alignment parameters and style selectors
text_y_position = st.sidebar.slider("Vertical Text Alignment (Height Offset)", min_value=50, max_value=650, value=360, step=10)
font_choice = st.sidebar.selectbox("Typography Font Style Asset", ["Ultra-Heavy Impact (Anton)", "Sleek Cyberpunk", "Classic Geometric Bold", "Retro Serif Bold"])
font_size = st.sidebar.slider("Font Size Scale", min_value=40, max_value=300, value=150, step=5)
line_width = st.sidebar.slider("Characters Per Line (Wrap Boundaries)", min_value=5, max_value=25, value=11, step=1)

# --- MAIN WORKSPACE INTERFACE ---
thumbnail_text = st.text_input(
    "Type Your Thumbnail Headline Text Here:", 
    value="100 DAYS IN HARDCORE",
    placeholder="e.g., STOP TYPING LIKE THIS!"
)

# --- CORE LOGIC: ADVANCED MULTI-FONT REPOSITORY MANAGERS ---
@st.cache_data
def fetch_font_from_web(url, target_filename):
    """Downloads explicit true type fonts directly from open-source branches"""
    if not os.path.exists(target_filename):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(target_filename, 'wb') as out_file:
                out_file.write(response.read())
        except Exception:
            return None
    return target_filename

def get_selected_font_object(style_string, size):
    """Maps user selection dropdown directly into active graphic compiler fonts"""
    font_urls = {
        "Ultra-Heavy Impact (Anton)": "https://github.com",
        "Sleek Cyberpunk": "https://github.com",
        "Classic Geometric Bold": "https://github.com",
        "Retro Serif Bold": "https://github.com"
    }
    file_names = {
        "Ultra-Heavy Impact (Anton)": "Anton-Regular.ttf",
        "Sleek Cyberpunk": "TechMono.ttf",
        "Classic Geometric Bold": "Kanit-Black.ttf",
        "Retro Serif Bold": "Cinzel-Black.ttf"
    }
    
    url = font_urls[style_string]
    filename = file_names[style_string]
    
    downloaded_path = fetch_font_from_web(url, filename)
    if downloaded_path and os.path.exists(downloaded_path):
        try:
            return ImageFont.truetype(downloaded_path, size)
        except Exception:
            pass
            
    # System recovery defaults if web drops out
    try:
        return ImageFont.truetype("arialbd.ttf", size)
    except IOError:
        return ImageFont.load_default()

# --- CORE LOGIC: PREMIUM THUMBNAIL LAYOUT ENGINE ---
def generate_advanced_thumbnail(title_text, bg_hex, txt_hex, shd_hex, bnr_hex, selected_size, selected_wrap, bg_file, y_pos, bnr_active, chosen_font_style):
    # 1. Base Canvas Preparation
    if bg_file is not None:
        img = Image.open(bg_file).convert("RGB")
        img = img.resize((1280, 720), Image.Resampling.LANCZOS)
    else:
        img = Image.new("RGB", (1280, 720), color=bg_hex)
        
    draw = ImageDraw.Draw(img)
    
    # 2. Cinematic Darkness Gradient Vignette Overlap
    for y in range(720):
        fade_factor = int((y / 720) * 130) 
        draw.line([(0, y), (1280, y)], fill=(0, 0, 0, fade_factor))
        
    # 3. Dynamic Font Ingestion Layer
    font = get_selected_font_object(chosen_font_style, selected_size)
    wrapped_lines = textwrap.wrap(title_text.upper(), width=selected_wrap)
    
    line_height = selected_size + 15
    total_text_height = len(wrapped_lines) * line_height
    
    # Calculate baseline vertical point matching our sidebar alignment slider
    start_y = y_pos - (total_text_height // 2)
    
    # Safe system break recovery map
    if font.getname() == 'ImageFont':
        for line in wrapped_lines:
            draw.text((100, start_y), line, fill=txt_hex)
            start_y += 30
        return img

    # Feature 2: Generate Solid Structural Layout Accent Banners behind words
    if bnr_active:
        banner_padding_v = 30
        banner_top = max(0, start_y - banner_padding_v)
        banner_bottom = min(720, start_y + total_text_height + banner_padding_v - 10)
        draw.rectangle([(0, banner_top), (1280, banner_bottom)], fill=bnr_hex)

    # 4. Draw Core Typography Maps
    current_y = start_y
    for line in wrapped_lines:
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        text_width = right - left
        x_position = (1280 - text_width) // 2
        
        # Feature 4: Custom Configurable 3D Drop Shadows
        shadow_offset = max(3, int(selected_size * 0.08))
        for sx in range(-shadow_offset, shadow_offset + 1):
            for sy in range(-shadow_offset, shadow_offset + 1):
                if abs(sx) > shadow_offset - 2 or abs(sy) > shadow_offset - 2:
                    draw.text((x_position + sx, current_y + sy), line, fill=shd_hex, font=font)
                
        # Primary Foreground Text Stamp
        draw.text((x_position, current_y), line, fill=txt_hex, font=font)
        current_y += line_height
        
    # 5. Bright Accent Anchor Footer Strip
    draw.rectangle([(0, 705), (1280, 720)], fill="#FF0000") 
    return img

# --- EXECUTION RENDER RUNNER ---
if st.button("🚀 Render Studio Layout Canvas", type="primary"):
    if not thumbnail_text:
        st.warning("Please type your canvas headline banner content first!")
    else:
        with st.spinner("Compiling image textures, mapping dimensions, and baking vector arrays..."):
            
            # Execute advanced composite graphics generation pipeline
            thumbnail_img = generate_advanced_thumbnail(
                thumbnail_text, fallback_bg, text_color, shadow_color, banner_color,
                font_size, line_width, uploaded_bg, text_y_position, use_banner, font_choice
            )
            
            # Render finished layout window block directly to client dashboard
            st.image(thumbnail_img, use_container_width=True)
            
            # Mount direct local disk downloading pipelines
            thumbnail_img.save("temp_thumb.png")
            with open("temp_thumb.png", "rb") as file:
                st.download_button(
                    label="💾 Download Finished Production PNG",
                    data=file,
                    file_name="youtube_thumbnail_pro.png",
                    mime="image/png"
                )
