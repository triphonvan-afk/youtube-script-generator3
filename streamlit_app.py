import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import urllib.request
import urllib.parse
import math
import io
import os
import datetime
import pandas as pd

# --- APP VIEWPORT SETUP ---
st.set_page_config(page_title="Ultimate Content Studio", layout="wide")

# --- INITIALIZE GLOBAL CACHE VARIABLES ---
if "current_page_idx" not in st.session_state:
    st.session_state.current_page_idx = 0
if "studio_theme" not in st.session_state:
    st.session_state.studio_theme = "Amethyst Dark"
if "downloaded_web_bg" not in st.session_state:
    st.session_state.downloaded_web_bg = None
if "sticker_list" not in st.session_state:
    st.session_state.sticker_list = []
if "schedule_list" not in st.session_state:
    st.session_state.schedule_list = []
if "analytics_list" not in st.session_state:
    st.session_state.analytics_list = []
if "default_export_res" not in st.session_state:
    st.session_state.default_export_res = "1280x720 (YouTube Thumbnail)"
if "default_motion_style" not in st.session_state:
    st.session_state.default_motion_style = "Straight"

# --- SIDEBAR: INTERFACE SYSTEM THEME SWITCHER ---
st.sidebar.header("⚙️ Studio Core Config")
selected_ui_theme = st.sidebar.selectbox(
    "Application Accent Theme",
    ["Amethyst Dark", "Sapphire Neon"],
    index=0 if st.session_state.studio_theme == "Amethyst Dark" else 1
)
st.session_state.studio_theme = selected_ui_theme

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
st.session_state.current_page_idx = page_names.index(chosen_sidebar_page)


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
FONT_URLS = {
    "Ultra-Heavy Block (Anton)": "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf",
    "Sleek Cyberpunk": "https://github.com/google/fonts/raw/main/ofl/shareTechMono/ShareTechMono-Regular.ttf",
    "Classic Geometric Bold": "https://github.com/google/fonts/raw/main/ofl/kanit/Kanit-Black.ttf",
    "Retro Serif Bold": "https://github.com/google/fonts/raw/main/ofl/cinzel/Cinzel%5Bwght%5D.ttf",
    "Elegant Script Modern": "https://github.com/google/fonts/raw/main/ofl/satisfy/Satisfy-Regular.ttf",
    "Futuristic Tech Accent": "https://github.com/google/fonts/raw/main/ofl/orbitron/Orbitron%5Bwght%5D.ttf",
    "Bold Poster (Bebas Neue)": "https://github.com/google/fonts/raw/main/ofl/bebasneue/BebasNeue-Regular.ttf",
    "Playful Rounded (Baloo 2)": "https://github.com/google/fonts/raw/main/ofl/baloo2/Baloo2%5Bwght%5D.ttf",
    "Handwritten Casual (Caveat)": "https://github.com/google/fonts/raw/main/ofl/caveat/Caveat%5Bwght%5D.ttf",
    "Horror Grunge (Nosifer)": "https://github.com/google/fonts/raw/main/ofl/nosifer/Nosifer-Regular.ttf",
    "Neon Sign (Monoton)": "https://github.com/google/fonts/raw/main/ofl/monoton/Monoton-Regular.ttf",
    "Minimal Sans (Poppins Black)": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Black.ttf",
}

FONT_FILENAMES = {
    "Ultra-Heavy Block (Anton)": "Anton-Regular.ttf",
    "Sleek Cyberpunk": "ShareTechMono-Regular.ttf",
    "Classic Geometric Bold": "Kanit-Black.ttf",
    "Retro Serif Bold": "Cinzel-Black.ttf",
    "Elegant Script Modern": "Satisfy.ttf",
    "Futuristic Tech Accent": "Orbitron.ttf",
    "Bold Poster (Bebas Neue)": "BebasNeue-Regular.ttf",
    "Playful Rounded (Baloo 2)": "Baloo2.ttf",
    "Handwritten Casual (Caveat)": "Caveat.ttf",
    "Horror Grunge (Nosifer)": "Nosifer-Regular.ttf",
    "Neon Sign (Monoton)": "Monoton-Regular.ttf",
    "Minimal Sans (Poppins Black)": "Poppins-Black.ttf",
}

