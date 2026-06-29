import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from sidebar_nav import render_sidebar

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Rental Activity & History",
    layout="wide",
    page_icon="🎬"
)

# ─── COLOR PALETTE — Ocean Teal ──────────────────────────────────────────────
COLORS = {
    "primary": "#14b8a6",   # teal
    "accent":  "#06b6d4",   # cyan
    "success": "#34d399",   # emerald
    "danger":  "#f87171",   # soft red
    "bg":      "#07111a",   # deep ocean
    "card":    "#0d1f2d",   # card bg
    "border":  "#1a3347",   # border
    "muted":   "#4a7c8a",   # muted teal
    "light":   "#cae8f0",   # light cyan
}
PALETTE = ["#14b8a6", "#06b6d4", "#34d399", "#818cf8", "#f472b6", "#fb923c"]

# ─── CSS — Ocean Teal ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
    background-color: #07111a;
    color: #cae8f0;
}
[data-testid="stAppViewContainer"] { background-color: #07111a; }
[data-testid="stHeader"]           { background-color: transparent !important; }
.block-container { padding: 2.5rem 3rem 4rem !important; max-width: 100% !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #050e15 !important;
    border-right: 1px solid #1a3347 !important;
}
[data-testid="stSidebar"] * { color: #cae8f0 !important; }
[data-testid="stSidebarNav"] { background: #050e15 !important; }

.sidebar-brand {
    background: linear-gradient(135deg, #0e7490, #14b8a6);
    border-radius: 12px; padding: 16px 18px; margin-bottom: 20px;
}
.sidebar-brand-title { color: #fff !important; font-size: 13px; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase; }
.sidebar-brand-sub { color: #a5f3fc !important; font-size: 11px; margin-top: 3px; }

/* ── MAIN TITLE ── */
.main-badge {
    display: inline-block;
    background: rgba(20,184,166,0.1); border: 1px solid rgba(20,184,166,0.3);
    color: #2dd4bf; font-size: 10px; font-weight: 600;
    letter-spacing: 0.14em; text-transform: uppercase;
    padding: 4px 14px; border-radius: 99px; margin-bottom: 16px;
}
.main-title {
    font-size: 44px; font-weight: 800; letter-spacing: -0.03em;
    color: #f0fdfa; line-height: 1.1; margin-bottom: 10px;
}
.main-title span { color: #14b8a6; }
.main-subtitle { color: #4a7c8a; font-size: 14px; line-height: 1.7; margin-bottom: 0; }
.title-divider { border: none; border-top: 1px solid #1a3347; margin: 28px 0; }

/* ── SECTION HEADER ── */
.section-header {
    font-size: 10px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase;
    color: #14b8a6; margin-top: 52px; margin-bottom: 4px; display: block;
}
.section-title {
    font-size: 26px; font-weight: 700; color: #f0fdfa;
    margin-bottom: 4px; margin-top: 2px;
}
.section-desc { color: #4a7c8a; font-size: 13px; margin-bottom: 18px; line-height: 1.65; }
.sub-header {
    font-size: 10px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase;
    color: #2d5a6a; margin-bottom: 14px;
}

/* ── KPI CARDS ── */
.kpi-card {
    background: #0d1f2d;
    border: 1px solid #1a3347;
    border-radius: 16px;
    padding: 24px;
    position: relative; overflow: hidden; min-height: 148px;
}
.kpi-card::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px; border-radius: 16px 16px 0 0;
}
.kpi-teal::before   { background: linear-gradient(90deg, #0d9488, #14b8a6); }
.kpi-cyan::before   { background: linear-gradient(90deg, #0891b2, #06b6d4); }
.kpi-emerald::before{ background: linear-gradient(90deg, #059669, #34d399); }
.kpi-indigo::before { background: linear-gradient(90deg, #4338ca, #818cf8); }

.kpi-label {
    font-size: 10px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase;
    color: #2d5a6a; margin-bottom: 12px;
}
.kpi-value { font-size: 34px; font-weight: 800; color: #f0fdfa; line-height: 1; margin-bottom: 10px; }
.kpi-badge { display: inline-block; font-size: 11px; font-weight: 500; padding: 3px 12px; border-radius: 99px; }
.badge-teal    { background: rgba(20,184,166,0.12);  color: #2dd4bf; }
.badge-cyan    { background: rgba(6,182,212,0.12);   color: #22d3ee; }
.badge-emerald { background: rgba(52,211,153,0.12);  color: #34d399; }
.badge-indigo  { background: rgba(129,140,248,0.12); color: #a5b4fc; }

/* ── CHART CARD ── */
.chart-card {
    background: #0d1f2d; border: 1px solid #1a3347;
    border-radius: 16px; padding: 22px 22px 12px 22px; margin-bottom: 10px;
}

/* ── INSIGHT / PREDICTION ── */
.insight-box {
    background: rgba(20,184,166,0.05); border: 1px solid rgba(20,184,166,0.2);
    border-left: 3px solid #14b8a6; border-radius: 0 12px 12px 0;
    padding: 16px 22px; margin: 16px 0; font-size: 13px; color: #7fb5c5; line-height: 1.85;
}
.insight-box b { color: #a5f3fc; font-weight: 600; }

.prediction-box {
    background: rgba(129,140,248,0.05); border: 1px solid rgba(129,140,248,0.2);
    border-left: 3px solid #818cf8; border-radius: 0 12px 12px 0;
    padding: 16px 22px; margin: 16px 0; font-size: 13px; color: #7fb5c5; line-height: 1.85;
}
.prediction-box b { color: #c7d2fe; font-weight: 600; }

/* ── STRATEGY CARDS ── */
.strat-card-green {
    background: rgba(52,211,153,0.05); border: 1px solid rgba(52,211,153,0.15);
    border-radius: 14px; padding: 24px; height: 100%;
    position: relative; overflow: hidden;
}
.strat-card-green::before {
    content: ''; position: absolute; top:0;left:0;right:0;height:3px;
    background: linear-gradient(90deg,#059669,#34d399); border-radius: 14px 14px 0 0;
}
.strat-card-amber {
    background: rgba(20,184,166,0.05); border: 1px solid rgba(20,184,166,0.15);
    border-radius: 14px; padding: 24px; height: 100%;
    position: relative; overflow: hidden;
}
.strat-card-amber::before {
    content: ''; position: absolute; top:0;left:0;right:0;height:3px;
    background: linear-gradient(90deg,#0d9488,#14b8a6); border-radius: 14px 14px 0 0;
}
.strat-card-red {
    background: rgba(129,140,248,0.05); border: 1px solid rgba(129,140,248,0.15);
    border-radius: 14px; padding: 24px; height: 100%;
    position: relative; overflow: hidden;
}
.strat-card-red::before {
    content: ''; position: absolute; top:0;left:0;right:0;height:3px;
    background: linear-gradient(90deg,#4338ca,#818cf8); border-radius: 14px 14px 0 0;
}
.strat-body { color: #4a7c8a; font-size: 13px; line-height: 1.75; margin-top: 10px; }
.strat-body b { color: #cae8f0; }

/* ── SEARCH INPUT ── */
[data-testid="stTextInput"] input {
    background: #0d1f2d !important; border: 1px solid #1a3347 !important;
    border-radius: 10px !important; color: #cae8f0 !important; font-size: 13px !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #14b8a6 !important; box-shadow: 0 0 0 3px rgba(20,184,166,0.12) !important;
}

/* ── FOOTER ── */
.footer {
    margin-top: 64px; padding: 22px 0; border-top: 1px solid #1a3347;
    font-size: 12px; color: #1a3347; text-align: center; letter-spacing: 0.06em;
}
.footer b { color: #2d5a6a; }
</style>
""", unsafe_allow_html=True)


# ─── DB ───────────────────────────────────────────────────────────────────────
def get_conn():
    return psycopg2.connect(
        host="localhost", database="dvdrental",
        user="postgres", password="satuduaakulupa", port="5432"
    )

GRID = "#f1f5f9"   # shared grid colour

def clean_layout(bg="white"):
    """Base style only — no xaxis/yaxis so callers can pass their own freely."""
    return dict(
        plot_bgcolor=bg, paper_bgcolor=bg,
        font=dict(family="Plus Jakarta Sans", color="#1e293b"),
        margin=dict(t=10, b=10, l=10, r=10),
    )

def ax(title="", grid=True, ticks=True):
    """Helper: build a standard axis dict."""
    return dict(
        title=title,
        showgrid=grid, gridcolor=GRID,
        zeroline=False,
        showticklabels=ticks,
    )


# ─── DATA LOADING ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    conn = get_conn()

    # Top renters
    df_top = pd.read_sql("""
        SELECT c.customer_id,
               CONCAT(c.first_name, ' ', c.last_name) AS full_name,
               COUNT(r.rental_id)  AS total_rentals,
               COALESCE(SUM(p.amount), 0) AS total_spent
        FROM customer c
        JOIN rental r  ON c.customer_id = r.customer_id
        LEFT JOIN payment p ON r.rental_id = p.rental_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        ORDER BY total_rentals DESC
    """, conn)

    # Weekend vs Weekday
    df_wkd = pd.read_sql("""
        SELECT
            CASE WHEN EXTRACT(DOW FROM rental_date) IN (0,6)
                 THEN 'Weekend' ELSE 'Weekday' END AS day_type,
            COUNT(*) AS total
        FROM rental GROUP BY 1
    """, conn)

    # Daily trend
    df_trend = pd.read_sql("""
        SELECT DATE(rental_date) AS date, COUNT(*) AS rentals
        FROM rental GROUP BY 1 ORDER BY 1
    """, conn)

    # Customer behavior base
    df_raw = pd.read_sql("""
        SELECT r.customer_id, r.rental_date,
               CONCAT(c.first_name,' ',c.last_name) AS full_name
        FROM rental r JOIN customer c ON r.customer_id = c.customer_id
    """, conn)

    conn.close()
    return df_top, df_wkd, df_trend, df_raw


df_top, df_wkd, df_trend, df_raw = load_data()

import joblib
import os
from sklearn.linear_model import LinearRegression

# ─── LOAD ML MODEL ────────────────────────────────────────────────────────────
MODEL_PATH       = "rental_model.pkl"
TREND_MODEL_PATH = "rental_trend_model.pkl"
model       = None
trend_data  = None

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

if os.path.exists(TREND_MODEL_PATH):
    trend_data = joblib.load(TREND_MODEL_PATH)

# ─── FEATURE ENGINEERING ──────────────────────────────────────────────────────
df_raw['rental_date'] = pd.to_datetime(df_raw['rental_date'])

df_bhv = df_raw.groupby(['customer_id','full_name']).agg(
    first_rental=('rental_date','min'),
    last_rental =('rental_date','max'),
    total_rentals=('rental_date','count')
).reset_index()

df_bhv['duration_days'] = (df_bhv['last_rental'] - df_bhv['first_rental']).dt.days
df_bhv['frequency']     = df_bhv['total_rentals'] / (df_bhv['duration_days'] + 1)

# ─── ML PREDICTION ────────────────────────────────────────────────────────────
X = df_bhv[['frequency', 'duration_days']]

if model is not None:
    # Real RandomForest predictions
    raw_preds = model.predict(X)

    # Remap model labels → rental-behaviour labels (distinct from Enja's RFM segments)
    label_map = {'Loyal': 'High Engagement', 'At Risk': 'Low Engagement'}
    df_bhv['predicted_segment'] = [label_map.get(p, p) for p in raw_preds]

    # predict_proba — get probability of "High Engagement" class (originally "Loyal")
    classes = list(model.classes_)
    loyal_idx = classes.index('Loyal') if 'Loyal' in classes else 0
    df_bhv['loyal_prob'] = model.predict_proba(X)[:, loyal_idx]

    loyal_pct = (df_bhv['predicted_segment'] == 'High Engagement').mean() * 100
    at_risk_n = (df_bhv['predicted_segment'] == 'Low Engagement').sum()
    avg_loyal_prob = df_bhv['loyal_prob'].mean() * 100
    model_active = True
else:
    # Fallback: rule-based if model file missing
    st.warning("⚠️ rental_model.pkl not found — using rule-based fallback. Run train_model.py first.")
    threshold = df_bhv['frequency'].median()
    df_bhv['predicted_segment'] = df_bhv['frequency'].apply(
        lambda x: 'High Engagement' if x > threshold else 'Low Engagement'
    )
    df_bhv['loyal_prob'] = df_bhv['frequency'] / df_bhv['frequency'].max()
    loyal_pct = (df_bhv['predicted_segment'] == 'High Engagement').mean() * 100
    at_risk_n = (df_bhv['predicted_segment'] == 'Low Engagement').sum()
    avg_loyal_prob = loyal_pct
    model_active = False

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
render_sidebar(
    active="Aktivitas & Riwayat Sewa",
    analyst="Abigail",
    section="Aktivitas & Riwayat Sewa"
)

# ─── MAIN TITLE ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-title">🎬 Aktivitas & Riwayat Sewa</div>
<div class="main-subtitle">Analisis mendalam perilaku penyewaan DVD — siapa menyewa, kapan, dan seberapa loyal.</div>
<hr class="title-divider"/>
""", unsafe_allow_html=True)


# ─── KPI ──────────────────────────────────────────────────────────────────────
total_rentals   = df_top['total_rentals'].sum()
total_customers = len(df_top)
top10_contrib   = df_top.head(10)['total_rentals'].sum() / total_rentals
weekend_total   = df_wkd[df_wkd['day_type']=='Weekend']['total'].values[0]
weekend_ratio   = weekend_total / df_wkd['total'].sum()
avg_rentals     = df_bhv['total_rentals'].mean()

c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"""
<div class="kpi-card kpi-teal">
    <div class="kpi-label">Total Rentals</div>
    <div class="kpi-value">{total_rentals:,}</div>
    <span class="kpi-badge badge-teal">{total_customers:,} customers</span>
</div>""", unsafe_allow_html=True)

c2.markdown(f"""
<div class="kpi-card kpi-cyan">
    <div class="kpi-label">Top 10 Contribution</div>
    <div class="kpi-value">{top10_contrib:.0%}</div>
    <span class="kpi-badge badge-cyan">of all rentals</span>
</div>""", unsafe_allow_html=True)

c3.markdown(f"""
<div class="kpi-card kpi-emerald">
    <div class="kpi-label">Weekend Activity</div>
    <div class="kpi-value">{weekend_ratio:.0%}</div>
    <span class="kpi-badge badge-emerald">vs {1-weekend_ratio:.0%} weekday</span>
</div>""", unsafe_allow_html=True)

model_tag = "RandomForest" if model_active else "Rule-based"
c4.markdown(f"""
<div class="kpi-card kpi-indigo">
    <div class="kpi-label">High Engagement ({model_tag})</div>
    <div class="kpi-value">{loyal_pct:.1f}%</div>
    <span class="kpi-badge badge-indigo">{at_risk_n} low-engagement customers</span>
</div>""", unsafe_allow_html=True)


# ─── SECTION 1: VOLUME SEWA ────────────────────────────────────────────────────
st.markdown('<div class="section-header">Volume Sewa</div><div class="section-title">Who Rents the Most?</div>', unsafe_allow_html=True)
st.markdown('<p class="section-desc">Ranking pelanggan berdasarkan volume sewa — mengidentifikasi top renters yang menjadi tulang punggung bisnis.</p>', unsafe_allow_html=True)

_f1, _f2 = st.columns([1, 3])
with _f1:
    top_n = st.slider("Tampilkan Top N Pelanggan", 5, 20, 10, key="top_n_slider")

df_top_n = df_top.head(top_n).sort_values('total_rentals')
fig_bar = go.Figure(go.Bar(
    x=df_top_n['total_rentals'],
    y=df_top_n['full_name'],
    orientation='h',
    marker=dict(
        color=df_top_n['total_rentals'],
        colorscale=[[0, '#0e4d5a'], [1, '#14b8a6']],
        line=dict(width=0),
    ),
    text=[f"{v}" for v in df_top_n['total_rentals']],
    textposition='outside',
    textfont=dict(size=12, color='#64748b'),
))
fig_bar.update_layout(**clean_layout(), height=360)
fig_bar.update_layout(
    xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
               title=dict(text="Total Rentals", font=dict(size=12, color='#4a7c8a'))),
    yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=12, color='#7fb5c5')),
    bargap=0.25,
)
st.markdown('<div class="chart-card"><p class="sub-header">Top Customers by Rental Volume</p>', unsafe_allow_html=True)
st.plotly_chart(fig_bar, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="insight-box">
    📌 <b>Insight:</b> Hanya <b>10% pelanggan teratas</b> menyumbang <b>{top10_contrib:.0%} dari total transaksi sewa</b>.
    Bisnis sangat bergantung pada kelompok kecil ini — menjaga loyalitas mereka adalah prioritas utama.
</div>
""", unsafe_allow_html=True)


# ─── SECTION 2: TREN WAKTU ────────────────────────────────────────────────────
st.markdown('<div class="section-header">Tren Waktu</div><div class="section-title">When Do They Rent?</div>', unsafe_allow_html=True)
st.markdown('<p class="section-desc">Analisis pola waktu penyewaan — kapan permintaan paling tinggi dan bagaimana trennya dari waktu ke waktu.</p>', unsafe_allow_html=True)

col_c, col_d = st.columns([1, 2])

with col_c:
    fig_pie = go.Figure(go.Pie(
        labels=df_wkd['day_type'],
        values=df_wkd['total'],
        hole=0.62,
        marker=dict(
            colors=['#14b8a6', '#1a3347'],
            line=dict(color='#07111a', width=2),
        ),
        textfont=dict(size=13, family='Plus Jakarta Sans'),
        textinfo='label+percent',
    ))
    fig_pie.update_layout(
        paper_bgcolor='#0d1f2d', plot_bgcolor='#0d1f2d',
        font=dict(family='Sora', color='#7fb5c5'),
        legend=dict(font=dict(size=11), bgcolor='white', orientation='h',
                    yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(t=10, b=10, l=10, r=10),
        annotations=[],
        height=300,
    )
    st.markdown('<div class="chart-card"><p class="sub-header">Weekend vs Weekday</p>', unsafe_allow_html=True)
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_d:
    df_trend['date'] = pd.to_datetime(df_trend['date'])
    df_trend['rolling_7'] = df_trend['rentals'].rolling(7).mean()

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=df_trend['date'], y=df_trend['rentals'],
        line=dict(color='#0e7490', width=1),
        name='Daily Rentals', fill='tozeroy', fillcolor='rgba(14,116,144,0.15)',
    ))
    fig_trend.add_trace(go.Scatter(
        x=df_trend['date'], y=df_trend['rolling_7'],
        line=dict(color='#06b6d4', width=2.5),
        name='7-day Moving Avg',
    ))
    fig_trend.update_layout(
        **clean_layout(),
        legend=dict(font=dict(size=11), bgcolor='#0d1f2d', orientation='h',
                    yanchor='bottom', y=1, xanchor='right', x=1),
        height=300,
    )
    fig_trend.update_layout(
        xaxis=dict(title="Date",    showgrid=True, gridcolor=GRID, zeroline=False),
        yaxis=dict(title="Rentals", showgrid=True, gridcolor=GRID, zeroline=False),
    )
    st.markdown('<div class="chart-card"><p class="sub-header">Daily Rental Trend (with 7-Day Moving Average)</p>', unsafe_allow_html=True)
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)




# ─── SECTION 3: DURASI HUBUNGAN ───────────────────────────────────────────────
st.markdown('<div class="section-header">Durasi Hubungan</div><div class="section-title">How Long Do They Stay?</div>', unsafe_allow_html=True)
st.markdown('<p class="section-desc">Durasi hubungan pelanggan — seberapa lama mereka aktif menyewa dan apa maknanya bagi retensi.</p>', unsafe_allow_html=True)

seg_opts = sorted(df_bhv['predicted_segment'].unique())
seg_sel  = st.multiselect(
    "Filter Loyalty Segment:",
    options=seg_opts, default=seg_opts,
    key="seg_filter"
)
dff_bhv = df_bhv[df_bhv['predicted_segment'].isin(seg_sel)].copy()

seg_color_map = {
    'High Engagement':  '#14b8a6',
    'Promising':        '#06b6d4',
    'Needs Attention':  '#fbbf24',
    'Low Engagement':   '#f87171',
}

col_e, col_f = st.columns([2,1])

with col_e:
    fig_scat = px.scatter(
        dff_bhv,
        x='duration_days', y='total_rentals',
        color='predicted_segment',
        size='total_rentals',
        hover_name='full_name',
        color_discrete_map=seg_color_map,
        labels={
            'duration_days':      'Customer Duration (Days)',
            'total_rentals':      'Total Rentals',
            'predicted_segment':  'Predicted Segment',
        },
    )
    fig_scat.update_layout(
        **clean_layout(),
        legend=dict(font=dict(size=11), bgcolor='#0d1f2d', orientation='h',
                    yanchor='bottom', y=1, xanchor='right', x=1),
        height=380,
    )
    st.plotly_chart(fig_scat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_f:
    seg_dist = dff_bhv['predicted_segment'].value_counts().reset_index()
    seg_dist.columns = ['Segment', 'Count']
    fig_seg = go.Figure(go.Bar(
        x=seg_dist['Count'],
        y=seg_dist['Segment'],
        orientation='h',
        marker=dict(
            color=[seg_color_map.get(s,'#94a3b8') for s in seg_dist['Segment']],
            line=dict(width=0),
        ),
        text=seg_dist['Count'],
        textposition='outside',
        textfont=dict(size=12, color='#64748b'),
    ))
    fig_seg.update_layout(
        **clean_layout(),
        height=380,
    )
    fig_seg.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=12)),
    )
    st.markdown('<div class="chart-card"><p class="sub-header">Loyalty Segment Distribution</p>', unsafe_allow_html=True)
    st.plotly_chart(fig_seg, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

avg_dur_loyal   = df_bhv[df_bhv['predicted_segment']=='High Engagement']['duration_days'].mean()
avg_dur_atrisk  = df_bhv[df_bhv['predicted_segment']=='Low Engagement']['duration_days'].mean()

st.markdown(f"""
<div class="insight-box">
    📌 <b>Insight:</b> Pelanggan <b>High Engagement</b> rata-rata aktif selama <b>{avg_dur_loyal:.0f} hari</b>,
    sementara segmen <b>Low Engagement</b> hanya <b>{avg_dur_atrisk:.0f} hari</b>.
    Durasi hubungan yang panjang berkorelasi kuat dengan volume sewa — pelanggan yang bertahan lama
    cenderung menyewa lebih sering dan berkontribusi lebih besar terhadap revenue.
</div>
""", unsafe_allow_html=True)


# ─── SECTION 4: ML PREDICTION — SALES TREND ──────────────────────────────────
st.markdown('<div class="section-header">ML Prediction</div><div class="section-title">Will Rental Volume Recover?</div>', unsafe_allow_html=True)
st.markdown('<p class="section-desc">Linear Regression dilatih dari data daily rental historis untuk memproyeksikan apakah volume sewa akan naik atau turun ke depannya.</p>', unsafe_allow_html=True)

if trend_data is not None:
    lr_model   = trend_data["model"]
    origin     = pd.Timestamp(trend_data["origin"])
    last_date  = pd.Timestamp(trend_data["last_date"])
    resid_std  = trend_data["resid_std"]
    slope      = trend_data["slope"]
    r2         = trend_data["r2"]

    # ── Historical fitted line (last 90 days of actual data) ──
    df_trend_hist = df_trend.copy()
    df_trend_hist['date'] = pd.to_datetime(df_trend_hist['date'])
    df_trend_hist = df_trend_hist[df_trend_hist['date'] >= df_trend_hist['date'].max() - pd.Timedelta(days=90)]
    df_trend_hist['day_num'] = (df_trend_hist['date'] - origin).dt.days
    df_trend_hist['fitted']  = lr_model.predict(df_trend_hist[['day_num']])

    # ── Forecast: 5 months after last data point ──
    forecast_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=30,    # ~1 month (lebih honest untuk R²=0.12)
        freq='D'
    )
    forecast_day_nums = (forecast_dates - origin).days.values.reshape(-1, 1)
    forecast_vals     = lr_model.predict(forecast_day_nums)
    forecast_upper    = forecast_vals + 1.96 * resid_std
    forecast_lower    = np.maximum(0, forecast_vals - 1.96 * resid_std)

    is_declining = slope < 0
    trend_color  = '#f87171' if is_declining else '#34d399'
    trend_label  = f"📉 TURUN ({slope:.2f} rentals/day)" if is_declining else f"📈 NAIK ({slope:.2f} rentals/day)"
    trend_msg    = (
        "Model memprediksi volume sewa akan <b>terus menurun</b> tanpa intervensi. "
        "Ini konsisten dengan data historis yang menunjukkan penurunan sejak Sep 2005."
        if is_declining else
        "Model memprediksi volume sewa akan <b>mengalami pemulihan</b>."
    )

    fig_fore = go.Figure()

    # Actual (last 90 days)
    fig_fore.add_trace(go.Scatter(
        x=df_trend_hist['date'], y=df_trend_hist['rentals'],
        line=dict(color='#06b6d4', width=1.5),
        fill='tozeroy', fillcolor='rgba(6,182,212,0.10)',
        name='Actual (Last 90 Days)',
    ))
    # Fitted line on historical
    fig_fore.add_trace(go.Scatter(
        x=df_trend_hist['date'], y=df_trend_hist['fitted'],
        line=dict(color='#06b6d4', width=1.5, dash='dot'),
        name='Linear Trend (Historical)',
    ))
    # Confidence band (forecast)
    fig_fore.add_trace(go.Scatter(
        x=list(forecast_dates) + list(forecast_dates[::-1]),
        y=list(forecast_upper) + list(forecast_lower[::-1]),
        fill='toself',
        fillcolor=f"rgba({'248,113,113' if is_declining else '52,211,153'},0.08)",
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=False, name='95% Confidence Band',
    ))
    # Forecast line
    fig_fore.add_trace(go.Scatter(
        x=forecast_dates, y=forecast_vals,
        line=dict(color=trend_color, width=2.5),
        name=f'Forecast ({last_date.strftime("%b %Y")} → {forecast_dates[-1].strftime("%b %Y")})',
    ))
    # Vertical "today" marker
    fig_fore.add_vline(
        x=int(last_date.timestamp() * 1000), line_dash="dash", line_color="#2d5a6a",
        annotation_text="Data ends",
        annotation_position="top right",
        annotation_font_color="#4a7c8a",
    )

    fig_fore.update_layout(
        **clean_layout(),
        legend=dict(font=dict(size=11), bgcolor='#0d1f2d', orientation='h',
                    yanchor='bottom', y=1, xanchor='right', x=1),
        height=340,
    )
    fig_fore.update_layout(
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, color='#7fb5c5'),
        yaxis=dict(title="Daily Rentals", showgrid=True, gridcolor=GRID,
                   zeroline=False, color='#7fb5c5', rangemode='tozero'),
    )

    st.markdown('<div class="chart-card"><p class="sub-header">Rental Volume Forecast — Linear Regression · 95% Confidence Band</p>', unsafe_allow_html=True)
    st.plotly_chart(fig_fore, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # KPI row
    fc_kpi1, fc_kpi2, fc_kpi3 = st.columns(3)
    fc_kpi1.markdown(f"""
    <div class="kpi-card kpi-teal" style="margin-top:12px;">
        <div class="kpi-label">Trend Direction</div>
        <div class="kpi-value" style="font-size:22px;color:{'#f87171' if is_declining else '#34d399'};">{trend_label}</div>
        <span class="kpi-badge {'badge-indigo' if not is_declining else 'badge-teal'}" style="margin-top:6px;">R² = {r2:.3f}</span>
    </div>""", unsafe_allow_html=True)
    fc_kpi2.markdown(f"""
    <div class="kpi-card kpi-cyan" style="margin-top:12px;">
        <div class="kpi-label">Forecast End Date</div>
        <div class="kpi-value" style="font-size:22px;">{forecast_dates[-1].strftime("%b %Y")}</div>
        <span class="kpi-badge badge-cyan">30 days ahead</span>
    </div>""", unsafe_allow_html=True)
    fc_kpi3.markdown(f"""
    <div class="kpi-card kpi-indigo" style="margin-top:12px;">
        <div class="kpi-label">Predicted Avg (Month 5)</div>
        <div class="kpi-value" style="font-size:22px;">{max(0,forecast_vals[-30:].mean()):.0f}</div>
        <span class="kpi-badge badge-indigo">rentals/day</span>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="prediction-box" style="margin-top:14px;">
        📉 <b>Prediksi Trend:</b> {trend_msg}
        <br>
        Forecast mencakup <b>30 hari ke depan</b> ({(last_date + pd.Timedelta(days=1)).strftime('%d %b %Y')}
        → {forecast_dates[-1].strftime('%d %b %Y')}) dengan confidence interval 95%.
        <br><small style="color:#7fb5c5;opacity:0.75;">
        Model: <b>Linear Regression</b> · R² = {r2:.3f} (model bersifat indikatif, cocok untuk melihat arah tren) ·
        slope = {slope:.4f} rentals/day ·
        dilatih dari data rental {origin.strftime('%b %Y')}–{last_date.strftime('%b %Y')}
        </small>
    </div>
    """, unsafe_allow_html=True)

else:
    st.warning("⚠️ rental_trend_model.pkl tidak ditemukan. Jalankan train_model.py terlebih dahulu.")


# ─── SECTION 5: STRATEGIC ACTIONS ─────────────────────────────────────────────
st.markdown('<div class="section-header">Rekomendasi</div><div class="section-title">Strategic Action Plan</div>', unsafe_allow_html=True)
st.markdown('<p class="section-desc">Rekomendasi berbasis data untuk meningkatkan aktivitas sewa dan retensi pelanggan.</p>', unsafe_allow_html=True)

r1, r2, r3 = st.columns(3)

with r1:
    st.markdown(f"""
    <div class="strat-card-green">
        <p style="font-size:13px;font-weight:700;color:#34d399;margin:0 0 10px 0;">🏆 Retain Top Renters</p>
        <p class="strat-body">Top 10 pelanggan menyumbang <b>{top10_contrib:.0%}</b> dari total sewa.
        Berikan <b>VIP Membership</b> atau <b>priority access</b> ke film baru
        untuk memastikan mereka tidak beralih ke kompetitor.</p>
    </div>""", unsafe_allow_html=True)

with r2:
    st.markdown(f"""
    <div class="strat-card-amber">
        <p style="font-size:13px;font-weight:700;color:#14b8a6;margin:0 0 10px 0;">🌊 Weekend Flash Promo</p>
        <p class="strat-body">Dengan <b>{weekend_ratio:.0%} transaksi di weekend</b>, jalankan promo
        <b>"Weekend Special"</b> — diskon 15% untuk penyewaan Sabtu-Minggu
        guna mendorong volume sewa lebih tinggi.</p>
    </div>""", unsafe_allow_html=True)

with r3:
    st.markdown(f"""
    <div class="strat-card-red">
        <p style="font-size:13px;font-weight:700;color:#a5b4fc;margin:0 0 10px 0;">⚠️ Re-engage Low-Engagement</p>
        <p class="strat-body"><b>{at_risk_n} pelanggan</b> teridentifikasi sebagai Low Engagement.
        Kirimkan <b>email "We Miss You"</b> dengan voucher gratis 1 rental
        untuk mendorong mereka kembali aktif sebelum benar-benar hilang.</p>
    </div>""", unsafe_allow_html=True)


# ─── CUSTOMER DETAIL TABLE ────────────────────────────────────────────────────
st.markdown('<div class="section-header">Data Explorer</div><div class="section-title">Customer Detail</div>', unsafe_allow_html=True)
st.markdown('<p class="section-desc">Telusuri data individual pelanggan beserta segmen prediksi loyalitas mereka.</p>', unsafe_allow_html=True)

search = st.text_input("🔍 Cari nama pelanggan:", placeholder="Ketik nama pelanggan...")
tbl = dff_bhv.copy()
if search:
    tbl = tbl[tbl['full_name'].str.contains(search, case=False, na=False)]

tbl['loyal_prob_pct'] = (tbl['loyal_prob'] * 100).round(1).astype(str) + '%'
tbl['frequency_int'] = tbl['frequency'].round(2)  # keep 2dp — it's rentals/day ratio
st.dataframe(
    tbl.sort_values('total_rentals', ascending=False)[[
        'full_name','total_rentals','duration_days','frequency_int','loyal_prob_pct','predicted_segment'
    ]].rename(columns={
        'full_name':          'Customer Name',
        'total_rentals':      'Total Rentals',
        'duration_days':      'Duration (Days)',
        'frequency_int':      'Rental Frequency',
        'loyal_prob_pct':     '🔮 Engagement Probability',
        'predicted_segment':  'RF Prediction (Engagement)',
    }).reset_index(drop=True),
    use_container_width=True,
    height=300,
    column_config={
        "Rental Frequency": st.column_config.NumberColumn(format="%.2f"),
    }
)


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Rental Activity & History Dashboard &nbsp;·&nbsp; Analyst: <strong>Abigail</strong> &nbsp;·&nbsp; DVDRental — Section 3
</div>
""", unsafe_allow_html=True)
