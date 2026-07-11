import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import urllib.request
import urllib.parse
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


def shift_to_back():
    if st.session_state.current_page_idx > 0:
        st.session_state.current_page_idx -= 1


def render_nav_buttons():
    nav_col_back, nav_col_spacer, nav_col_next = st.columns([1, 4, 1])
    with nav_col_back:
        st.button("⬅️ Back", on_click=shift_to_back, disabled=st.session_state.current_page_idx == 0)
    with nav_col_next:
        st.button(
            "Next ➡️",
            on_click=shift_to_next,
            disabled=st.session_state.current_page_idx == len(page_names) - 1
        )


# --- FONTS ENGINE MANAGEMENT ---
# NOTE: These must point directly at raw .ttf/.otf file bytes, not HTML pages.
FONT_URLS = {
    "Ultra-Heavy Block (Anton)": "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf",
    "Sleek Cyberpunk": "https://github.com/google/fonts/raw/main/ofl/shareTechMono/ShareTechMono-Regular.ttf",
    "Classic Geometric Bold": "https://github.com/google/fonts/raw/main/ofl/kanit/Kanit-Black.ttf",
    "Retro Serif Bold": "https://github.com/google/fonts/raw/main/ofl/cinzel/Cinzel%5Bwght%5D.ttf",
    "Elegant Script Modern": "https://github.com/google/fonts/raw/main/ofl/satisfy/Satisfy-Regular.ttf",
    "Futuristic Tech Accent": "https://github.com/google/fonts/raw/main/ofl/orbitron/Orbitron%5Bwght%5D.ttf",
}

FONT_FILENAMES = {
    "Ultra-Heavy Block (Anton)": "Anton-Regular.ttf",
    "Sleek Cyberpunk": "ShareTechMono-Regular.ttf",
    "Classic Geometric Bold": "Kanit-Black.ttf",
    "Retro Serif Bold": "Cinzel-Black.ttf",
    "Elegant Script Modern": "Satisfy.ttf",
    "Futuristic Tech Accent": "Orbitron.ttf",
}


@st.cache_data
def fetch_font_from_web(url, target_filename):
    """Download a font file if not already cached locally. Returns the local
    path on success, or None if the download failed / didn't yield a usable
    font file."""
    if os.path.exists(target_filename) and os.path.getsize(target_filename) > 0:
        return target_filename
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=10) as response, open(target_filename, 'wb') as out_file:
            out_file.write(response.read())
        # Sanity check: a real font file should be more than a few KB.
        if os.path.getsize(target_filename) < 1024:
            os.remove(target_filename)
            return None
        return target_filename
    except Exception:
        if os.path.exists(target_filename):
            os.remove(target_filename)
        return None


def get_selected_font_object(style_string, size):
    url = FONT_URLS[style_string]
    filename = FONT_FILENAMES[style_string]
    downloaded_path = fetch_font_from_web(url, filename)
    if downloaded_path and os.path.exists(downloaded_path):
        try:
            return ImageFont.truetype(downloaded_path, size)
        except Exception:
            pass
    # Fallback: PIL's built-in bitmap font (fixed size, no .size attribute reliability)
    return ImageFont.load_default()


def is_fallback_font(font_obj):
    """Detect whether we ended up with PIL's built-in default font instead
    of a real TrueType font (the default font has no usable font file)."""
    return not hasattr(font_obj, "path")