MOTION_STYLES = ["Straight", "Arc Up", "Arc Down", "Wave", "Skew Right", "Skew Left"]

STICKER_TYPES = ["Star", "Heart", "Arrow", "Burst Badge", "Fire", "Speech Bubble", "Crown", "Checkmark"]

EXPORT_RESOLUTIONS = {
    "1280x720 (YouTube Thumbnail)": (1280, 720),
    "1920x1080 (Full HD Landscape)": (1920, 1080),
    "1080x1080 (Square Post)": (1080, 1080),
    "1080x1920 (Reels / TikTok / Shorts)": (1080, 1920),
}

PLATFORM_LIST = ["YouTube", "TikTok", "Instagram Reels", "Instagram Post", "Twitter / X", "Facebook", "LinkedIn"]
SCHEDULE_STATUSES = ["Idea", "Scripting", "Filming", "Editing", "Ready to Post", "Published"]

# Curated, fully offline starter dataset for the Trend Finder page.
TREND_LIBRARY = {
    "Gaming": ["#GamingClips", "#SpeedrunSunday", "#RetroGaming", "#IndieGameDev", "#ControllerCam", "#BossFight", "#GameplayHighlights"],
    "Beauty & Fashion": ["#GRWM", "#OOTD", "#SkincareRoutine", "#MakeupTransformation", "#ThriftFlip", "#StyleHaul", "#SelfCareSunday"],
    "Food & Cooking": ["#WhatIEatInADay", "#RecipeOfTheDay", "#QuickMeals", "#FoodHack", "#MukbangTime", "#BudgetMeals", "#KitchenTips"],
    "Fitness & Health": ["#WorkoutMotivation", "#30DayChallenge", "#HomeGym", "#MorningRoutine", "#ProgressNotPerfection", "#FormCheck"],
    "Tech & Productivity": ["#TechReview", "#ProductivityHacks", "#AppOfTheDay", "#DeskSetup", "#CodingLife", "#AIExplained"],
    "Comedy & Skits": ["#RelatableContent", "#PlotTwist", "#DailySkit", "#POV", "#UnexpectedEnding", "#CaughtOnCamera"],
    "Travel & Lifestyle": ["#HiddenGem", "#PackingTips", "#SoloTravel", "#DayInMyLife", "#BudgetTravel", "#VanLife"],
    "Business & Finance": ["#SideHustle", "#MoneyTips", "#SmallBusinessOwner", "#PassiveIncome", "#InvestingBasics", "#EntrepreneurLife"],
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
    return ImageFont.load_default()


def is_fallback_font(font_obj):
    return not hasattr(font_obj, "path")


# --- TEXT MOTION / STYLE RENDERING ---
def draw_line_straight(base_rgba, line, font, x_center, current_y, txt_hex, shd_hex, shadow_offset):
    draw = ImageDraw.Draw(base_rgba)
    left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
    text_width = right - left
    x_position = x_center - text_width // 2
    for sx in range(-shadow_offset, shadow_offset + 1):
        for sy in range(-shadow_offset, shadow_offset + 1):
            if abs(sx) > shadow_offset - 2 or abs(sy) > shadow_offset - 2:
                draw.text((x_position + sx, current_y + sy), line, fill=shd_hex, font=font)
    draw.text((x_position, current_y), line, fill=txt_hex, font=font)


def draw_line_arc_or_wave(base_rgba, line, font, x_center, current_y, txt_hex, shd_hex, shadow_offset, motion):
    draw = ImageDraw.Draw(base_rgba)
    chars = list(line)
    if not chars:
        return
    widths = []
    for ch in chars:
        l, t, r, b = draw.textbbox((0, 0), ch, font=font)
        widths.append(r - l)
    total_width = sum(widths)
    amplitude = max(10, int(font.size * 0.25)) if hasattr(font, "size") else 15
    start_x = x_center - total_width // 2
    n = len(chars)
    cursor_x = start_x
    for i, ch in enumerate(chars):
        t = i / max(1, n - 1)
        if motion == "Arc Up":
            y_off = -amplitude * math.sin(math.pi * t)
        elif motion == "Arc Down":
            y_off = amplitude * math.sin(math.pi * t)
        else:
            y_off = amplitude * math.sin(2 * math.pi * t * 1.5)
        y = current_y + y_off
        for sx in range(-shadow_offset, shadow_offset + 1):
            for sy in range(-shadow_offset, shadow_offset + 1):
                if abs(sx) > shadow_offset - 2 or abs(sy) > shadow_offset - 2:
                    draw.text((cursor_x + sx, y + sy), ch, fill=shd_hex, font=font)
        draw.text((cursor_x, y), ch, fill=txt_hex, font=font)
        cursor_x += widths[i]


def draw_line_skew(base_rgba, line, font, x_center, current_y, txt_hex, shd_hex, shadow_offset, direction):
    tmp_draw = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    left, top, right, bottom = tmp_draw.textbbox((0, 0), line, font=font)
    pad = shadow_offset + 10
    layer_w = (right - left) + pad * 2
    layer_h = (bottom - top) + pad * 2
    layer = Image.new("RGBA", (layer_w, layer_h), (0, 0, 0, 0))
    layer_draw = ImageDraw.Draw(layer)
    for sx in range(-shadow_offset, shadow_offset + 1):
        for sy in range(-shadow_offset, shadow_offset + 1):
            if abs(sx) > shadow_offset - 2 or abs(sy) > shadow_offset - 2:
                layer_draw.text((pad - left + sx, pad - top + sy), line, fill=shd_hex, font=font)
    layer_draw.text((pad - left, pad - top), line, fill=txt_hex, font=font)

    shear_factor = 0.3 if direction == "Skew Right" else -0.3
    new_w = layer_w + int(abs(shear_factor) * layer_h)
    sheared = layer.transform(
        (new_w, layer_h),
        Image.AFFINE,
        (1, shear_factor, -shear_factor * layer_h if shear_factor > 0 else 0, 0, 1, 0),
        resample=Image.BICUBIC
    )
    paste_x = x_center - new_w // 2
    paste_y = current_y - pad
    base_rgba.alpha_composite(sheared, (paste_x, paste_y))


def draw_styled_text(base_rgba, wrapped_lines, font, x_center, start_y, line_height, txt_hex, shd_hex, shadow_offset, motion):
    current_y = start_y
    for line in wrapped_lines:
        if motion == "Straight":
            draw_line_straight(base_rgba, line, font, x_center, current_y, txt_hex, shd_hex, shadow_offset)
        elif motion in ("Arc Up", "Arc Down", "Wave"):
            draw_line_arc_or_wave(base_rgba, line, font, x_center, current_y, txt_hex, shd_hex, shadow_offset, motion)
        elif motion in ("Skew Right", "Skew Left"):
            draw_line_skew(base_rgba, line, font, x_center, current_y, txt_hex, shd_hex, shadow_offset, motion)
        current_y += line_height


# --- STICKER (VECTOR ICON) LIBRARY ---
def _hex_to_rgba(hex_color, alpha=255):
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return (r, g, b, alpha)


def make_sticker_star(size, color):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size / 2, size / 2
    outer_r, inner_r = size * 0.48, size * 0.19
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        r = outer_r if i % 2 == 0 else inner_r
        points.append((cx + r * math.cos(angle), cy - r * math.sin(angle)))
    draw.polygon(points, fill=_hex_to_rgba(color))
    return img


def make_sticker_heart(size, color):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fill = _hex_to_rgba(color)
    r = size * 0.28
    draw.ellipse([size * 0.06, size * 0.10, size * 0.06 + 2 * r, size * 0.10 + 2 * r], fill=fill)
    draw.ellipse([size * 0.94 - 2 * r, size * 0.10, size * 0.94, size * 0.10 + 2 * r], fill=fill)
    draw.polygon([(size * 0.06, size * 0.42), (size * 0.94, size * 0.42), (size * 0.50, size * 0.95)], fill=fill)
    return img


def make_sticker_arrow(size, color):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fill = _hex_to_rgba(color)
    draw.polygon([
        (size * 0.05, size * 0.38), (size * 0.55, size * 0.38), (size * 0.55, size * 0.15),
        (size * 0.95, size * 0.50), (size * 0.55, size * 0.85), (size * 0.55, size * 0.62),
        (size * 0.05, size * 0.62)
    ], fill=fill)
    return img


def make_sticker_burst_badge(size, color):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fill = _hex_to_rgba(color)
    cx, cy = size / 2, size / 2
    outer_r, inner_r = size * 0.50, size * 0.36
    points = []
    for i in range(16):
        angle = i * math.pi / 8
        r = outer_r if i % 2 == 0 else inner_r
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill)
    return img


