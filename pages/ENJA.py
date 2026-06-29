import streamlit as st
import psycopg2
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sidebar_nav import render_sidebar

st.set_page_config(page_title="RFM Analysis", layout="wide", page_icon="🎯")
render_sidebar(active="RFM Segmentation", analyst="Enja", section="RFM Analysis")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d1117;
    color: #cbd5e1;
}

[data-testid="stAppViewContainer"] { background-color: #0d1117; }
[data-testid="stHeader"]           { display: none; }
[data-testid="stToolbar"]          { display: none; }
header                             { display: none !important; }
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 100% !important; }

.kpi-grid {
    display: grid; grid-template-columns: repeat(4, minmax(0,1fr));
    gap: 10px; margin-bottom: 1.25rem;
}
.kpi-card {
    background: #131922; border: 0.5px solid #1e2635;
    border-radius: 10px; padding: 18px 20px;
    position: relative; overflow: hidden;
}
.kpi-card::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
}
.kpi-blue::before   { background: linear-gradient(90deg, #4f8aff, #00c6ff); }
.kpi-purple::before { background: linear-gradient(90deg, #a78bfa, #c084fc); }
.kpi-amber::before  { background: linear-gradient(90deg, #fb923c, #fbbf24); }
.kpi-teal::before   { background: linear-gradient(90deg, #2dd4bf, #34d399); }
.kpi-red::before    { background: linear-gradient(90deg, #f87171, #fb923c); }

.kpi-lbl  { font-size: 10px; font-weight: 500; text-transform: uppercase;
    letter-spacing: 0.09em; color: #64748b; margin-bottom: 8px; }
.kpi-val  { font-size: 26px; font-weight: 600; color: #f1f5f9; line-height: 1.1; }
.kpi-sub  { font-size: 12px; color: #475569; margin-top: 5px; }

.seg-legend {
    display: flex; gap: 10px; margin-bottom: 1.25rem; flex-wrap: wrap;
}
.seg-badge {
    display: flex; align-items: center; gap: 7px;
    background: #131922; border: 0.5px solid #1e2635;
    border-radius: 20px; padding: 6px 14px;
    font-size: 12px; color: #94a3b8;
}
.seg-dot { width: 8px; height: 8px; border-radius: 50%; }

.chart-card {
    background: #131922; border: 0.5px solid #1e2635;
    border-radius: 12px; padding: 18px 20px;
}
.card-title {
    font-size: 10px; font-weight: 500; text-transform: uppercase;
    letter-spacing: 0.1em; color: #64748b; margin-bottom: 14px;
}

.insight-bar {
    background: #131922; border: 0.5px solid #1e2635;
    border-left: 2px solid #4f8aff; border-radius: 0 10px 10px 0;
    padding: 14px 20px; margin: 1.25rem 0;
    font-size: 13px; color: #64748b; line-height: 1.75;
}
.insight-bar b { color: #cbd5e1; font-weight: 500; }

.section-label {
    font-size: 10px; font-weight: 500; text-transform: uppercase;
    letter-spacing: 0.1em; color: #475569; margin-bottom: 10px; margin-top: 1.5rem;
}

[data-testid="stCheckbox"] { background: transparent !important; }
[data-testid="stCheckbox"] label {
    font-size: 13px !important; color: #94a3b8 !important;
    font-family: 'DM Sans', sans-serif !important; background: transparent !important;
}
[data-testid="stCheckbox"] label:hover { color: #e2e8f0 !important; }
[data-testid="stCheckbox"] > label > div:first-child { background: transparent !important; }

.stDownloadButton > button {
    background: transparent !important; color: #4f8aff !important;
    border: 0.5px solid #4f8aff !important; border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 12px !important;
    font-weight: 500 !important; height: 36px !important;
}
.stDownloadButton > button:hover { background: #4f8aff15 !important; }

.footer {
    text-align: center; color: #1e2635; font-size: 12px;
    margin-top: 3rem; padding-top: 1rem; border-top: 0.5px solid #1e2635;
}

.desc-table {
    width: 100%; border-collapse: collapse; font-size: 13px;
}
.desc-table thead tr {
    border-bottom: 0.5px solid #1e2635;
}
.desc-table th {
    color: #475569; font-weight: 500; padding: 8px 14px; text-align: right;
}
.desc-table th:first-child { text-align: left; }
.desc-table tbody tr {
    border-bottom: 0.5px solid #131922;
    transition: background 0.15s;
}
.desc-table tbody tr:hover { background: #0d111780; }
.desc-table td {
    padding: 9px 14px; color: #cbd5e1; text-align: right;
}
.desc-table td:first-child {
    color: #64748b; font-weight: 500; text-align: left;
}
.desc-table .highlight-row td { color: #f1f5f9; }
</style>
""", unsafe_allow_html=True)

def get_conn():
    return psycopg2.connect(
        host="localhost", database="dvdrental",
        user="postgres", password="satuduaakulupa", port="5432"
    )

@st.cache_data
def load_data():
    try:
        conn = get_conn()
        df = pd.read_sql("""
            SELECT
                c.customer_id,
                CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
                c.email,
                MAX(r.rental_date)          AS last_rental,
                COUNT(DISTINCT r.rental_id) AS frequency,
                COALESCE(SUM(p.amount), 0)  AS monetary
            FROM customer c
            LEFT JOIN rental  r ON c.customer_id = r.customer_id
            LEFT JOIN payment p ON c.customer_id = p.customer_id
            GROUP BY c.customer_id, c.first_name, c.last_name, c.email
            HAVING COUNT(DISTINCT r.rental_id) > 0
        """, conn)
        conn.close()

        df['last_rental'] = pd.to_datetime(df['last_rental'])
        ref = df['last_rental'].max()
        df['recency'] = (ref - df['last_rental']).dt.days

        df['r_score'] = np.where(df['recency'] == 0, 3,
                        np.where(df['recency'] <= 175, 2, 1))

        df['f_score'] = np.where(df['frequency'] >= 30, 3,
                        np.where(df['frequency'] >= 23, 2, 1))

        df['m_score'] = np.where(df['monetary'] >= 3439, 3,
                        np.where(df['monetary'] >= 2041, 2, 1))

        df['rfm_score'] = df['r_score'] + df['f_score'] + df['m_score']

        df['segment'] = np.where(df['rfm_score'] >= 8, 'Champions',
                        np.where(df['rfm_score'] >= 6, 'Regular',
                        np.where(df['rfm_score'] >= 4, 'At Risk', 'Low Value')))

        return df
    except Exception as e:
        st.error(f"Connection error: {e}")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

SEG_COLORS = {
    'Champions': '#4f8aff',
    'Regular':   '#2dd4bf',
    'At Risk':   '#fb923c',
    'Low Value': '#f87171',
}

SEG_DESC = {
    'Champions': 'Score 8–9 — best performing customers across dimensions · retain & reward',
    'Regular':   'Score 6–7 — moderately performing with growth potential · push toward Champions',
    'At Risk':   'Score 4–5 — performance declining in at least one dimension · immediate reactivation needed',
    'Low Value': 'Score 3 — lowest performance across all dimensions · needs initial engagement',
}

BG     = 'rgba(0,0,0,0)'
GRID_C = '#1e2635'
TICK_C = '#475569'
TEXT_C = '#94a3b8'

PLOT_BASE = dict(
    paper_bgcolor=BG, plot_bgcolor=BG,
    font=dict(family='DM Sans', color=TEXT_C, size=11),
    margin=dict(t=8, b=8, l=8, r=8),
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding-top:0.5rem;margin-bottom:1.5rem;padding-bottom:1.25rem;border-bottom:0.5px solid #1e2635;">
    <p style="font-size:11px;font-weight:500;letter-spacing:0.12em;text-transform:uppercase;
        color:#4f8aff;margin:0 0 6px 0;line-height:1;">Data Science · RFM Analysis</p>
    <h1 style="font-size:24px;font-weight:600;color:#f1f5f9;margin:0 0 4px 0;line-height:1.2;
        font-family:'DM Sans',sans-serif;">Customer Segmentation</h1>
    <p style="font-size:13px;color:#64748b;margin:0;line-height:1;">Recency · Frequency · Monetary — DVDRental Database</p>
</div>
""", unsafe_allow_html=True)

# ── Legend badges ─────────────────────────────────────────────────────────────
badges_html = '<div class="seg-legend">'
for seg, color in SEG_COLORS.items():
    badges_html += f'''
    <div class="seg-badge">
        <div class="seg-dot" style="background:{color};"></div>
        <span><b style="color:#e2e8f0;">{seg}</b> &nbsp;·&nbsp; {SEG_DESC[seg]}</span>
    </div>'''
badges_html += '</div>'
st.markdown(badges_html, unsafe_allow_html=True)

dff = df.copy()

# ── KPI ───────────────────────────────────────────────────────────────────────
total    = len(dff)
champ_n  = len(dff[dff['segment'] == 'Champions'])
reg_n    = len(dff[dff['segment'] == 'Regular'])
risk_n   = len(dff[dff['segment'] == 'At Risk'])
low_n    = len(dff[dff['segment'] == 'Low Value'])

st.markdown(f"""
<div class="kpi-grid" style="grid-template-columns: repeat(5, minmax(0,1fr));">
  <div class="kpi-card kpi-blue">
    <div class="kpi-lbl">Total Customers</div>
    <div class="kpi-val">{total:,}</div>
    <div class="kpi-sub">active in analysis</div>
  </div>
  <div class="kpi-card kpi-purple">
    <div class="kpi-lbl">Champions</div>
    <div class="kpi-val">{champ_n}</div>
    <div class="kpi-sub">{champ_n/total*100:.1f}% of total</div>
  </div>
  <div class="kpi-card kpi-teal">
    <div class="kpi-lbl">Regular</div>
    <div class="kpi-val">{reg_n}</div>
    <div class="kpi-sub">{reg_n/total*100:.1f}% of total</div>
  </div>
  <div class="kpi-card kpi-amber">
    <div class="kpi-lbl">At Risk</div>
    <div class="kpi-val">{risk_n}</div>
    <div class="kpi-sub">{risk_n/total*100:.1f}% of total</div>
  </div>
  <div class="kpi-card kpi-red">
    <div class="kpi-lbl">Low Value</div>
    <div class="kpi-val">{low_n}</div>
    <div class="kpi-sub">{low_n/total*100:.1f}% of total</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Charts row 1 ──────────────────────────────────────────────────────────────
c1, c2 = st.columns(2, gap="small")

with c1:
    st.markdown('<div class="chart-card"><div class="card-title">Segment Composition</div>', unsafe_allow_html=True)
    seg_df = dff['segment'].value_counts().reset_index()
    seg_df.columns = ['Segment', 'Count']

    fig_pie = go.Figure(go.Pie(
        labels=seg_df['Segment'],
        values=seg_df['Count'],
        hole=0.62,
        marker=dict(
            colors=[SEG_COLORS.get(s, '#94a3b8') for s in seg_df['Segment']],
            line=dict(color='#0d1117', width=2),
        ),
        textfont=dict(size=11, family='DM Sans', color='#e2e8f0'),
        textinfo='label+percent',
        textposition='outside',
        insidetextorientation='horizontal',
    ))
    fig_pie.update_layout(
        **PLOT_BASE,
        legend=dict(font=dict(size=11, color=TEXT_C), bgcolor=BG, orientation='v'),
        annotations=[dict(
            text=f'<b>{total}</b>', x=0.5, y=0.5, showarrow=False,
            font=dict(size=22, color='#f1f5f9', family='DM Sans'),
        )],
        height=340,
    )
    fig_pie.update_layout(margin=dict(t=30, b=50, l=20, r=20))
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-card"><div class="card-title">Revenue per Segment · with Benchmark</div>', unsafe_allow_html=True)

    rev_df      = dff.groupby('segment')['monetary'].sum().reset_index().sort_values('monetary')
    avg_rev_seg = rev_df['monetary'].mean()
    top20_rev   = rev_df['monetary'].quantile(0.80)
    x_max       = rev_df['monetary'].max() * 1.3

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=rev_df['monetary'], y=rev_df['segment'], orientation='h',
        marker=dict(
            color=[SEG_COLORS.get(s, '#94a3b8') for s in rev_df['segment']],
            opacity=0.9, line=dict(width=0),
        ),
        text=[f"${v:,.0f}" for v in rev_df['monetary']],
        textposition='outside',
        textfont=dict(size=11, color='#64748b'),
        name='Revenue',
    ))

    n_seg = len(rev_df)
    fig_bar.add_shape(
        type='line', x0=avg_rev_seg, x1=avg_rev_seg,
        y0=-0.5, y1=n_seg - 0.5,
        line=dict(color='#f87171', width=1.5, dash='dot'),
    )
    fig_bar.add_annotation(
        x=avg_rev_seg, y=n_seg - 0.55, text=f"Avg ${avg_rev_seg:,.0f}",
        showarrow=False, font=dict(size=10, color='#f87171', family='DM Sans'),
        yanchor='top', xanchor='left', xshift=6,
    )
    fig_bar.add_shape(
        type='line', x0=top20_rev, x1=top20_rev,
        y0=-0.5, y1=n_seg - 0.5,
        line=dict(color='#fbbf24', width=1.5, dash='dash'),
    )
    fig_bar.add_annotation(
        x=top20_rev, y=n_seg - 0.55, text=f"Top 20% ${top20_rev:,.0f}",
        showarrow=False, font=dict(size=10, color='#fbbf24', family='DM Sans'),
        yanchor='top', xanchor='left', xshift=6,
    )
    fig_bar.update_layout(
        **PLOT_BASE,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, x_max]),
        yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=12, color='#94a3b8')),
        showlegend=False, height=340,
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Descriptive Statistics ────────────────────────────────────────────────────
st.markdown('<div class="section-label">Descriptive Statistics — Recency · Frequency · Monetary</div>', unsafe_allow_html=True)

desc = dff[['recency', 'frequency', 'monetary']].describe().round(2)
desc.index = ['Count', 'Mean', 'Std Dev', 'Min', '25%', '50%', '75%', 'Max']

highlight_rows = {'25%', '50%', '75%'}

rows_html = ""
for idx, row in desc.iterrows():
    row_class = "highlight-row" if idx in highlight_rows else ""
    rows_html += f"""
    <tr class="{row_class}">
        <td>{idx}</td>
        <td>{row['recency']:,.2f}</td>
        <td>{row['frequency']:,.2f}</td>
        <td>${row['monetary']:,.2f}</td>
    </tr>"""

st.markdown(f"""
<div class="chart-card">
  <div class="card-title">Data Distribution Summary</div>
  <table class="desc-table">
    <thead>
      <tr>
        <th></th>
        <th>Recency (days)</th>
        <th>Frequency</th>
        <th>Monetary ($)</th>
      </tr>
    </thead>
    <tbody>{rows_html}</tbody>
  </table>
</div>
""", unsafe_allow_html=True)

# ── Distribution histograms ───────────────────────────────────────────────────
st.markdown('<div class="section-label">Distribution — Recency · Frequency · Monetary</div>', unsafe_allow_html=True)

h1, h2, h3 = st.columns(3, gap="small")

def make_hist(data, color, xlabel, nbins=16):
    fig = go.Figure(go.Histogram(
        x=data, nbinsx=nbins,
        marker=dict(color=color, opacity=0.85, line=dict(color='#0d1117', width=0.5)),
    ))
    fig.update_layout(
        **PLOT_BASE,
        xaxis=dict(
            title=dict(text=xlabel, font=dict(size=10, color=TICK_C)),
            showgrid=False, zeroline=False, tickfont=dict(size=9, color=TICK_C),
        ),
        yaxis=dict(showgrid=True, gridcolor=GRID_C, zeroline=False, tickfont=dict(size=9, color=TICK_C)),
        bargap=0.05, height=200,
    )
    return fig

with h1:
    st.markdown('<div class="chart-card"><div class="card-title">Recency</div>', unsafe_allow_html=True)
    st.plotly_chart(make_hist(dff['recency'],   '#4f8aff', 'Days'),        use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with h2:
    st.markdown('<div class="chart-card"><div class="card-title">Frequency</div>', unsafe_allow_html=True)
    st.plotly_chart(make_hist(dff['frequency'], '#fb923c', 'Rental Count'), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with h3:
    st.markdown('<div class="chart-card"><div class="card-title">Monetary</div>', unsafe_allow_html=True)
    st.plotly_chart(make_hist(dff['monetary'],  '#fbbf24', 'USD'),          use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Insight bar ───────────────────────────────────────────────────────────────
champ_avg    = dff[dff['segment'] == 'Champions']['monetary'].mean() if champ_n > 0 else 0
rev_df_fb    = dff.groupby('segment')['monetary'].sum().reset_index()
avg_rev_fb   = rev_df_fb['monetary'].mean()
top20_rev_fb = rev_df_fb['monetary'].quantile(0.80)

st.markdown(f"""
<div class="insight-bar">
  Out of <b>{total:,} customers</b>, segmentation uses <b>RFM scoring 1–3</b> per dimension based on data distribution percentiles.
  <b>Champions</b> (score 8–9): <b>{champ_n} customers</b> ({champ_n/total*100:.1f}%) with an average spending of <b>${champ_avg:,.2f}</b>.
  <b>Regular</b> (score 6–7): <b>{reg_n} customers</b> ({reg_n/total*100:.1f}%) — moderate performance with growth potential.
  <b>At Risk</b> (score 4–5): <b>{risk_n} customers</b> ({risk_n/total*100:.1f}%) — declining, immediate reactivation needed.
  <b>Low Value</b> (score 3): <b>{low_n} customers</b> ({low_n/total*100:.1f}%) — lowest performance, needs initial engagement.
  &nbsp;·&nbsp;
  <span style="color:#f87171;">·····</span> Avg revenue/segment: <b>${avg_rev_fb:,.0f}</b>
  &nbsp;·&nbsp;
  <span style="color:#fbbf24;">━━</span> Top 20% threshold: <b>${top20_rev_fb:,.0f}</b>
</div>
""", unsafe_allow_html=True)

# ── Customer detail table ─────────────────────────────────────────────────────
st.markdown('<div class="section-label" style="margin-top:0.25rem;">Customer Details</div>', unsafe_allow_html=True)

search = st.text_input("", placeholder="Search by customer name…", label_visibility="collapsed")
display_df = dff.copy()
if search:
    display_df = display_df[display_df['customer_name'].str.contains(search, case=False, na=False)]

st.dataframe(
    display_df.sort_values('monetary', ascending=False)[[
        'customer_name', 'recency', 'frequency', 'monetary', 'rfm_score', 'segment'
    ]].rename(columns={
        'customer_name': 'Name',
        'recency':       'Recency (days)',
        'frequency':     'Frequency',
        'monetary':      'Monetary ($)',
        'rfm_score':     'RFM Score',
        'segment':       'Segment',
    }).reset_index(drop=True),
    use_container_width=True,
    height=320,
)

st.markdown(
    '<div class="footer">RFM Customer Segmentation · Analyst: <b>Najwa Zhafarina Alyani Wilujeng</b> · DVDRental</div>',
    unsafe_allow_html=True,
)