# --- PREMIUM THUMBNAIL RENDER ENGINE ---
def generate_advanced_thumbnail(title_text, bg_hex, txt_hex, shd_hex, bnr_hex,
                                 selected_size, selected_wrap, web_bg_file,
                                 y_pos, bnr_active, chosen_font_style):
    if web_bg_file and os.path.exists(web_bg_file):
        try:
            img = Image.open(web_bg_file).convert("RGB")
            img = img.resize((1280, 720), Image.Resampling.LANCZOS)
        except Exception:
            img = Image.new("RGB", (1280, 720), color=bg_hex)
    else:
        img = Image.new("RGB", (1280, 720), color=bg_hex)

    # Add a dark vignette gradient for contrast. Plain RGB draw.line() ignores
    # alpha, so we composite a separate RGBA overlay instead.
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    for y in range(720):
        fade_factor = int((y / 720) * 130)
        overlay_draw.line([(0, y), (1280, y)], fill=(0, 0, 0, fade_factor))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    draw = ImageDraw.Draw(img)
    font = get_selected_font_object(chosen_font_style, selected_size)
    wrapped_lines = textwrap.wrap(title_text.upper(), width=selected_wrap) or [""]
    line_height = selected_size + 15
    total_text_height = len(wrapped_lines) * line_height
    start_y = y_pos - (total_text_height // 2)

    if is_fallback_font(font):
        # Degrade gracefully with the built-in bitmap font instead of the
        # full styled render pipeline (it can't be resized reliably).
        fallback_y = start_y
        for line in wrapped_lines:
            draw.text((100, fallback_y), line, fill=txt_hex)
            fallback_y += 30
        draw.rectangle([(0, 705), (1280, 720)], fill="#FF0000")
        return img

    if bnr_active:
        banner_padding_v = 30
        draw.rectangle(
            [(0, max(0, start_y - banner_padding_v)),
             (1280, min(720, start_y + total_text_height + banner_padding_v - 10))],
            fill=bnr_hex
        )

    current_y = start_y
    for line in wrapped_lines:
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        text_width = right - left
        x_position = (1280 - text_width) // 2

        # 3D drop shadow
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
    font_choice = st.sidebar.selectbox(
        "Headline Font Style Asset",
        ["Ultra-Heavy Block (Anton)", "Sleek Cyberpunk", "Classic Geometric Bold",
         "Retro Serif Bold", "Elegant Script Modern", "Futuristic Tech Accent"]
    )
    font_size = st.sidebar.slider("Font Vector Size Scale", min_value=40, max_value=300, value=150, step=5)
    line_width = st.sidebar.slider("Characters Per Line (Wrap)", min_value=5, max_value=25, value=11, step=1)
    text_y_position = st.sidebar.slider("Vertical Alignment Offset", min_value=50, max_value=650, value=360, step=10)

    st.sidebar.subheader("🏷️ Banner Layer Accents")
    use_banner = st.sidebar.checkbox("Enable Solid Text Backdrop Accent Banner", value=False)
    banner_color = st.sidebar.color_picker("Backdrop Banner Color", "#000000")

    st.subheader("🌐 Live Internet Background Sourcing Core")
    search_query = st.text_input(
        "Type an internet keyword search prompt to load a background live:",
        value="",
        placeholder="e.g., gaming setup, space galaxy, drift car"
    )

    if st.button("🔍 Source Background From Internet"):
        if search_query:
            with st.spinner(f"Connecting to live media indexes to fetch '{search_query}'..."):
                try:
                    # loremflickr expects /<width>/<height>/<comma,separated,tags>
                    formatted_query = urllib.parse.quote(search_query.strip().replace(" ", ","))
                    source_url = f"https://loremflickr.com/1280/720/{formatted_query}"
                    temp_img_path = "downloaded_bg.jpg"

                    req = urllib.request.Request(source_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                    with urllib.request.urlopen(req, timeout=10) as response, open(temp_img_path, 'wb') as out_file:
                        out_file.write(response.read())

                    st.session_state.downloaded_web_bg = temp_img_path
                    st.success("🎉 Photo successfully downloaded over public image node!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Network Download Blocked: {str(e)}")
        else:
            st.warning("Enter a search keyword first.")

    if st.session_state.downloaded_web_bg:
        if st.button("❌ Wipe Internet Image (Return to Fallback Color)"):
            st.session_state.downloaded_web_bg = None
            st.rerun()

    thumbnail_text = st.text_input("Type Your Thumbnail Headline Title Text Here:", value="SECRET TRICKS")

    # REAL-TIME RENDER: Generates canvas immediately upon UI changes
    st.write("### 🖼️ Real-Time Output Canvas Preview")
    thumbnail_img = generate_advanced_thumbnail(
        thumbnail_text,
        bg_color,
        text_color,
        shadow_color,
        banner_color,
        font_size,
        line_width,
        st.session_state.downloaded_web_bg,
        text_y_position,
        use_banner,
        font_choice
    )

    st.image(thumbnail_img, use_container_width=True)

    # Offer the rendered thumbnail as a downloadable PNG
    import io
    buf = io.BytesIO()
    thumbnail_img.save(buf, format="PNG")
    st.download_button(
        "⬇️ Download Thumbnail (PNG)",
        data=buf.getvalue(),
        file_name="thumbnail.png",
        mime="image/png"
    )

    render_nav_buttons()

# --- WORKSPACE 2: PRODUCTION SCHEDULER ---
elif st.session_state.current_page_idx == 1:
    st.title("🎥 Production Scheduler")
    st.caption("Plan upcoming content shoots and publish dates.")
    st.info("This workspace is a placeholder — wire up your scheduling logic here.")
    render_nav_buttons()

# --- WORKSPACE 3: ANALYTICS TRACKER ---
elif st.session_state.current_page_idx == 2:
    st.title("📊 Analytics Tracker")
    st.caption("Track view counts, retention, and click-through performance.")
    st.info("This workspace is a placeholder — connect your analytics data source here.")
    render_nav_buttons()

# --- WORKSPACE 4: VIRAL TREND FINDER ---
elif st.session_state.current_page_idx == 3:
    st.title("🔥 Viral Trend Finder")
    st.caption("Surface trending topics relevant to your niche.")
    st.info("This workspace is a placeholder — connect a trends API here.")
    render_nav_buttons()

# --- WORKSPACE 5: STUDIO SETTINGS ---
elif st.session_state.current_page_idx == 4:
    st.title("⚙️ Studio Settings")
    st.caption("Configure app-wide preferences.")
    st.write(f"Current theme: **{st.session_state.studio_theme}**")
    render_nav_buttons()
