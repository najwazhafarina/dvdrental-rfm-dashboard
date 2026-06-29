import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
from sidebar_nav import render_sidebar

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Strategic Customer Intelligence", layout="wide", page_icon="📈")
render_sidebar(active="Profil Pelanggan", analyst="Tita", section="Profil & Demografi")

# --- COLOR PALETTE ---
COLORS = {
    "primary": "#3b82f6",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "navy": "#0f172a",
    "slate": "#1e293b",
    "muted": "#64748b",
    "light": "#94a3b8",
    "border": "#1e293b",
}
PALETTE = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]

# --- 2. CSS DARK MODE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stAppViewContainer"] { background-color: #0f172a !important; }
    [data-testid="stHeader"] { background-color: #0f172a !important; }
    .main .block-container { background-color: #0f172a !important; }

    [data-testid="stSidebar"] { background-color: #0a1120 !important; }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] { background-color: #3b82f6 !important; }
    [data-testid="stSidebar"] [data-baseweb="select"] > div { background-color: #1e293b !important; border-color: #334155 !important; color: #e2e8f0 !important; }
    [data-testid="stSidebar"] [data-baseweb="popover"] { background-color: #1e293b !important; }
    [data-testid="stSidebar"] hr { border-color: #334155 !important; }
    [data-testid="stSidebar"] .stCaption { color: #475569 !important; }
    [data-testid="stSidebarNav"] { background-color: #0a1120 !important; }

    .sidebar-brand { background: linear-gradient(135deg, #1e40af, #3b82f6); border-radius: 10px; padding: 14px 16px; margin-bottom: 20px; }
    .sidebar-brand-title { color: white !important; font-size: 13px; font-weight: 800; letter-spacing: 0.05em; text-transform: uppercase; }
    .sidebar-brand-sub { color: #bfdbfe !important; font-size: 11px; margin-top: 2px; }

    .main-title { color: #f1f5f9; font-size: 36px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 2px; }
    .main-subtitle { color: #94a3b8; font-size: 14px; margin-bottom: 24px; }
    .title-divider { border: none; border-top: 1px solid #1e293b; margin-bottom: 28px; }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1e293b !important;
        border-radius: 14px;
        border: 1px solid #334155 !important;
        padding: 4px 10px;
        box-shadow: 0 1px 8px rgba(0,0,0,0.3);
    }

    .section-header { color: #f1f5f9; font-size: 26px; font-weight: 800; margin-top: 48px; margin-bottom: 2px; padding-top: 8px; border-top: 3px solid #3b82f6; display: inline-block; }
    .section-desc { color: #94a3b8; font-size: 14px; margin-bottom: 16px; margin-top: 6px; }
    .sub-header { color: #cbd5e1; font-size: 15px; font-weight: 700; margin-bottom: 8px; margin-top: 4px; }

    .kpi-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 20px 22px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    border-left-width: 4px;
    border-left-style: solid;
    min-height: 175px;
    height: auto;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-sizing: border-box;
    }
    .kpi-card-blue  { border-left-color: #3b82f6; }
    .kpi-card-green { border-left-color: #10b981; }
    .kpi-card-amber { border-left-color: #f59e0b; }
    .kpi-card-red   { border-left-color: #ef4444; }
    .kpi-label { color: #64748b; font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px; }
    .kpi-value { color: #f1f5f9; font-size: 30px; font-weight: 800; line-height: 1.1; margin-bottom: 6px; }
    .kpi-icon { font-size: 18px; margin-bottom: 10px; }
    .kpi-badge { display: inline-block; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 99px; margin-top: 4px; }
    .kpi-badge-blue  { background: #1e3a5f; color: #60a5fa; }
    .kpi-badge-green { background: #14342a; color: #34d399; }
    .kpi-badge-amber { background: #3a2e0c; color: #fbbf24; }
    .kpi-badge-red   { background: #3b1515; color: #f87171; }

    .chart-card { background: #1e293b; border: 1px solid #334155; border-radius: 14px; padding: 20px 20px 8px 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.25); margin-bottom: 8px; }

    [data-testid="stTextInput"] input { border-radius: 10px !important; border: 1.5px solid #334155 !important; padding: 10px 14px !important; font-size: 14px !important; background: #1e293b !important; color: #e2e8f0 !important; }
    [data-testid="stTextInput"] input:focus { border-color: #3b82f6 !important; box-shadow: 0 0 0 3px rgba(59,130,246,0.2) !important; }
    [data-testid="stTextInput"] input::placeholder { color: #64748b !important; }

    [data-baseweb="select"] > div { background-color: #1e293b !important; border-color: #334155 !important; color: #e2e8f0 !important; }
    [data-baseweb="menu"] { background-color: #1e293b !important; }
    [data-baseweb="option"] { background-color: #1e293b !important; color: #e2e8f0 !important; }
    [data-baseweb="option"]:hover { background-color: #334155 !important; }

    [data-testid="stExpander"] { background-color: #1e293b !important; border: 1px solid #334155 !important; border-radius: 12px !important; }
    [data-testid="stExpander"] summary { color: #e2e8f0 !important; }

    [data-testid="stMetric"] { background-color: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 12px; }
    [data-testid="stMetricLabel"] { color: #94a3b8 !important; }
    [data-testid="stMetricValue"] { color: #f1f5f9 !important; }
    [data-testid="stMetricDelta"] { color: #f87171 !important; }

    [data-testid="stAlert"] { background-color: #1e293b !important; border-color: #334155 !important; color: #e2e8f0 !important; border-radius: 10px !important; }

    .stDownloadButton button { background-color: #3b82f6 !important; color: white !important; border-radius: 10px !important; border: none !important; padding: 0.5rem 1rem !important; font-weight: 600 !important; width: 100% !important; }
    .stDownloadButton button:hover { background-color: #2563eb !important; color: white !important; }
    [data-testid="stSidebar"] .stDownloadButton button { color: white !important; }

    .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #e2e8f0 !important; }
    .stCaption { color: #64748b !important; }
    hr { border-color: #1e293b !important; }

    .footer { margin-top: 60px; padding: 20px 0 10px 0; border-top: 1px solid #1e293b; color: #475569; font-size: 13px; text-align: center; }
    .empty-state { text-align: center; padding: 60px 20px; color: #64748b; font-size: 15px; }
    .empty-state-icon { font-size: 48px; margin-bottom: 12px; }

    .rec-card-green, .rec-card-red, .rec-card-blue {
    padding: 20px;
    border-radius: 12px;
    min-height: 200px;
    height: auto;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    }
    .rec-card-green { background-color: #0d2419; border-left: 5px solid #10b981; }
    .rec-card-red   { background-color: #200d0d; border-left: 5px solid #ef4444; }
    .rec-card-blue  { background-color: #0d1a2e; border-left: 5px solid #3b82f6; }
    .rec-card-green p, .rec-card-red p, .rec-card-blue p {
        font-size: 13px;
        flex: 1;
        margin: 0;
    }
    .leaderboard-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-left: 4px solid #3b82f6;
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    display: flex;
    flex-direction: column;
    gap: 4px;
    height: 210px;
    box-sizing: border-box;
    overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)


# --- 3. DATABASE CONNECTION ---
def get_connection():
    return psycopg2.connect(
        host="localhost", database="dvdrental",
        user="postgres", password="satuduaakulupa", port="5432"
    )

@st.cache_data
def load_data():
    try:
        conn = get_connection()
        query = """
        WITH first_rentals AS (
            SELECT customer_id, MIN(rental_date) AS first_rental_date
            FROM rental
            GROUP BY customer_id
        )
        SELECT
            c.customer_id,
            CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
            c.email,
            ct.city,
            c.create_date AS acquisition_date,
            fr.first_rental_date,
            COUNT(DISTINCT r.rental_id) AS total_rentals,
            COALESCE(SUM(p.amount), 0) AS total_spent,
            MAX(r.rental_date) AS last_rental_date
        FROM customer c
        JOIN address a ON c.address_id = a.address_id
        JOIN city ct ON a.city_id = ct.city_id
        JOIN first_rentals fr ON c.customer_id = fr.customer_id
        LEFT JOIN rental r ON c.customer_id = r.customer_id
        LEFT JOIN payment p ON r.rental_id = p.rental_id
        GROUP BY c.customer_id, ct.city, fr.first_rental_date, c.first_name, c.last_name, c.email, c.create_date
        """
        df = pd.read_sql(query, conn)
        conn.close()
        df['last_rental_date'] = pd.to_datetime(df['last_rental_date'])
        latest = df['last_rental_date'].max()
        df['days_since_last_rental'] = (latest - df['last_rental_date']).dt.days
        return df
    except Exception as e:
        st.error(f"Error Database: {e}")
        return pd.DataFrame()

@st.cache_data
def load_early_spending():
    conn = get_connection()
    query = """
    SELECT
        c.customer_id,
        COALESCE(SUM(CASE
            WHEN r.rental_date <= (
                SELECT MIN(r2.rental_date) + INTERVAL '30 days'
                FROM rental r2
                WHERE r2.customer_id = c.customer_id
            ) THEN p.amount ELSE 0
        END), 0) AS early_spending
    FROM customer c
    LEFT JOIN rental r ON c.customer_id = r.customer_id
    LEFT JOIN payment p ON r.rental_id = p.rental_id
    GROUP BY c.customer_id
    """
    df_early = pd.read_sql(query, conn)
    conn.close()
    return df_early

@st.cache_data
def load_rental_history(customer_ids: tuple):
    conn = get_connection()
    ids_str = ','.join(map(str, customer_ids))
    query = f"""
    SELECT r.customer_id, r.rental_date, r.return_date, c.name AS genre
    FROM rental r
    JOIN inventory i      ON r.inventory_id  = i.inventory_id
    JOIN film_category fc ON i.film_id        = fc.film_id
    JOIN category c       ON fc.category_id   = c.category_id
    WHERE r.customer_id IN ({ids_str})
    ORDER BY r.rental_date
    """
    df_hist = pd.read_sql(query, conn)
    conn.close()
    df_hist['rental_date'] = pd.to_datetime(df_hist['rental_date'])
    return df_hist


def classify_refined_segment(row):
    is_high_revenue = row['total_spent'] > 150
    is_frequent_renter = row['total_rentals'] > 30
    is_active = row['days_since_last_rental'] <= 100
    if is_high_revenue and is_frequent_renter and is_active:
        return 'Champions'
    elif not is_active:
        return 'At Risk'
    else:
        return 'Regular'

def clean_layout():
    return dict(
        plot_bgcolor="#1e293b",
        paper_bgcolor="#1e293b",
        font=dict(family="Plus Jakarta Sans", color="#e2e8f0"),
        xaxis=dict(showgrid=True, gridcolor="#334155", zeroline=False, color="#94a3b8"),
        yaxis=dict(showgrid=True, gridcolor="#334155", zeroline=False, color="#94a3b8"),
        margin=dict(t=10, b=10, l=10, r=10),
        legend=dict(bgcolor="#1e293b", bordercolor="#334155", font=dict(color="#e2e8f0"))
    )

def render_html_table(df_display):
    seg_color = {'Champions': '#10b981', 'At Risk': '#ef4444', 'Regular': '#3b82f6'}
    rows_html = ""
    for _, row in df_display.iterrows():
        sc = seg_color.get(row['segment'], '#3b82f6')
        status_icon = '🟢' if row['days_since_last_rental'] <= 100 else '🔴'
        last_rental = pd.to_datetime(row['last_rental_date']).strftime('%d %b %Y') if pd.notna(row['last_rental_date']) else '-'
        days_color = '#ef4444' if row['days_since_last_rental'] > 200 else '#f59e0b' if row['days_since_last_rental'] > 100 else '#10b981'
        rows_html += f"""
        <tr style="border-bottom: 1px solid #334155;">
            <td style="padding:10px 14px; color:#f1f5f9; font-weight:600;">{row['customer_name']}</td>
            <td style="padding:10px 14px; color:#94a3b8; font-size:12px;">{row['email']}</td>
            <td style="padding:10px 14px; color:#e2e8f0;">{row['city']}</td>
            <td style="padding:10px 14px;">
                <span style="background:{sc}22; color:{sc}; padding:2px 10px; border-radius:99px; font-size:12px; font-weight:600;">
                    {row['segment']}
                </span>
            </td>
            <td style="padding:10px 14px; color:#e2e8f0;">{status_icon} {'Active' if row['days_since_last_rental'] <= 100 else 'Inactive'}</td>
            <td style="padding:10px 14px; color:#60a5fa; font-weight:700;">${row['total_spent']:,.2f}</td>
            <td style="padding:10px 14px; color:#e2e8f0; text-align:center;">{int(row['total_rentals'])}</td>
            <td style="padding:10px 14px; color:#94a3b8; font-size:12px;">{last_rental}</td>
            <td style="padding:10px 14px; color:{days_color}; text-align:center; font-weight:600;">{int(row['days_since_last_rental'])}</td>
        </tr>
        """
    return f"""
    <div style="overflow-x:auto; overflow-y:auto; max-height:420px; border-radius:10px; border:1px solid #334155; background:#1e293b;">
    <table style="width:100%; border-collapse:collapse; font-family:'Plus Jakarta Sans', sans-serif; font-size:13px;">
        <thead style="position:sticky; top:0; z-index:1;">
            <tr style="background:#0f172a; border-bottom:2px solid #334155;">
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase; white-space:nowrap;">Customer Name</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">Email</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">City</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">Segment</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">Status</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">Total Spent</th>
                <th style="padding:12px 14px; text-align:center; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">Rentals</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase; white-space:nowrap;">Last Rental</th>
                <th style="padding:12px 14px; text-align:center; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase; white-space:nowrap;">Days Since</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    </div>
    """
    return f"""
    <div style="overflow-x:auto; overflow-y:auto; max-height:420px; border-radius:10px; border:1px solid #334155; background:#1e293b;">
    <table style="width:100%; border-collapse:collapse; font-family:'Plus Jakarta Sans', sans-serif; font-size:13px;">
        <thead style="position:sticky; top:0; z-index:1;">
            <tr style="background:#0f172a; border-bottom:2px solid #334155;">
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase; white-space:nowrap;">Customer Name</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">Email</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">City</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">Segment</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">Status</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">Total Spent</th>
                <th style="padding:12px 14px; text-align:center; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">Rentals</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase; white-space:nowrap;">Last Rental</th>
                <th style="padding:12px 14px; text-align:center; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase; white-space:nowrap;">Days Since</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    </div>
    """


# --- 4. LOAD & SEGMENT ---
df = load_data()
df['segment'] = df.apply(classify_refined_segment, axis=1)

if not df.empty:

    # --- SIDEBAR ---
    st.sidebar.markdown("### **Filter Data**")
    city_filter = st.sidebar.multiselect(
        "Select Locations:",
        options=sorted(df["city"].unique()),
        default=sorted(df["city"].unique())[:5]
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📥 Export Data")

    @st.cache_data
    def convert_df(df_to_download):
        return df_to_download.to_csv(index=False).encode('utf-8')

    df_preview = df[df["city"].isin(city_filter)].copy() if city_filter else df.copy()
    csv_data = convert_df(df_preview)
    st.sidebar.download_button(
        label="Download Filtered Data as CSV",
        data=csv_data,
        file_name='strategic_customer_data.csv',
        mime='text/csv',
    )

    # --- MAIN TITLE ---
    st.markdown("""
    <div class="main-title">Strategic Customer Intelligence</div>
    <div class="main-subtitle">Comprehensive analysis of DVD Rental customer performance and behavioral insights.</div>
    <hr class="title-divider"/>
    """, unsafe_allow_html=True)

    # --- EMPTY STATE GUARD ---
    if not city_filter:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🗺️</div>
            <strong>No cities selected.</strong><br>
            Please select at least one location from the sidebar to display data.
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # --- SINGLE SOURCE OF TRUTH ---
    df_f = df[df["city"].isin(city_filter)].copy()

    # --- KPI CALCULATIONS ---
    t_cust = len(df_f)
    customer_equity = df_f['total_spent'].sum()

    # KPI 1 — Customer Base Health
    df_f['tenure_months'] = (
        pd.to_datetime(df_f['last_rental_date']) -
        pd.to_datetime(df_f['first_rental_date'])
    ).dt.days / 30
    df_f['rental_rate'] = df_f['total_rentals'] / df_f['tenure_months'].replace(0, 1)
    avg_rental_rate = df_f['rental_rate'].mean() if t_cust > 0 else 0
    active_count = len(df_f[df_f['days_since_last_rental'] <= 100])
    active_rate = (active_count / t_cust * 100) if t_cust > 0 else 0

    # KPI 2 — Customer Equity + Spending Growth
    df_early = load_early_spending()
    df_f = df_f.merge(df_early, on='customer_id', how='left')
    avg_early_spending = df_f['early_spending'].mean() if t_cust > 0 else 0
    avg_lifetime_spending = df_f['total_spent'].mean() if t_cust > 0 else 0
    spending_growth_pct = (
        ((avg_lifetime_spending - avg_early_spending) / avg_early_spending) * 100
        if avg_early_spending > 0 else 0
    )
    growth_badge = "kpi-badge-green" if spending_growth_pct > 50 else "kpi-badge-amber"
    growth_label = f"📈 +{spending_growth_pct:.1f}% lifetime growth" if spending_growth_pct > 0 else f"📉 {spending_growth_pct:.1f}% lifetime growth"

    # KPI 3 — Avg Profile Value
    avg_profile_value = df_f['total_spent'].mean() if t_cust > 0 else 0
    median_profile_value = df_f['total_spent'].median() if t_cust > 0 else 0
    skew_gap = avg_profile_value - median_profile_value

    # KPI 4 — Risk Exposure
    at_risk_customers = df_f[df_f['segment'] == 'At Risk']
    risk_count = len(at_risk_customers)
    risk_pct = (risk_count / t_cust * 100) if t_cust > 0 else 0
    risk_exposure = at_risk_customers['total_spent'].sum()
    avg_days_at_risk = at_risk_customers['days_since_last_rental'].mean() if risk_count > 0 else 0
    if avg_days_at_risk <= 130:
        urgency_label, urgency_badge = "🟡 Recoverable", "kpi-badge-amber"
    elif avg_days_at_risk <= 200:
        urgency_label, urgency_badge = "🔴 High Urgency", "kpi-badge-red"
    else:
        urgency_label, urgency_badge = "💀 Near Lost", "kpi-badge-red"

    # --- KPI CARDS ---
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="kpi-card kpi-card-blue">
            <div class="kpi-icon">👥</div>
            <div class="kpi-label">Customer Base Health</div>
            <div class="kpi-value">{t_cust:,}</div>
            <div style="display:flex; gap:6px; flex-wrap:wrap; margin-top:6px;">
                <span class="kpi-badge kpi-badge-blue">🟢 {active_rate:.1f}% Active Base</span>
                <span class="kpi-badge kpi-badge-blue">⌀ {avg_rental_rate:.1f}x / month</span>
            </div>
        </div>""", unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi-card kpi-card-green">
            <div class="kpi-icon">💎</div>
            <div class="kpi-label">Customer Equity</div>
            <div class="kpi-value">${customer_equity:,.0f}</div>
            <div style="display:flex; gap:6px; flex-wrap:wrap; margin-top:6px;">
                <span class="kpi-badge kpi-badge-green">⌀ Early ${avg_early_spending:.2f} → Lifetime ${avg_lifetime_spending:.2f}</span>
                <span class="kpi-badge {growth_badge}">{growth_label}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-card kpi-card-amber">
            <div class="kpi-icon">📈</div>
            <div class="kpi-label">Avg Profile Value</div>
            <div class="kpi-value">${avg_profile_value:.2f}</div>
            <div style="display:flex; gap:6px; flex-wrap:wrap; margin-top:6px;">
                <span class="kpi-badge kpi-badge-amber">Median ${median_profile_value:.2f}</span>
                <span class="kpi-badge kpi-badge-amber">{'⚠️ Outlier-driven' if skew_gap > 20 else '✅ Healthy spread'}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-card kpi-card-red">
            <div class="kpi-icon">🚨</div>
            <div class="kpi-label">Risk Exposure</div>
            <div class="kpi-value">${risk_exposure:,.0f}</div>
            <div style="display:flex; gap:6px; flex-wrap:wrap; margin-top:6px;">
                <span class="kpi-badge kpi-badge-red">{risk_pct:.1f}% Population at Risk</span>
                <span class="kpi-badge kpi-badge-red">⌀ {avg_days_at_risk:.0f} days gone</span>
                <span class="kpi-badge {urgency_badge}">{urgency_label}</span>
            </div>
        </div>""", unsafe_allow_html=True)


    # --- SPENDING DISTRIBUTION ---
    st.markdown('<h2 class="section-header">💰 Spending Distribution</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Understanding how spending is spread across the customer base.</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        fig_hist = px.histogram(
            df_f, x='total_spent', nbins=40,
            color_discrete_sequence=[COLORS["primary"]],
            labels={'total_spent': 'Total Spending ($)', 'count': 'Number of Customers'}
        )
        mean_val = df_f['total_spent'].mean()
        median_val = df_f['total_spent'].median()
        fig_hist.add_vline(
            x=mean_val, line_dash="dash", line_color=COLORS["warning"],
            annotation_text=f"Mean ${mean_val:.0f}", annotation_position="top right",
            annotation_font_color=COLORS["warning"]
        )
        fig_hist.add_vline(
            x=median_val, line_dash="dot", line_color=COLORS["success"],
            annotation_text=f"Median ${median_val:.0f}", annotation_position="top left",
            annotation_font_color=COLORS["success"]
        )
        fig_hist.update_layout(**clean_layout(), bargap=0.05, yaxis_title="Number of Customers")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Overall Spending Distribution</p>', unsafe_allow_html=True)
        st.caption("Dashed = Mean, Dotted = Median.")
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        fig_seg = px.histogram(
            df_f, x='total_spent', color='segment', nbins=40, barmode='overlay', opacity=0.7,
            color_discrete_map={
                'Champions': COLORS["success"],
                'At Risk':   COLORS["danger"],
                'Regular':   COLORS["primary"]
            },
            labels={'total_spent': 'Total Spending ($)', 'count': 'Number of Customers'}
        )
        layout = clean_layout()
        layout['legend'] = dict(
            orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5,
            font=dict(color="#e2e8f0"), bgcolor="#1e293b"
        )
        fig_seg.update_layout(**layout, bargap=0.05, yaxis_title="Number of Customers")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Spending Distribution by Segment</p>', unsafe_allow_html=True)
        st.caption("Overlay shows where each segment sits on the spending spectrum.")
        st.plotly_chart(fig_seg, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    skew_gap_display = mean_val - median_val
    if skew_gap_display > 20:
        st.warning(f"⚠️ Mean is **${skew_gap_display:.0f} higher** than Median — spending is right-skewed, driven by a small group of high spenders.")
    else:
        st.success(f"✅ Mean and Median are close (gap: ${skew_gap_display:.0f}) — spending is relatively evenly spread.")


    # --- OPERATIONAL INSIGHT ---
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('## ⚙️ Operational Insight')
    st.markdown('Use this section for actionable insights to rescue at-risk customers.')

    at_risk_customers = df_f[df_f['segment'] == 'At Risk']

    if not at_risk_customers.empty:
        at_risk_whales = at_risk_customers.nlargest(5, 'total_spent')
        st.error("🚨 **TODAY'S TOP PRIORITY: High-Value Customers on the Brink of Leaving!**")
        cols = st.columns(len(at_risk_whales))
        for i, (idx, row) in enumerate(at_risk_whales.iterrows()):
            with cols[i]:
                st.metric(
                    label=row['customer_name'],
                    value=f"${row['total_spent']:.0f}",
                    delta="AT RISK",
                    delta_color="inverse"
                )
                st.caption(f"Last rental: {row['days_since_last_rental']} days ago")
    else:
        st.success("✅ No high-value customers are currently in the 'At Risk' category.")


    # --- CUSTOMER DIRECTORY ---
    st.markdown('<h2 class="section-header">🗂️ Customer Directory</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Search, rank, and drill down into individual customer profiles.</p>', unsafe_allow_html=True)


    # ── FULL CUSTOMER TABLE ───────────────────────────────────
    st.markdown('<p class="sub-header">📋 Full Customer Directory</p>', unsafe_allow_html=True)

    col_search, col_seg, col_sort = st.columns([2, 1.5, 1.5])
    with col_search:
        search_query = st.text_input("🔍 Search by Name or Email:", placeholder="e.g. John, john@email.com ...", key="cust_search")
    with col_seg:
        seg_options = sorted(df_f['segment'].unique().tolist())
        selected_seg = st.multiselect("Filter Segment:", options=seg_options, default=seg_options, key="cust_seg")
    with col_sort:
        sort_by = st.selectbox("Sort By:", options=["Total Spent ↓", "Total Rentals ↓", "Days Since Last Rental ↑", "Name A–Z"], key="cust_sort")

    display_df = df_f[df_f['segment'].isin(selected_seg)].copy()
    if search_query:
        mask = (
            display_df['customer_name'].str.contains(search_query, case=False, na=False) |
            display_df['email'].str.contains(search_query, case=False, na=False)
        )
        display_df = display_df[mask]

    sort_map = {
        "Total Spent ↓":            ('total_spent', False),
        "Total Rentals ↓":          ('total_rentals', False),
        "Days Since Last Rental ↑": ('days_since_last_rental', True),
        "Name A–Z":                 ('customer_name', True),
    }
    sort_col, sort_asc = sort_map[sort_by]
    display_df = display_df.sort_values(sort_col, ascending=sort_asc)

    st.caption(f"Showing **{len(display_df)}** customers")
    st.html(render_html_table(display_df))

    # Download section
    st.markdown("#### 📥 Download List")
    dl_col1, dl_col2 = st.columns([2, 1])
    with dl_col1:
        seg_dl = st.selectbox(
            "Select segment to download:",
            options=['All'] + seg_options,
            key="dl_seg"
        )
    with dl_col2:
        dl_df = display_df if seg_dl == 'All' else display_df[display_df['segment'] == seg_dl]
        st.download_button(
            label=f"⬇️ Download {seg_dl}",
            data=dl_df.to_csv(index=False).encode('utf-8'),
            file_name=f'customers_{seg_dl.lower().replace(" ", "_")}.csv',
            mime='text/csv',
            use_container_width=True,
        )

    st.markdown('<br>', unsafe_allow_html=True)

    # ── CUSTOMER DRILL DOWN ───────────────────────────────────
    st.markdown('<p class="sub-header">🔎 Customer Drill Down</p>', unsafe_allow_html=True)
    st.caption("Select a customer to see their full profile, rental timeline, and genre preferences.")

    customer_options = (
        df_f.sort_values('customer_name')
        .apply(lambda r: f"{r['customer_name']} — {r['city']}", axis=1)
        .tolist()
    )
    selected_label = st.selectbox(
        "Choose Customer:",
        options=["(Select a customer)"] + customer_options,
        key="drill_select"
    )

    if selected_label != "(Select a customer)":
        sel_name, sel_city = selected_label.split(" — ", 1)
        cust_row = df_f[
            (df_f['customer_name'] == sel_name) &
            (df_f['city'] == sel_city)
        ].iloc[0]

        cid = int(cust_row['customer_id'])
        df_hist = load_rental_history((cid,))

        seg_color_map = {'Champions': '#10b981', 'At Risk': '#ef4444', 'Regular': '#3b82f6'}
        seg_color = seg_color_map.get(cust_row['segment'], '#3b82f6')
        status_label = '🟢 Active' if cust_row['days_since_last_rental'] <= 100 else '🔴 Inactive'

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid #334155;
                    border-left: 5px solid {seg_color}; border-radius: 14px; padding: 24px 28px; margin: 12px 0 20px 0;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
                <div>
                    <div style="color:#94a3b8; font-size:11px; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">Customer Profile</div>
                    <div style="color:#f1f5f9; font-size:26px; font-weight:800; margin-bottom:4px;">{cust_row['customer_name']}</div>
                    <div style="color:#64748b; font-size:13px;">{cust_row['email']}</div>
                    <div style="color:#64748b; font-size:13px; margin-top:2px;">📍 {cust_row['city']}</div>
                </div>
                <div style="display:flex; flex-direction:column; gap:8px; align-items:flex-end;">
                    <span style="background:{seg_color}22; color:{seg_color}; padding:4px 14px; border-radius:99px; font-weight:700; font-size:13px;">{cust_row['segment']}</span>
                    <span style="background:#1e293b; color:#94a3b8; padding:4px 14px; border-radius:99px; font-size:12px; border:1px solid #334155;">{status_label}</span>
                </div>
            </div>
            <hr style="border-color:#334155; margin:16px 0;">
            <div style="display:flex; gap:32px; flex-wrap:wrap;">
                <div>
                    <div style="color:#64748b; font-size:11px; text-transform:uppercase; letter-spacing:0.06em;">Lifetime Spending</div>
                    <div style="color:#f1f5f9; font-size:22px; font-weight:800;">${cust_row['total_spent']:,.2f}</div>
                </div>
                <div>
                    <div style="color:#64748b; font-size:11px; text-transform:uppercase; letter-spacing:0.06em;">Total Rentals</div>
                    <div style="color:#f1f5f9; font-size:22px; font-weight:800;">{int(cust_row['total_rentals'])}</div>
                </div>
                <div>
                    <div style="color:#64748b; font-size:11px; text-transform:uppercase; letter-spacing:0.06em;">Avg per Rental</div>
                    <div style="color:#f1f5f9; font-size:22px; font-weight:800;">${cust_row['total_spent']/max(cust_row['total_rentals'],1):.2f}</div>
                </div>
                <div>
                    <div style="color:#64748b; font-size:11px; text-transform:uppercase; letter-spacing:0.06em;">Last Rental</div>
                    <div style="color:#f1f5f9; font-size:22px; font-weight:800;">{int(cust_row['days_since_last_rental'])} days ago</div>
                </div>
                <div>
                    <div style="color:#64748b; font-size:11px; text-transform:uppercase; letter-spacing:0.06em;">Member Since</div>
                    <div style="color:#f1f5f9; font-size:22px; font-weight:800;">{pd.to_datetime(cust_row['acquisition_date']).strftime('%b %Y')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        ch1, ch2 = st.columns([3, 2])

        with ch1:
            if not df_hist.empty:
                df_timeline = (
                    df_hist.set_index('rental_date').resample('ME').size()
                    .reset_index(name='rentals')
                )
                df_timeline['rental_date'] = df_timeline['rental_date'].dt.strftime('%b %Y')
                fig_tl = px.bar(
                    df_timeline, x='rental_date', y='rentals',
                    color_discrete_sequence=[seg_color],
                    labels={'rental_date': 'Month', 'rentals': 'Rentals'}
                )
                fig_tl.update_layout(**clean_layout(), xaxis_tickangle=-30)
                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                st.markdown('<p class="sub-header">📅 Monthly Rental Activity</p>', unsafe_allow_html=True)
                st.caption("How often does this customer rent over time?")
                st.plotly_chart(fig_tl, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No rental history found for this customer.")

        with ch2:
            if not df_hist.empty:
                genre_counts = (
                    df_hist.groupby('genre').size()
                    .reset_index(name='count').sort_values('count', ascending=False)
                )
                fig_genre = px.pie(
                    genre_counts, names='genre', values='count', hole=0.55,
                    color_discrete_sequence=PALETTE
                )
                layout = clean_layout()
                layout['legend'] = dict(orientation="v", font=dict(size=11, color="#e2e8f0"), bgcolor="#1e293b")
                layout['margin'] = dict(t=10, b=30, l=10, r=10)
                fig_genre.update_layout(**layout)
                fig_genre.update_traces(
                    textinfo='percent',
                    hovertemplate='<b>%{label}</b><br>%{value} rentals<extra></extra>'
                )
                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                st.markdown('<p class="sub-header">🎬 Favourite Genres</p>', unsafe_allow_html=True)
                st.caption("Genre distribution based on all rentals.")
                st.plotly_chart(fig_genre, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)


    # --- STRATEGIC RECOMMENDATIONS (DINAMIS) ---
    st.markdown('<h2 class="section-header">💡 Strategic Action Plan</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Automated data-backed recommendations based on current customer conditions.</p>', unsafe_allow_html=True)

    champions_count = len(df_f[df_f['segment'] == 'Champions'])
    champions_pct = (champions_count / t_cust * 100) if t_cust > 0 else 0
    potential_loss = df_f[df_f['segment'] == 'At Risk']['total_spent'].sum()

    # --- Champions Strategy (dinamis) ---
    if champions_count == 0:
        champ_title = "💎 Build Your Champions"
        champ_body = """
            No Champions detected in the current filter. Focus on converting top Regular customers —
            those with high rental frequency but spending just below the threshold —
            through exclusive early-access promos to push them over the line.
        """
    elif champions_pct < 10:
        champ_title = "💎 Protect Your Champions"
        champ_body = f"""
            Only <b>{champions_count} Champions ({champions_pct:.1f}%)</b> detected — a thin base.
            Prioritize retention: offer VIP early access to new titles and a dedicated loyalty tier
            to prevent any defection from this critical group.
        """
    else:
        champ_title = "💎 Champions Strategy"
        champ_body = f"""
            <b>{champions_count} Champions ({champions_pct:.1f}% of base)</b> are driving your top-line revenue.
            Reward them with 2x Loyalty Points and exclusive perks to sustain their engagement
            and deepen lifetime value.
        """

    # --- Win-back Strategy (dinamis) ---
    if risk_count == 0:
        risk_title = "✅ No Active Risk Detected"
        risk_body = "All customers in this filter are currently active. Keep monitoring recency — set an alert if any customer exceeds 90 days without a rental."
        risk_card = "rec-card-blue"
    elif urgency_label == "🟡 Recoverable":
        risk_title = "⚠️ Win-back Window Open"
        risk_body = f"""
            <b>${potential_loss:,.0f}</b> at risk across <b>{risk_count} customers</b> —
            but avg inactivity is only <b>{avg_days_at_risk:.0f} days</b>, still within recovery range.
            Send a personalized 'We Miss You' promo with 20% off within the next 2 weeks.
        """
        risk_card = "rec-card-red"
    elif urgency_label == "🔴 High Urgency":
        risk_title = "🔴 High Urgency: Act Now"
        risk_body = f"""
            <b>${potential_loss:,.0f}</b> exposure across <b>{risk_count} customers</b> averaging
            <b>{avg_days_at_risk:.0f} days</b> inactive. Standard promos may not be enough —
            escalate to a direct outreach campaign with a time-limited 30% discount offer.
        """
        risk_card = "rec-card-red"
    else:
        risk_title = "💀 Near-Lost: Last Resort"
        risk_body = f"""
            <b>{risk_count} customers</b> averaging <b>{avg_days_at_risk:.0f} days</b> without activity —
            recovery probability is low. Deploy a high-value 'Come Back' bundle (free rental + 40% off)
            targeting only the top spenders among this group to maximize ROI on win-back spend.
        """
        risk_card = "rec-card-red"

    # --- Upselling Strategy (dinamis) ---
    if avg_rental_rate < 1.5:
        up_title = "🚀 Activation Needed"
        up_body = f"""
            Avg rental rate is only <b>{avg_rental_rate:.1f}x/month</b> — customers are barely engaging.
            Introduce a low-barrier 'First Bundle' promo: Rent 3 for the price of 2,
            to create a habit loop before pushing higher-tier upsells.
        """
    elif avg_rental_rate < 3.0:
        up_title = "🚀 Upselling Strategy"
        up_body = f"""
            Rental rate sits at <b>{avg_rental_rate:.1f}x/month</b> — moderate engagement with room to grow.
            Offer a 'Rent 5 Movies for Less' bundle targeting Regular customers
            to push frequency closer to Champions territory.
        """
    else:
        up_title = "🚀 Maximize High-Frequency Customers"
        up_body = f"""
            Strong avg rental rate of <b>{avg_rental_rate:.1f}x/month</b>.
            Shift focus to increasing <i>spend per rental</i> — promote premium or new-release titles
            with a small surcharge to grow revenue without needing more visits.
        """

    rec1, rec2, rec3 = st.columns(3)

    with rec1:
        st.markdown(f"""
        <div class="rec-card-green">
            <h4 style="color: #34d399; margin-top:0;">{champ_title}</h4>
            <p style="color: #a7f3d0; font-size: 14px;">{champ_body}</p>
        </div>""", unsafe_allow_html=True)

    with rec2:
        st.markdown(f"""
        <div class="{risk_card}">
            <h4 style="color: #f87171; margin-top:0;">{risk_title}</h4>
            <p style="color: #fecaca; font-size: 14px;">{risk_body}</p>
        </div>""", unsafe_allow_html=True)

    with rec3:
        st.markdown(f"""
        <div class="rec-card-blue">
            <h4 style="color: #60a5fa; margin-top:0;">{up_title}</h4>
            <p style="color: #bfdbfe; font-size: 14px;">{up_body}</p>
        </div>""", unsafe_allow_html=True)


# --- FOOTER ---
st.markdown("""
    <div class="footer">
        Strategic Customer Intelligence Dashboard &nbsp;·&nbsp; Analyst: <strong>Puspita Tri Rahayu</strong>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("Analyst: Puspita Tri Rahayu")
