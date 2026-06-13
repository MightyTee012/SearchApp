import streamlit as st
import base64
import os

# --- DESIGN ICON REGISTRY ---
ICONS = {
    "database": "🫥",
    "search": "😍",
    "filter": "😜",
    "visible": "😒",
    "download": "🤑",
    "file": "😎"
}

@st.cache_data(show_spinner=False)
def get_cached_base64(file_name):
    """Safely locates and reads local assets from your app directory."""
    if not file_name:
        return ""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_dir, file_name)
    
    if os.path.exists(full_path):
        try:
            with open(full_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except Exception:
            return ""
    return ""

def get_icon_html(icon_name, size=32):
    """Displays animated GIF files directly inline with headers with a custom tracking class."""
    file_map = {
        "database": "database.gif",
        "search": "search.gif",
        "filter": "filter.gif",
        "visible": "visible.gif",
        "download": "download.gif",
        "file": "file.gif"
    }
    
    target_file = file_map.get(icon_name, "")
    b64_str = get_cached_base64(target_file)
    
    if b64_str:
        return f'<img class="custom-gif-icon" src="data:image/gif;base64,{b64_str}" width="{size}" style="vertical-align: middle; margin-right: 10px; margin-bottom: 4px;">'
    
    return f"<span style='font-size: {size}px; margin-right: 10px;'>{ICONS.get(icon_name, '')}</span>"

def inject_modern_css():
    """Injects high-contrast overrides to optimize text visibility and border definition."""
    
    is_dark = st.session_state.get("dark_mode", False)
    
    bg_local = get_cached_base64("background.jpg") or get_cached_base64("background.gif")
    if bg_local:
        bg_url = f"data:image/jpeg;base64,{bg_local}"
        bg_url_1 = f"data:image/gif;base64,{bg_local}"
    else:
        bg_url = "https://plus.unsplash.com/premium_vector-1719816838907-8b4304af21e6?q=80&w=1316&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        bg_url_1 = "https://media.istockphoto.com/id/1147249349/vector/beagle-in-action-seamless-pattern.jpg?s=612x612&w=0&k=20&c=vyFNQzFKxojRckU584PDEXLZIVNbDbQa0cUQRwXiaJA="

    if is_dark:
        # 🌙 MIDNIGHT STATES (HIGH CONTRAST BORDERS)
        main_overlay = "linear-gradient(rgba(15, 23, 42, 0.78), rgba(15, 23, 42, 0.78))"
        side_overlay = "linear-gradient(rgba(30, 41, 59, 0.82), rgba(30, 41, 59, 0.82))"
        text_color = "#FFFFFF"         
        input_bg = "rgba(15, 23, 42, 0.85)"
        input_text = "#38BDF8"
        border_color = "#38BDF8"       
        border_thickness = "2.5px"     
        card_bg = "#1E293B"
        track_color = "#0F172A"
        thumb_color = "#334155"
        thumb_hover = "#38BDF8"
        
        btn_bg = "transparent"
        btn_text = "#38BDF8"
        btn_hover_bg = "rgba(56, 189, 248, 0.15)"
        gif_filter = "brightness(1.3) contrast(1.15)"
    else:
        # ☀️ EXECUTIVE LIGHT STATES
        main_overlay = "linear-gradient(rgba(230, 240, 250, 0.85), rgba(230, 240, 250, 0.85))"
        side_overlay = "linear-gradient(rgba(203, 220, 235, 0.88), rgba(203, 220, 235, 0.88))"
        text_color = "#0A1931"
        input_bg = "rgba(206, 235, 224, 0.6)"
        input_text = "#021eba"
        border_color = "#0A1931"      
        border_thickness = "2px"
        card_bg = "#ceebe0"
        track_color = "#CBDCEB"
        thumb_color = "#0A1931"
        thumb_hover = "#7cb7f7"
        
        btn_bg = "transparent"
        btn_text = "#0A1931"
        btn_hover_bg = "rgba(10, 25, 49, 0.08)"
        gif_filter = "none"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght=400;500;600;700;800&display=swap');

        /* FORCE CRASH CONFIG.TOML ARTIFACTS */
        :root, [data-theme="light"], [data-theme="dark"], html, body {{
            --primary-color: {border_color} !important;
            --background-color: {card_bg} !important;
            --secondary-background-color: {input_bg} !important;
            --text-color: {text_color} !important;
            --st-color-background: {card_bg} !important;
            --st-color-secondary-background: {input_bg} !important;
            --st-color-text: {text_color} !important;
            --st-color-primary: {border_color} !important;
        }}

        /* APP VIEWPORT COMPONENT RESETS */
        header[data-testid="stHeader"], footer {{
            visibility: hidden !important;
            display: none !important;
            height: 0px !important;
        }}
        [data-testid="stAppViewContainer"] {{
            padding-top: 0px !important;
        }}

        /* APP GLOBAL TYPOGRAPHY RESOLUTIONS */
        html, body, .stApp, input, button, select, textarea, .stTabs {{
            font-size: 18px !important;
            font-family: 'Poppins', sans-serif !important;
            color: {text_color} !important;
        }}
        h1, h2, h3, span, p, label, .stMarkdown, div[data-testid="stWidgetLabel"] p {{
            color: {text_color} !important;
        }}

        /* HIGH-DEFINITION NAVIGATION SCROLLBAR CONTEXTS */
        ::-webkit-scrollbar {{
            width: 14px !important;      
            height: 14px !important;      
            display: block !important;
        }}
        ::-webkit-scrollbar-track {{
            background: {track_color} !important;       
            border: {border_thickness} solid {border_color} !important;
            border-radius: 6px !important;
        }}
        ::-webkit-scrollbar-thumb {{
            background-color: {thumb_color} !important;
            border-radius: 6px !important;
            border: 2px solid {track_color} !important; 
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background-color: {thumb_hover} !important;
        }}

        /* STRUCTURAL CONTENT BACKDROPS */
        html, body, .stApp {{
            background-image: {main_overlay}, url('{bg_url}') !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            overflow-x: hidden !important;
        }}
        
        .main .block-container {{
            max-width: 100% !important;      
            width: 100% !important;      
            margin: 0 !important;
            padding: 15px 20px 0px 20px !important;
            height: calc(100vh - 20px) !important;
            overflow: hidden !important;
            display: flex;
            flex-direction: column;
        }}

        [data-testid="stVerticalBlock"] {{
            width: 100% !important;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            gap: 0.35rem !important;
            row-gap: 0.35rem !important;
        }}

        /* CONTROL RACK SIDEBAR MATRIX */
        [data-testid="stSidebar"] {{
            background-image: {side_overlay}, url('{bg_url_1}') !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            border-right: {border_thickness} solid {border_color} !important;
        }}
        [data-testid="stSidebarUserContent"] {{
            background-color: transparent !important; 
            padding-top: 0.25rem !important;  
        }}
        [data-testid="stSidebarHeader"] {{
            background-color: transparent !important;
            padding: 0px !important;
            min-height: unset !important;
        }}
        
        hr {{ margin: 0.4rem 0 !important; border-color: {border_color} !important; }}

        /* DATA FORM HOUSINGS */
        div[data-testid="stForm"] {{
            background-color: transparent !important;
            border: {border_thickness} solid {border_color} !important;
            border-radius: 12px !important;
            padding: 1rem !important;
        }}
        .stExpander {{
            background-color: {card_bg} !important;
            border: {border_thickness} solid {border_color} !important;
            border-radius: 0.5rem !important;
        }}

        /* 📁 FILE UPLOADER STYLE CRADLE */
        div[data-testid="stFileUploader"], 
        div[data-testid="stFileUploader"] *, 
        div[data-testid="stFileUploaderDropzone"],
        div[data-testid="stFileUploaderFilesContainer"],
        div[data-testid="stFileUploaderFilesContainer"] * {{
            background-color: transparent !important;
            background: transparent !important;
        }}
        
        div[data-testid="stFileUploaderDropzone"] {{
            background-color: {input_bg} !important;
            border: {border_thickness} dashed {border_color} !important;
            border-radius: 10px !important;
        }}

        /* 🎯 ULTRASHIELD FIX: FORCE VISIBILITY BEFORE AND AFTER FILE UPLOAD COMPLETION */
        div[data-testid="stFileUploader"] *,
        div[data-testid="stFileUploader"] div,
        div[data-testid="stFileUploader"] span,
        div[data-testid="stFileUploader"] small,
        div[data-testid="stFileUploader"] p,
        div[data-testid="stFileUploaderFilesContainer"] *,
        div[data-testid="stFileUploaderFilesContainer"] span,
        div[data-testid="stFileUploaderFilesContainer"] div {{
            color: {text_color} !important;
            -webkit-text-fill-color: {text_color} !important;
            font-weight: 600 !important;
        }}

        /* 👑 GIF VISIBILITY ENGINE */
        .custom-gif-icon {{
            filter: {gif_filter} !important;
            transition: filter 0.3s ease-in-out;
        }}

        /* TRANSPARENT DESIGN INTERACTIVE BUTTON DECK WITH RE-ENFORCED CONTRAST */
        .stButton>button, .stDownloadButton>button, div[data-testid="stFormSubmitButton"]>button, button[data-baseweb="button"] {{
            background-color: {btn_bg} !important;
            color: {btn_text} !important;
            font-weight: 700 !important;
            border: {border_thickness} solid {border_color} !important;
            border-radius: 0.4rem !important;
            width: 100% !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            transition: all 0.2s ease-in-out !important;
        }}
        .stButton>button:hover, .stDownloadButton>button:hover, div[data-testid="stFormSubmitButton"]>button:hover {{
            background-color: {btn_hover_bg} !important;
            color: {btn_text} !important;
            border-color: {border_color} !important;
            transform: translateY(-1px);
        }}

        /* COMPONENT MATRIX INPUT BOX ENTRIES */
        .stTextInput input {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            font-size: 1.15rem !important;
            font-weight: 600 !important;
            border: {border_thickness} solid {border_color} !important;
            border-radius: 0.4rem !important;
        }}
        
        /* 🔍 FIX: COLUMN PICKER / MULTISELECT INTERIOR TEXT visibility */
        div[data-baseweb="select"] {{
            background-color: {input_bg} !important;
            border: {border_thickness} solid {border_color} !important;
            border-radius: 0.4rem !important;
        }}
        div[data-baseweb="select"] *,
        div[data-baseweb="select"] div,
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] input,
        .stMultiSelect div[role="combobox"] *,
        .stMultiSelect div[role="combobox"] div {{
            color: {text_color} !important;
            -webkit-text-fill-color: {text_color} !important;
        }}
        
        /* Multiselect item tags */
        div[data-baseweb="tag"] {{
            background-color: {card_bg} !important;
            border: 1px solid {border_color} !important;
            border-radius: 4px !important;
        }}
        div[data-baseweb="tag"] * {{
            color: {text_color} !important;
            -webkit-text-fill-color: {text_color} !important;
        }}

        /* Float listbox popovers appended directly to document body context */
        div[data-baseweb="popover"], 
        div[data-baseweb="popover"] *, 
        div[data-baseweb="menu"], 
        div[data-baseweb="menu"] *, 
        div[role="listbox"], 
        div[role="listbox"] *, 
        ul[role="listbox"],
        ul[role="listbox"] *,
        li[role="option"] {{
            background-color: {card_bg} !important;
            background: {card_bg} !important;
            color: {text_color} !important;
        }}
        li[role="option"]:hover, li[role="option"]:hover * {{
            background-color: {btn_hover_bg} !important;
        }}

        /* RUNTIME ANALYTICS STATUS VALUE BAR */
        .status-bar {{
            background-color: {track_color} !important;
            padding: 0.6rem 1rem;
            border-radius: 0.4rem;
            font-family: monospace;
            font-size: 1rem !important;
            font-weight: 700 !important;
            border: {border_thickness} solid {border_color} !important;
        }}
        
        /* WORKSPACE ACTION VIEWPORT TABS */
        button[data-baseweb="tab"] {{ font-weight: 700 !important; }}
        button[data-baseweb="tab"][aria-selected="true"] p {{ color: {thumb_hover} !important; }}

        /* ULTRACLEAN TRANSPARENT DATAFRAME OVERRIDES WITH BORDER COATING */
        [data-testid="stDataFrame"], 
        [data-testid="stDataFrame"] *, 
        [data-testid="stDataFrame"]>div, 
        [data-testid="stDataFrame"] iframe,
        div[data-testid="stDataFrame"] [role="grid"],
        div[data-testid="stDataFrame"] [class*="canvas"],
        div[data-testid="stDataFrame"] [class*="StyledDataFrame"],
        .glideDataGridCanvas {{
            background-color: transparent !important;
            background: transparent !important;
        }}
        [data-testid="stDataFrame"] {{
            border: {border_thickness} solid {border_color} !important;
            border-radius: 10px !important;
        }}
        </style>
    """, unsafe_allow_html=True)