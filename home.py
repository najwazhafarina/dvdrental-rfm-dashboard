import streamlit as st
from sidebar_nav import render_sidebar

st.set_page_config(page_title="DVDRental Analytics", layout="wide", page_icon="🎬")
render_sidebar(active="Overview")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family:'Sora',sans-serif; background:#07111a; color:#cae8f0; }
[data-testid="stAppViewContainer"] { background:#07111a; }
[data-testid="stHeader"] { background:transparent !important; }
.block-container { padding:2.5rem 3rem 4rem !important; }

.hero-eyebrow { font-size:10px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:#14b8a6;margin-bottom:14px; }
.hero-title   { font-size:52px;font-weight:800;letter-spacing:-0.03em;color:#f0fdfa;line-height:1.1;margin-bottom:14px; }
.hero-title span { color:#14b8a6; }
.hero-sub     { font-size:15px;color:#4a7c8a;line-height:1.75;max-width:600px;margin-bottom:36px; }

.stat-strip { display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:40px; }
.stat-box   { background:#0d1f2d;border:1px solid #1a3347;border-radius:14px;padding:20px 22px;position:relative;overflow:hidden; }
.stat-box::before { content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#0d9488,#14b8a6); }
.stat-val { font-size:32px;font-weight:800;color:#f0fdfa;line-height:1; }
.stat-lbl { font-size:11px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#2d5a6a;margin-top:8px; }

.s-label  { font-size:10px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#14b8a6;margin-bottom:14px; }

.cards-grid { display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-bottom:40px; }
.page-card  { background:#0d1f2d;border:1px solid #1a3347;border-radius:16px;padding:26px;position:relative;overflow:hidden; }
.page-card::before { content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:16px 16px 0 0; }
.card-tita::before    { background:linear-gradient(90deg,#2563eb,#60a5fa); }
.card-abel::before    { background:linear-gradient(90deg,#059669,#34d399); }
.card-abigail::before { background:linear-gradient(90deg,#0d9488,#14b8a6); }
.card-enja::before    { background:linear-gradient(90deg,#7c3aed,#a78bfa); }
.card-num   { font-size:10px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#1e4a5a;margin-bottom:12px; }
.card-icon  { font-size:28px;margin-bottom:10px; }
.card-title { font-size:16px;font-weight:700;color:#f0fdfa;margin-bottom:6px; }
.card-badge { display:inline-block;font-size:10px;font-weight:600;padding:3px 10px;border-radius:99px;margin-bottom:12px; }
.badge-tita    { background:rgba(59,130,246,0.12);color:#93c5fd; }
.badge-abel    { background:rgba(52,211,153,0.12);color:#6ee7b7; }
.badge-abigail { background:rgba(20,184,166,0.12);color:#2dd4bf; }
.badge-enja    { background:rgba(167,139,250,0.12);color:#c4b5fd; }
.card-desc  { font-size:13px;color:#2d5a6a;line-height:1.7; }

.team-grid { display:grid;grid-template-columns:repeat(4,1fr);gap:12px; }
.team-card { background:#0d1f2d;border:1px solid #1a3347;border-radius:12px;padding:18px 20px; }
.team-role { font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#1e4a5a;margin-bottom:6px; }
.team-name { font-size:17px;font-weight:700;color:#f0fdfa;margin-bottom:4px; }
.team-topic{ font-size:12px;color:#4a7c8a; }

.ocean-hr  { border:none;border-top:1px solid #0f2535;margin:36px 0; }
.footer    { text-align:center;font-size:12px;color:#1a3347;margin-top:48px;letter-spacing:0.06em; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-eyebrow">📊 Data Science · Mid Exam · DVDRental Database</div>
<div class="hero-title">Understanding Our<br><span>DVD Rental</span> Customers</div>
<div class="hero-sub">
    Analisis menyeluruh database DVDRental — dari siapa pelanggan kita, di mana mereka berada,
    bagaimana mereka berperilaku, hingga prediksi loyalitas berbasis machine learning.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stat-strip">
    <div class="stat-box"><div class="stat-val">599</div><div class="stat-lbl">Total Customers</div></div>
    <div class="stat-box"><div class="stat-val">16,044</div><div class="stat-lbl">Total Rentals</div></div>
    <div class="stat-box"><div class="stat-val">109</div><div class="stat-lbl">Countries</div></div>
    <div class="stat-box"><div class="stat-val">4</div><div class="stat-lbl">Analysis Sections</div></div>
</div>
<hr class="ocean-hr">
<div class="s-label">Dashboard Sections</div>
<div class="cards-grid">
  <div class="page-card card-tita">
    <div class="card-num">Section 01</div><div class="card-icon">👤</div>
    <div class="card-title">Profil & Demografi Pelanggan</div>
    <span class="card-badge badge-tita">Tita</span>
    <div class="card-desc">Siapa pelanggan kita? Status keaktifan, distribusi toko, tren akuisisi dari waktu ke waktu, dan customer segmentation berbasis spending.</div>
  </div>
  <div class="page-card card-abel">
    <div class="card-num">Section 02</div><div class="card-icon">🗺️</div>
    <div class="card-title">Analisis Geografis</div>
    <span class="card-badge badge-abel">Abel</span>
    <div class="card-desc">Dari mana pelanggan kita berasal? Choropleth map global, top country by revenue, dan deep-dive trend per kota & negara.</div>
  </div>
  <div class="page-card card-abigail">
    <div class="card-num">Section 03</div><div class="card-icon">🌊</div>
    <div class="card-title">Aktivitas & Riwayat Sewa</div>
    <span class="card-badge badge-abigail">Abigail</span>
    <div class="card-desc">Siapa yang paling sering menyewa? Kapan waktu tersibuk? Prediksi loyalitas pelanggan dengan RandomForest Classifier ML model.</div>
  </div>
  <div class="page-card card-enja">
    <div class="card-num">Section 04</div><div class="card-icon">🎯</div>
    <div class="card-title">Segmentasi Pelanggan (RFM)</div>
    <span class="card-badge badge-enja">Enja</span>
    <div class="card-desc">Recency · Frequency · Monetary — mengelompokkan pelanggan dari Champions hingga Hibernating untuk strategi marketing yang tepat sasaran.</div>
  </div>
</div>
<hr class="ocean-hr">
<div class="s-label">Our Team</div>
<div class="team-grid">
  <div class="team-card"><div class="team-role">Section 01</div><div class="team-name">Tita</div><div class="team-topic">Profil & Demografi</div></div>
  <div class="team-card"><div class="team-role">Section 02</div><div class="team-name">Abel</div><div class="team-topic">Analisis Geografis</div></div>
  <div class="team-card"><div class="team-role">Section 03</div><div class="team-name">Abigail</div><div class="team-topic">Aktivitas & Riwayat Sewa</div></div>
  <div class="team-card"><div class="team-role">Section 04</div><div class="team-name">Enja</div><div class="team-topic">Segmentasi RFM</div></div>
</div>
<div class="footer">DVDRental Customer Intelligence &nbsp;·&nbsp; Data Science &nbsp;·&nbsp; Mid Exam</div>
""", unsafe_allow_html=True)