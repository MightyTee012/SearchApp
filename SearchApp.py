import os
import sys
import asyncio
import warnings
import re
from io import BytesIO
import pandas as pd
import streamlit as st

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

if sys.platform == 'win32':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Initialize structural memory states for themes and file streams
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "file_capsule" not in st.session_state:
    st.session_state.file_capsule = None
if "confirmed_cols" not in st.session_state:
    st.session_state.confirmed_cols = []

# Imported using the exact case matching your file name
import AppStyle as style

# --- INIT PAGE CONFIG ---
st.set_page_config(
    page_title="Team Permitting",
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# Apply dynamic active theme styling (Light vs Dark)
style.inject_modern_css()

# --- HIGH-DENSITY SCREEN OPTIMIZER ---
st.markdown("""
    <style>
        .block-container {
            max-width: 100% !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            padding-top: 1.5rem !important;
            padding-bottom: 1rem !important;
        }
        div[data-testid="stVerticalBlock"] {
            gap: 0.6rem !important;
        }
        body {
            overflow: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# --- HELPER UTILITIES ---
def clear_all_searches_and_filters():
    st.session_state.global_search_input = ""
    for key in list(st.session_state.keys()):
        if key.startswith("sidebar_filter_"):
            st.session_state[key] = ""

def normalize_text(text):
    if pd.isna(text):
        return ""
    return re.sub(r'[^a-zA-Z0-9]', '', str(text)).lower()

def fuzzy_contains(series, query):
    normalized_query = normalize_text(query)
    if not normalized_query:
        return pd.Series(True, index=series.index)
    normalized_series = series.astype(str).str.replace(r'[^a-zA-Z0-9]', '', regex=True).str.lower()
    return normalized_series.str.contains(normalized_query, regex=False)

# --- LIGHTWEIGHT HEADER SCANNER ---
@st.cache_data(ttl=60, show_spinner=False)
def scan_file_headers(file):
    try:
        file.seek(0)
        if file.name.endswith('.csv'):
            df_headers = pd.read_csv(file, nrows=0)
        else:
            df_headers = pd.read_excel(file, engine='openpyxl', nrows=0)
        return df_headers.columns.tolist()
    except Exception:
        return []

# --- OPTIMIZED BULLETPROOF DATA PROCESSING ENGINE ---
@st.cache_data(ttl=60, show_spinner=False)
def load_large_data(file, usecols=None):
    try:
        file.seek(0)
        if file.name.endswith('.csv'):
            df = pd.read_csv(file, dtype=str, usecols=usecols)
        else:
            df = pd.read_excel(file, engine='openpyxl', usecols=usecols, dtype=str)

        for col in df.columns:
            col_lower = col.lower()
            is_target_date_column = any(k in col_lower for k in ['date', 'time', 'prepared', 'validity', 'valid', 'timestamp'])

            if is_target_date_column:
                def safe_isolate_timestamp(val):
                    if pd.isna(val) or str(val).strip().lower() in ['nan', '', '<na>', 'none']:
                        return ""
                    val_str = str(val).strip()
                    
                    if val_str.replace('.', '', 1).isdigit():
                        try:
                            numeric_days = float(val_str)
                            if 1 <= numeric_days <= 100000:
                                dt = pd.to_datetime(numeric_days, unit='D', origin='1899-12-30', errors='coerce')
                                if pd.notna(dt) and 1678 <= dt.year <= 2261:
                                    return dt.strftime('%B %d, %Y')
                        except:
                            pass
                    try:
                        if any(bad in val_str for bad in ['0001', '1-01-01', '0000']):
                            return ""
                        dt = pd.to_datetime(val_str, errors='coerce')
                        if pd.notna(dt) and 1678 <= dt.year <= 2261:
                            return dt.strftime('%B %d, %Y')
                    except:
                        pass
                    return val_str

                df[col] = df[col].apply(safe_isolate_timestamp)
            else:
                df[col] = df[col].fillna('').astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
                df[col] = df[col].replace(['nan', '<NA>', 'None', 'NaN'], '')

        return df
    except Exception as e:
        st.error(f"🚨 **Upload Processing Failed!**")
        st.info(f"**Error Details:** {e}")
        return None

# --- MAIN BRANDING HEADER ---
st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 5px; height: 65px; margin-bottom: 5px; margin-top: -15px; background: transparent;">
        <img src="https://i.pinimg.com/originals/15/c1/44/15c144e8dc552a100b3292d268854499.gif" style="height: 60px; width: auto; image-rendering: pixelated; mix-blend-mode: multiply;">
        <span style="font-size: 24px; font-weight: 800; font-family: 'Source Sans Pro', sans-serif;">GAWA NI NONOY 👌</span>
    </div>
    """, 
    unsafe_allow_html=True
)

active_file = st.session_state.file_capsule
df = None
all_headers = []

# ==========================================
# 🎯 PHASE 1: INITIAL LIGHTWEIGHT LANDING VIEW (NO FILE YET)
# ==========================================
if active_file is None:
    st.markdown("### 📂 Setup Deck")
    raw_upload = st.file_uploader(
        "Drop workbook matrix:", 
        type=["csv", "xlsx"],
        key="file_uploader_widget"
    )
    if raw_upload is not None:
        st.session_state.file_capsule = raw_upload
        st.rerun()
        
    st.info("💡 **Workspace Idle.** Drop a source data file into the setup panel above to instantly configure features, dark mode controls, and display column layouts.")

# ==========================================
# 🎯 PHASE 2: DASHBOARD VIEW (ONCE FILE IS UPLOADED)
# ==========================================
else:
    # Outer Layout Setup for App Panel
    side_control_panel, main_data_window = st.columns([0.20, 0.80], gap="small")
    
    # Scan the layout headers first to know what columns exist
    all_headers = scan_file_headers(active_file)
    
    # 🔍 FIX: If it's a brand new file, automatically confirm ALL columns right away
    if "last_loaded_name" not in st.session_state or st.session_state.last_loaded_name != active_file.name:
        st.session_state.confirmed_cols = all_headers  # Default straight to all columns
        st.session_state.last_loaded_name = active_file.name

    with side_control_panel:
        tab_setup, tab_search, tab_download = st.tabs([
            "⚙️1.SETUP", 
            "🔍2.SEARCH", 
            "💾3.EXPORT"
        ])
        
        with tab_setup:
            st.markdown("---")
            theme_label = "☀️ Switch to Light Mode" if st.session_state.dark_mode else "🌙 Switch to Dark Mode"
            if st.button(theme_label, use_container_width=True):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()
                
            st.markdown("---")
            if st.button("🗑️ Unload Current File", use_container_width=True):
                st.session_state.file_capsule = None
                st.session_state.confirmed_cols = []
                if "last_loaded_name" in st.session_state:
                    del st.session_state["last_loaded_name"]
                st.cache_data.clear()
                st.toast("🗑️ File unloaded successfully.", icon="ℹ️")
                st.rerun()

            st.markdown("---")
            st.markdown("### 👁️ Display Columns")
            st.markdown("<small>Pick your target headers, then click the button below to load:</small>", unsafe_allow_html=True)
            
            with st.form(key="batch_column_form", border=False):
                picked_columns = st.multiselect(
                    "Select columns to stream:",
                    options=all_headers,
                    default=[c for c in st.session_state.confirmed_cols if c in all_headers],
                    placeholder="Choose columns..."
                )
                
                load_triggered = st.form_submit_button("⚡ APPLY & LOAD COLUMNS", use_container_width=True)
                
                if load_triggered:
                    st.session_state.confirmed_cols = picked_columns
                    st.rerun()

    # --- CONDITIONAL RUNTIME PROCESSING ---
    if st.session_state.confirmed_cols:
        visible_columns = st.session_state.confirmed_cols
        
        with st.spinner("⏳ Nonoy's engine is optimizing your dataset... Please wait..."):
            df = load_large_data(active_file, usecols=visible_columns)
            
        if df is not None:
            filtered_df = df[visible_columns].copy()

            # --- SEARCH ENGINE INTERFACE GENERATION ---
            with side_control_panel:
                with tab_search:
                    st.markdown("### 🔍 Master Filters")
                    st.button("❌ CLEAR ", on_click=clear_all_searches_and_filters, key="reset_search_deck_btn", use_container_width=True)
                    st.markdown("<div style='margin-bottom: 2px;'></div>", unsafe_allow_html=True)
                    
                    with st.form(key="optimized_search_form", border=False):
                        st.text_input(
                            "Main Search Bar:", 
                            placeholder="🔍 Search...",
                            key="global_search_input"
                        )
                        st.markdown("---")
                        st.markdown("### ⚙️Sub-Filters")
                        
                        with st.container(height=400, border=False):
                            for col_name in visible_columns:
                                st.text_input(
                                    f"{col_name}", 
                                    key=f"sidebar_filter_{col_name}",
                                    placeholder=f"🔎 {col_name}..."
                                )
                        
                        st.form_submit_button(label="⚡ RUN SEARCH FILTERS", use_container_width=True)

            # --- SEARCH DATA PROCESSING STRATIFICATION ---
            if st.session_state.get("global_search_input", ""):
                search_query = st.session_state.global_search_input
                masks = [fuzzy_contains(filtered_df[col], search_query) for col in visible_columns]
                global_mask = pd.concat(masks, axis=1).any(axis=1)
                filtered_df = filtered_df[global_mask]

            for col_name in visible_columns:
                search_val = st.session_state.get(f"sidebar_filter_{col_name}", "")
                if search_val:
                    col_mask = fuzzy_contains(filtered_df[col_name], search_val)
                    filtered_df = filtered_df[col_mask]

            # --- EXPORT DECK COMPILATION MANAGEMENT ---
            with side_control_panel:
                with tab_download:
                    st.markdown("### 💾Export Deck")
                    def convert_df_to_excel(df_to_save):
                        output = BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            df_to_save.to_excel(writer, index=False, sheet_name='Filtered_View')
                        return output.getvalue()

                    if not filtered_df.empty:
                        excel_file = convert_df_to_excel(filtered_df)
                        st.download_button(
                            label="👌 Export Excel File",
                            data=excel_file,
                            file_name="Salamat_Nonoy.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True 
                        )
                    else:
                        st.warning("No metrics match your search parameters to compile.")

            # --- MAIN VISUAL CONTENT DATA DISPLAY LAYER ---
            with main_data_window:
                clean_title = os.path.splitext(active_file.name)[0]
                st.markdown(f'<div style="display: flex; align-items: center; gap: 5px; margin-top: -15px; margin-bottom: 2px;"><img src="https://i.pinimg.com/originals/c5/ee/51/c5ee5152fd8575cd966fa258addca1a1.gif" style="height: 100px; width: auto; image-rendering: pixelated; mix-blend-mode: multiply;"><span style="font-size: 30px; font-weight: 700;">{clean_title}</span></div>', unsafe_allow_html=True)
                
                if filtered_df.empty:
                    st.error("🙈😫 **DI MASEARCH NGANIII!!!!** CHECK SPELLING MUNA BAGO SEARCH OR CLEAR FILTERS TAPOS SEARCH ULIT")
                else:
                    st.dataframe(
                        filtered_df,
                        use_container_width=True, 
                        height=650, 
                        hide_index=True,
                        column_config={col: st.column_config.TextColumn(col, width=None, disabled=True) for col in visible_columns}
                    )
                    st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.1rem 0.5rem; background: transparent; border-radius: 6px; font-size: 20px; margin-top: 2px;">
                            <div>
                                📊 <b>Rows Viewable:</b> {len(filtered_df):,} of {len(df):,} records | 📋 <b>Columns Visible:</b> {len(visible_columns)} of {len(all_headers)} columns total
                            </div>
                            <div>
                                <img src="https://dl.glitter-graphics.com/pub/3709/3709531e18qrw4sle.gif" 
                                    style="height: 100px; width: auto; image-rendering: pixelated; mix-blend-mode: multiply; margin-right: 300px;">
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
    else:
        with main_data_window:
            clean_title = os.path.splitext(active_file.name)[0]
            st.markdown(f'<div style="display: flex; align-items: center; gap: 5px; margin-top: -15px; margin-bottom: 2px;"><img src="https://i.pinimg.com/originals/c5/ee/51/c5ee5152fd8575cd966fa258addca1a1.gif" style="height: 100px; width: auto; image-rendering: pixelated; mix-blend-mode: multiply;"><span style="font-size: 30px; font-weight: 700;">{clean_title}</span></div>', unsafe_allow_html=True)
            st.info("💡 **File Staged Successfully!** Please use the **Column Picker** inside the `⚙️1.SETUP` tab on the left to select your targets, then click **APPLY & LOAD COLUMNS**.")
        with side_control_panel:
            with tab_search:
                st.warning("⚠️ Choose columns first.")
            with tab_download:
                st.warning("⚠️ Choose columns first.")