def make_sticker_fire(size, color):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fill = _hex_to_rgba(color)
    points = [
        (size * 0.50, size * 0.02), (size * 0.68, size * 0.30), (size * 0.80, size * 0.20),
        (size * 0.85, size * 0.55), (size * 0.65, size * 0.98), (size * 0.35, size * 0.98),
        (size * 0.15, size * 0.55), (size * 0.25, size * 0.42), (size * 0.35, size * 0.55),
        (size * 0.40, size * 0.30)
    ]
    draw.polygon(points, fill=fill)
    return img


def make_sticker_speech_bubble(size, color):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fill = _hex_to_rgba(color)
    draw.rounded_rectangle([size * 0.04, size * 0.08, size * 0.96, size * 0.72], radius=size * 0.12, fill=fill)
    draw.polygon([(size * 0.20, size * 0.68), (size * 0.38, size * 0.68), (size * 0.16, size * 0.96)], fill=fill)
    return img


def make_sticker_crown(size, color):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fill = _hex_to_rgba(color)
    points = [
        (size * 0.05, size * 0.85), (size * 0.05, size * 0.40), (size * 0.25, size * 0.55),
        (size * 0.50, size * 0.15), (size * 0.75, size * 0.55), (size * 0.95, size * 0.40),
        (size * 0.95, size * 0.85)
    ]
    draw.polygon(points, fill=fill)
    return img


