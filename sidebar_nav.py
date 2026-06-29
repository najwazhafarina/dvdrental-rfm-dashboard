import streamlit as st

# ─── Shared sidebar CSS ──────────────────────────────────────────────────────
# Aku tambahkan rule untuk menyembunyikan file uploader & widget bawaan di sidebar
SIDEBAR_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&display=swap');

[data-testid="stSidebar"] {
    background: #050e15 !important;
    border-right: 1px solid #0f2535 !important;
    min-width: 230px !important;
}
[data-testid="stSidebar"] * { font-family: 'Sora', sans-serif !important; }

/* Menyembunyikan Navigasi asli & File Uploader bawaan Streamlit di Sidebar */
[data-testid="stSidebarNav"], 
[data-testid="stSidebar"] [data-testid="stFileUploader"],
[data-testid="stSidebar"] .stFileUploader { 
    display: none !important; 
}

.nav-brand {
    background: linear-gradient(135deg, #0e7490, #14b8a6);
    border-radius: 12px; padding: 16px 18px; margin-bottom: 22px;
}
.nav-brand-icon  { font-size: 22px; margin-bottom: 4px; }
.nav-brand-title { color: #fff !important; font-size: 13px; font-weight: 700;
                   letter-spacing: 0.07em; text-transform: uppercase; margin: 0; }
.nav-brand-sub   { color: #a5f3fc !important; font-size: 11px; margin-top: 2px; }

.nav-label {
    font-size: 10px; font-weight: 700; letter-spacing: 0.16em;
    text-transform: uppercase; color: #1e4a5a; margin: 0 0 8px 2px;
}

.nav-item {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 12px; border-radius: 8px; margin-bottom: 4px;
    font-size: 13px; font-weight: 500; color: #4a7c8a !important;
    cursor: pointer; transition: all 0.2s;
    text-decoration: none !important;
}
.nav-item:hover { background: rgba(20,184,166,0.08); color: #7fb5c5 !important; }
.nav-item.active {
    background: rgba(20,184,166,0.12) !important;
    border-left: 3px solid #14b8a6;
    color: #2dd4bf !important; font-weight: 600;
}
.nav-icon { font-size: 16px; width: 22px; text-align: center; }

.nav-divider { border: none; border-top: 1px solid #0f2535; margin: 16px 0; }

.nav-analyst {
    padding: 12px; border-radius: 10px;
    background: rgba(20,184,166,0.04); border: 1px solid #0f2535;
}
.nav-analyst-row { font-size: 11px; line-height: 2; }
.nav-analyst-label { color: #1e4a5a !important; }
.nav-analyst-val   { color: #7fb5c5 !important; font-weight: 600; }
</style>
"""

# ─── Pages config ──────────────────────────────────────────────────────────────
PAGES = [
    {"icon": "🏠", "label": "Overview",                 "path": "/"},
    {"icon": "👤", "label": "Profil Pelanggan",         "path": "TITA"},
    {"icon": "🗺️", "label": "Analisis Geografis",       "path": "ABEL"},
    {"icon": "🌊", "label": "Aktivitas & Riwayat Sewa", "path": "ABIGAIL"},
    {"icon": "🎯", "label": "Segmentasi RFM",           "path": "ENJA"},
]

def render_sidebar(active: str, analyst: str = "", section: str = ""):
    st.sidebar.markdown(SIDEBAR_CSS, unsafe_allow_html=True)

    # ── Brand ──
    st.sidebar.markdown("""
    <div class="nav-brand">
        <div class="nav-brand-icon">🎬</div>
        <div class="nav-brand-title">DVDRental Analytics</div>
        <div class="nav-brand-sub">Customer Intelligence</div>
    </div>
    <div class="nav-label">Navigation</div>
    """, unsafe_allow_html=True)

    # ── Nav items ──
    for page in PAGES:
        is_active = page["label"] == active
        cls = "nav-item active" if is_active else "nav-item"
        
        # Link navigasi menggunakan <a> tag
        st.sidebar.markdown(
            f'''
            <a href="{page["path"]}" target="_self" style="text-decoration: none;">
                <div class="{cls}">
                    <span class="nav-icon">{page["icon"]}</span>
                    <span>{page["label"]}</span>
                </div>
            </a>
            ''',
            unsafe_allow_html=True,
        )

    # ── Divider + analyst info ──
    if analyst:
        st.sidebar.markdown(f"""
        <hr class="nav-divider">
        <div class="nav-analyst">
            <div class="nav-analyst-row">
                <span class="nav-analyst-label">Analyst &nbsp;</span>
                <span class="nav-analyst-val">{analyst}</span>
            </div>
            <div class="nav-analyst-row">
                <span class="nav-analyst-label">Section &nbsp;</span>
                <span class="nav-analyst-val">{section}</span>
            </div>
            <div class="nav-analyst-row">
                <span class="nav-analyst-label">Database &nbsp;</span>
                <span class="nav-analyst-val">PostgreSQL</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown('<hr class="nav-divider">', unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div style="font-size:10px; color:#1e4a5a; text-align:center; margin-top:15px; letter-spacing:0.1em;">
        MID EXAM · DATA SCIENCE
    </div>
    """, unsafe_allow_html=True)