def make_sticker_checkmark(size, color):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fill = _hex_to_rgba(color)
    draw.ellipse([size * 0.04, size * 0.04, size * 0.96, size * 0.96], outline=fill, width=max(2, int(size * 0.06)))
    draw.line([(size * 0.25, size * 0.52), (size * 0.44, size * 0.72), (size * 0.78, size * 0.28)],
              fill=fill, width=max(2, int(size * 0.08)), joint="curve")
    return img


STICKER_BUILDERS = {
    "Star": make_sticker_star,
    "Heart": make_sticker_heart,
    "Arrow": make_sticker_arrow,
    "Burst Badge": make_sticker_burst_badge,
    "Fire": make_sticker_fire,
    "Speech Bubble": make_sticker_speech_bubble,
    "Crown": make_sticker_crown,
    "Checkmark": make_sticker_checkmark,
}


def render_sticker(sticker_type, px_size, color, rotation):
    builder = STICKER_BUILDERS.get(sticker_type, make_sticker_star)
    icon = builder(px_size, color)
    if rotation:
        icon = icon.rotate(rotation, expand=True, resample=Image.BICUBIC)
    return icon


# --- PREMIUM THUMBNAIL RENDER ENGINE ---
def generate_advanced_thumbnail(title_text, bg_hex, txt_hex, shd_hex, bnr_hex,
                                 selected_size, selected_wrap, web_bg_file,
                                 y_pos, bnr_active, chosen_font_style, motion_style,
                                 sticker_list, canvas_size=(1280, 720)):
    canvas_w, canvas_h = canvas_size
    if web_bg_file and os.path.exists(web_bg_file):
        try:
            img = Image.open(web_bg_file).convert("RGB")
            img = img.resize((canvas_w, canvas_h), Image.Resampling.LANCZOS)
        except Exception:
            img = Image.new("RGB", (canvas_w, canvas_h), color=bg_hex)
    else:
        img = Image.new("RGB", (canvas_w, canvas_h), color=bg_hex)

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    for y in range(canvas_h):
        fade_factor = int((y / canvas_h) * 130)
        overlay_draw.line([(0, y), (canvas_w, y)], fill=(0, 0, 0, fade_factor))
    img_rgba = Image.alpha_composite(img.convert("RGBA"), overlay)

    font = get_selected_font_object(chosen_font_style, selected_size)
    wrapped_lines = textwrap.wrap(title_text.upper(), width=selected_wrap) or [""]
    line_height = selected_size + 15
    total_text_height = len(wrapped_lines) * line_height
    start_y = y_pos - (total_text_height // 2)

    if is_fallback_font(font):
        draw = ImageDraw.Draw(img_rgba)
        fallback_y = start_y
        for line in wrapped_lines:
            draw.text((100, fallback_y), line, fill=txt_hex)
            fallback_y += 30
        draw.rectangle([(0, canvas_h - 15), (canvas_w, canvas_h)], fill="#FF0000")
        return img_rgba.convert("RGB")

    draw = ImageDraw.Draw(img_rgba)
    if bnr_active:
        banner_padding_v = 30
        draw.rectangle(
            [(0, max(0, start_y - banner_padding_v)),
             (canvas_w, min(canvas_h, start_y + total_text_height + banner_padding_v - 10))],
            fill=bnr_hex
        )

    shadow_offset = max(3, int(selected_size * 0.08))
    draw_styled_text(img_rgba, wrapped_lines, font, canvas_w // 2, start_y, line_height,
                      txt_hex, shd_hex, shadow_offset, motion_style)

    for sticker in sticker_list:
        icon = render_sticker(sticker["type"], sticker["size"], sticker["color"], sticker["rotation"])
        px = int(sticker["x"] - icon.width / 2)
        py = int(sticker["y"] - icon.height / 2)
        img_rgba.alpha_composite(icon, (px, py))

    draw = ImageDraw.Draw(img_rgba)
    draw.rectangle([(0, canvas_h - 15), (canvas_w, canvas_h)], fill="#FF0000")
    return img_rgba.convert("RGB")


# =====================================================================
# --- RENDER LOGIC WORKSPACE SWITCH DEPOT ---
# =====================================================================

# --- PAGE 1: MAIN STUDIO CANVAS ---
if st.session_state.current_page_idx == 0:
    st.title("🎨 Pro Short-Form Thumbnail Studio")
    st.caption("Design advanced high-contrast image layouts locally with real-time vector adjustments.")

    st.sidebar.subheader("🎨 Canvas Controls")
    bg_color = st.sidebar.color_picker("Fallback Canvas Color", "#1E1E2E")
    text_color = st.sidebar.color_picker("Headline Text Color", "#FFCC00")
    shadow_color = st.sidebar.color_picker("3D Outline Drop-Shadow Color", "#000000")

    st.sidebar.subheader("📐 Custom Formatting Adjustments")
    font_choice = st.sidebar.selectbox("Headline Font Style Asset", list(FONT_URLS.keys()))
    default_motion_idx = MOTION_STYLES.index(st.session_state.default_motion_style) if st.session_state.default_motion_style in MOTION_STYLES else 0
    motion_choice = st.sidebar.selectbox("Text Movement / Motion Style", MOTION_STYLES, index=default_motion_idx)
    font_size = st.sidebar.slider("Font Vector Size Scale", min_value=40, max_value=300, value=150, step=5)
    line_width = st.sidebar.slider("Characters Per Line (Wrap)", min_value=5, max_value=25, value=11, step=1)
    text_y_position = st.sidebar.slider("Vertical Alignment Offset", min_value=50, max_value=650, value=360, step=10)

    st.sidebar.subheader("🏷️ Banner Layer Accents")
    use_banner = st.sidebar.checkbox("Enable Solid Text Backdrop Accent Banner", value=False)
    banner_color = st.sidebar.color_picker("Backdrop Banner Color", "#000000")

    canvas_w, canvas_h = EXPORT_RESOLUTIONS[st.session_state.default_export_res]
    st.sidebar.caption(f"Export size set in Studio Settings: **{canvas_w}×{canvas_h}**")

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
                    formatted_query = urllib.parse.quote(search_query.strip().replace(" ", ","))
                    source_url = f"https://loremflickr.com/{canvas_w}/{canvas_h}/{formatted_query}"
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

    st.subheader("🎉 Stickers")
    st_col1, st_col2, st_col3, st_col4 = st.columns(4)
    with st_col1:
        new_sticker_type = st.selectbox("Sticker Icon", STICKER_TYPES, key="new_sticker_type")
        new_sticker_color = st.color_picker("Sticker Color", "#FF2D55", key="new_sticker_color")
    with st_col2:
        new_sticker_x = st.slider("Position X", 0, canvas_w, min(canvas_w - 100, int(canvas_w * 0.85)), key="new_sticker_x")
        new_sticker_y = st.slider("Position Y", 0, canvas_h, int(canvas_h * 0.15), key="new_sticker_y")
    with st_col3:
        new_sticker_size = st.slider("Sticker Size", 30, 400, 140, key="new_sticker_size")
        new_sticker_rotation = st.slider("Rotation °", -180, 180, 0, key="new_sticker_rotation")
    with st_col4:
        st.write("")
        st.write("")
        if st.button("➕ Add Sticker"):
            st.session_state.sticker_list.append({
                "type": new_sticker_type,
                "color": new_sticker_color,
                "x": new_sticker_x,
                "y": new_sticker_y,
                "size": new_sticker_size,
                "rotation": new_sticker_rotation,
            })
            st.rerun()
        if st.button("🗑️ Clear All Stickers"):
            st.session_state.sticker_list = []
            st.rerun()

    if st.session_state.sticker_list:
        st.write("**Placed stickers:**")
        for idx, sticker in enumerate(st.session_state.sticker_list):
            s_col1, s_col2 = st.columns([6, 1])
            with s_col1:
                st.write(f"{idx + 1}. {sticker['type']} — pos ({sticker['x']}, {sticker['y']}), size {sticker['size']}, rot {sticker['rotation']}°")
            with s_col2:
                if st.button("Remove", key=f"remove_sticker_{idx}"):
                    st.session_state.sticker_list.pop(idx)
                    st.rerun()

    st.write("### 🖼️ Real-Time Output Canvas Preview")
    thumbnail_img = generate_advanced_thumbnail(
        thumbnail_text, bg_color, text_color, shadow_color, banner_color,
        font_size, line_width, st.session_state.downloaded_web_bg,
        text_y_position, use_banner, font_choice, motion_choice,
        st.session_state.sticker_list, canvas_size=(canvas_w, canvas_h)
    )

    st.image(thumbnail_img, use_container_width=True)

    buf = io.BytesIO()
    thumbnail_img.save(buf, format="PNG")
    st.download_button("⬇️ Download Thumbnail (PNG)", data=buf.getvalue(), file_name="thumbnail.png", mime="image/png")

    render_nav_buttons()

# --- PAGE 2: PRODUCTION SCHEDULER ---
elif st.session_state.current_page_idx == 1:
    st.title("🎥 Production Scheduler")
    st.caption("Plan, track, and organize every video from idea to publish.")

    with st.form("add_schedule_item_form", clear_on_submit=True):
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            sched_title = st.text_input("Video / Post Title")
            sched_platform = st.selectbox("Platform", PLATFORM_LIST)
        with f_col2:
            sched_date = st.date_input("Scheduled Date", value=datetime.date.today())
            sched_time = st.time_input("Scheduled Time", value=datetime.time(12, 0))
        with f_col3:
            sched_status = st.selectbox("Status", SCHEDULE_STATUSES)
            sched_notes = st.text_input("Notes (optional)")
        submitted = st.form_submit_button("➕ Add To Schedule")
        if submitted:
            if sched_title.strip():
                st.session_state.schedule_list.append({
                    "Title": sched_title,
                    "Platform": sched_platform,
                    "Date": sched_date,
                    "Time": sched_time.strftime("%H:%M"),
                    "Status": sched_status,
                    "Notes": sched_notes,
                })
                st.success(f"Added '{sched_title}' to the schedule.")
            else:
                st.warning("Give the video a title before adding it.")

    if st.session_state.schedule_list:
        df = pd.DataFrame(st.session_state.schedule_list).sort_values("Date")

        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Total Planned", len(df))
        m_col2.metric("Ready To Post", int((df["Status"] == "Ready to Post").sum()))
        m_col3.metric("Published", int((df["Status"] == "Published").sum()))

        filt_col1, filt_col2 = st.columns(2)
        with filt_col1:
            status_filter = st.multiselect("Filter by status", SCHEDULE_STATUSES, default=SCHEDULE_STATUSES)
        with filt_col2:
            platform_filter = st.multiselect("Filter by platform", PLATFORM_LIST, default=PLATFORM_LIST)

        filtered_df = df[df["Status"].isin(status_filter) & df["Platform"].isin(platform_filter)]
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

        st.write("**Remove an entry:**")
        for idx, row in df.iterrows():
            r_col1, r_col2 = st.columns([6, 1])
            with r_col1:
                st.write(f"{row['Date']} · {row['Time']} — **{row['Title']}** ({row['Platform']}, {row['Status']})")
            with r_col2:
                if st.button("Remove", key=f"remove_sched_{idx}"):
                    st.session_state.schedule_list.pop(idx)
                    st.rerun()
    else:
        st.info("Nothing scheduled yet — add your first video above.")

    render_nav_buttons()

# --- PAGE 3: ANALYTICS TRACKER ---
elif st.session_state.current_page_idx == 2:
    st.title("📊 Analytics Tracker")
    st.caption("Log performance numbers manually and track engagement over time.")

    with st.form("add_analytics_form", clear_on_submit=True):
        a_col1, a_col2, a_col3 = st.columns(3)
        with a_col1:
            an_title = st.text_input("Video / Post Title")
            an_platform = st.selectbox("Platform", PLATFORM_LIST, key="an_platform")
        with a_col2:
            an_date = st.date_input("Published Date", value=datetime.date.today(), key="an_date")
            an_views = st.number_input("Views", min_value=0, value=0, step=100)
        with a_col3:
            an_likes = st.number_input("Likes", min_value=0, value=0, step=10)
            an_comments = st.number_input("Comments", min_value=0, value=0, step=5)
        an_shares = st.number_input("Shares", min_value=0, value=0, step=5)
        submitted_analytics = st.form_submit_button("➕ Log Performance")
        if submitted_analytics:
            if an_title.strip():
                engagement = an_likes + an_comments + an_shares
                engagement_rate = round((engagement / an_views) * 100, 2) if an_views > 0 else 0.0
                st.session_state.analytics_list.append({
                    "Title": an_title,
                    "Platform": an_platform,
                    "Date": an_date,
                    "Views": an_views,
                    "Likes": an_likes,
                    "Comments": an_comments,
                    "Shares": an_shares,
                    "Engagement Rate %": engagement_rate,
                })
                st.success(f"Logged performance for '{an_title}'.")
            else:
                st.warning("Give the video a title before logging performance.")

    if st.session_state.analytics_list:
        df = pd.DataFrame(st.session_state.analytics_list).sort_values("Date")

        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("Total Views", int(df["Views"].sum()))
        m_col2.metric("Total Likes", int(df["Likes"].sum()))
        m_col3.metric("Avg. Engagement Rate", f"{df['Engagement Rate %'].mean():.2f}%")
        m_col4.metric("Videos Tracked", len(df))

        st.dataframe(df, use_container_width=True, hide_index=True)

        st.write("#### Views by Video")
        chart_df = df.set_index("Title")[["Views"]]
        st.bar_chart(chart_df)

        st.write("#### Views Over Time")
        time_df = df.groupby("Date")["Views"].sum()
        st.line_chart(time_df)

        st.write("**Remove an entry:**")
        for idx, row in df.iterrows():
            r_col1, r_col2 = st.columns([6, 1])
            with r_col1:
                st.write(f"{row['Date']} — **{row['Title']}** ({row['Platform']}): {row['Views']} views, {row['Engagement Rate %']}% engagement")
            with r_col2:
                if st.button("Remove", key=f"remove_analytics_{idx}"):
                    st.session_state.analytics_list.pop(idx)
                    st.rerun()
    else:
        st.info("No performance data logged yet — add your first entry above.")

    render_nav_buttons()

# --- PAGE 4: VIRAL TREND FINDER ---
elif st.session_state.current_page_idx == 3:
    st.title("🔥 Viral Trend Finder")
    st.caption("Browse a curated, offline hashtag and content-idea starter library by niche.")

    trend_category = st.selectbox("Choose your content niche", list(TREND_LIBRARY.keys()))
    keyword_filter = st.text_input("Optional: narrow down by keyword", value="")

    tags = TREND_LIBRARY[trend_category]
    if keyword_filter.strip():
        tags = [t for t in tags if keyword_filter.lower() in t.lower()]

    st.write(f"### Trending Tag Ideas — {trend_category}")
    if tags:
        tag_cols = st.columns(3)
        for i, tag in enumerate(tags):
            with tag_cols[i % 3]:
                st.markdown(f"**{tag}**")
        combo = " ".join(tags)
        st.text_area("Copy-ready hashtag block", value=combo, height=100)
    else:
        st.info("No tags match that keyword filter — try clearing it.")

    st.write("### Content Idea Prompts")
    idea_prompts = [
        f"Do a 'day in the life' angle built around {trend_category.lower()}.",
        f"React to a common myth or mistake people make in {trend_category.lower()}.",
        f"Turn your top comment into a full follow-up video.",
        f"Show a before/after or transformation tied to {trend_category.lower()}.",
        f"Break down a trending topic in {trend_category.lower()} in under 60 seconds.",
    ]
    for prompt in idea_prompts:
        st.markdown(f"- {prompt}")

    st.caption("This is a static, fully offline idea library rather than a live trends feed — a good starting point when you're short on ideas.")

    render_nav_buttons()

# --- PAGE 5: STUDIO SETTINGS ---
elif st.session_state.current_page_idx == 4:
    st.title("⚙️ Studio Settings")
    st.caption("Configure app-wide defaults and manage your saved studio data.")

    st.subheader("🖼️ Export Defaults")
    res_choice = st.selectbox(
        "Default canvas / export resolution",
        list(EXPORT_RESOLUTIONS.keys()),
        index=list(EXPORT_RESOLUTIONS.keys()).index(st.session_state.default_export_res)
    )
    st.session_state.default_export_res = res_choice

    motion_default_choice = st.selectbox(
        "Default text movement style",
        MOTION_STYLES,
        index=MOTION_STYLES.index(st.session_state.default_motion_style)
    )
    st.session_state.default_motion_style = motion_default_choice

    st.subheader("🎨 Interface")
    st.write(f"Current accent theme: **{st.session_state.studio_theme}** (change it from the sidebar)")

    st.subheader("📦 Data Overview")
    d_col1, d_col2, d_col3 = st.columns(3)
    d_col1.metric("Stickers Saved", len(st.session_state.sticker_list))
    d_col2.metric("Scheduled Items", len(st.session_state.schedule_list))
    d_col3.metric("Analytics Entries", len(st.session_state.analytics_list))

    st.subheader("🧹 Reset Studio Data")
    st.caption("These actions clear data for this session only.")
    rc1, rc2, rc3, rc4 = st.columns(4)
    with rc1:
        if st.button("Clear Stickers"):
            st.session_state.sticker_list = []
            st.rerun()
    with rc2:
        if st.button("Clear Schedule"):
            st.session_state.schedule_list = []
            st.rerun()
    with rc3:
        if st.button("Clear Analytics"):
            st.session_state.analytics_list = []
            st.rerun()
    with rc4:
        if st.button("Clear Background Image"):
            st.session_state.downloaded_web_bg = None
            st.rerun()

    render_nav_buttons()
