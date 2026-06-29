import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import numpy as np
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

# Fungsi untuk koneksi ke database PostgreSQL
def get_data():
    conn = psycopg2.connect(
        host="localhost",
        database="dvdrental",
        user="postgres",       
        password="satuduaakulupa"    
    )
    
    # Ambil data mentah tanpa GROUP BY di SQL agar Python bisa mengolahnya secara dinamis
    query = """
    SELECT 
        p.payment_date,
        co.country, 
        ci.city,
        cu.customer_id,
        cu.first_name || ' ' || cu.last_name as customer_name,
        p.amount,
        p.payment_id
    FROM customer cu
    JOIN payment p ON cu.customer_id = p.customer_id
    JOIN address a ON cu.address_id = a.address_id
    JOIN city ci ON a.city_id = ci.city_id
    JOIN country co ON ci.country_id = co.country_id;
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Judul Dashboard
st.set_page_config(page_title="DVD Rental Analysis", layout="wide")
st.title("🌎 Customer Geographic Dashboard")

try:
    # 1. Ambil data asli dari DB
    df_raw = get_data()

    # Pastikan payment_date dalam format datetime
    df_raw['payment_date'] = pd.to_datetime(df_raw['payment_date'])
    
    # 2. Kalkulasi Metrik Secara Dinamis (Global)
    total_cust = df_raw['customer_id'].nunique()
    total_rev = df_raw['amount'].sum()
    total_trans = df_raw['payment_id'].count()
    total_city = df_raw['city'].nunique()
    total_country = df_raw['country'].nunique()

    # 2. Kalkulasi Metrik Secara Dinamis
    total_cust = df_raw['customer_id'].nunique()
    total_rev = df_raw['amount'].sum()
    total_trans = df_raw['payment_id'].count()
    total_city = df_raw['city'].nunique()
    total_country = df_raw['country'].nunique()
    
    # ... sisa kode kamu ...

    # --- BARIS 1 (4 Kolom Utama) ---
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric(label="Total Customer", value=f"{total_cust:,}")
    with m2:
        st.metric(label="Total Revenue", value=f"${total_rev:,.2f}")
    with m3:
        st.metric(label="Total Transaction", value=f"{total_trans:,}")
    with m4:
        st.metric(label="Total City", value=f"{total_city:,}")
    with m5:
        st.metric(label="Total Country", value=f"{total_country:,}")

    st.markdown("---")
    # --- PERHITUNGAN 4 METRIK RATA-RATA GLOBAL ---
    
    # 1. Level KOTA (City)
    avg_trans_per_city = total_trans / total_city if total_city > 0 else 0
    # Average Spending per City = Total Revenue / Total City
    avg_spending_per_city = total_rev / total_city if total_city > 0 else 0

    # 2. Level NEGARA (Country)
    avg_trans_per_country = total_trans / total_country if total_country > 0 else 0
    # Average Spending per Country = Total Revenue / Total Country
    avg_spending_per_country = total_rev / total_country if total_country > 0 else 0

    # --- TAMPILAN 4 KOLOM ---
    st.write("#### 📊 Average Performance Benchmarks (per Entity)")
    a1, a2, a3, a4 = st.columns(4)

    with a1:
        st.metric(label="Avg Trans per City", value=f"{avg_trans_per_city:.1f}")
        st.caption("Average Transaction for City")

    with a2:
        st.metric(label="Avg Spending per City", value=f"${avg_spending_per_city:,.2f}")
        st.caption("Average Spending for City")

    with a3:
        st.metric(label="Avg Trans per Country", value=f"{avg_trans_per_country:.1f}")
        st.caption("Average Transaction for Country")

    with a4:
        st.metric(label="Avg Spending per Country", value=f"${avg_spending_per_country:,.2f}")
        st.caption("Average Spending for Country")

    st.markdown("---")

    # --- REGION SEGMENTATION (GLOBAL 5 REGION) ---
    region_map = {

        # Asia
        "Afghanistan": "Asia","Bangladesh": "Asia","China": "Asia","India": "Asia",
        "Indonesia": "Asia","Japan": "Asia","Malaysia": "Asia","Pakistan": "Asia",
        "Philippines": "Asia","Singapore": "Asia","South Korea": "Asia",
        "Thailand": "Asia","Vietnam": "Asia","Iran": "Asia","Iraq": "Asia",
        "Israel": "Asia","Saudi Arabia": "Asia","Turkey": "Asia",

        # Europe
        "Austria": "Europe","Belgium": "Europe","Denmark": "Europe","Finland": "Europe",
        "France": "Europe","Germany": "Europe","Greece": "Europe","Ireland": "Europe",
        "Italy": "Europe","Netherlands": "Europe","Norway": "Europe","Poland": "Europe",
        "Portugal": "Europe","Spain": "Europe","Sweden": "Europe","Switzerland": "Europe",
        "United Kingdom": "Europe","Czech Republic": "Europe","Hungary": "Europe",

        # Americas
        "Argentina": "Americas","Brazil": "Americas","Canada": "Americas",
        "Chile": "Americas","Colombia": "Americas","Mexico": "Americas",
        "Peru": "Americas","United States": "Americas","Venezuela": "Americas",

        # Africa
        "Algeria": "Africa","Egypt": "Africa","Ethiopia": "Africa","Ghana": "Africa",
        "Kenya": "Africa","Morocco": "Africa","Nigeria": "Africa",
        "South Africa": "Africa","Tanzania": "Africa",

        # Oceania
        "Australia": "Oceania","New Zealand": "Oceania",
        "Fiji": "Oceania","Papua New Guinea": "Oceania"
    }

    # Tambahkan kolom region ke dataframe
    df_raw["region"] = df_raw["country"].map(region_map)

    # Jika ada negara yang belum masuk mapping
    df_raw["region"] = df_raw["region"].fillna("Other")


    # 3. Siapkan Data untuk Visualisasi (Grouped)
    df_grouped = df_raw.groupby('country').agg({
        'customer_id': 'nunique',   # Total Customer per Country
        'payment_id': 'count',      # Total Transaction per Country
        'amount': 'sum'             # Total Revenue per Country
    }).reset_index().rename(columns={
        'customer_id': 'total_customers', 
        'payment_id': 'total_transactions',
        'amount': 'total_revenue'
    })
    # Menghitung Average Payment (AOV) per Negara
    df_grouped['avg_payment'] = df_grouped['total_revenue'] / df_grouped['total_transactions']

    # Menghitung Average Transaction per Customer per Negara
    df_grouped['avg_trans_per_cust'] = df_grouped['total_transactions'] / df_grouped['total_customers']

    # --- PERSIAPAN DATA UNTUK PERSENTASE ---
    total_cust_all = df_grouped['total_customers'].sum()
    df_grouped['cust_percentage'] = (df_grouped['total_customers'] / total_cust_all) * 100

    # --- VISUALISASI: MAP & BAR CHART DALAM 1 ROW ---
    st.subheader("Geographic & Top Customer Distribution")
    
    # Membagi baris menjadi 2 kolom dengan rasio lebar 2:1 (Map lebih lebar)
    col_map, col_bar = st.columns([2, 1])

    with col_map:
        st.write("**Customer Density by Country**")
        fig_map = px.choropleth(
            df_grouped, 
            locations="country", 
            locationmode="country names",
            color="total_customers", 
            hover_name="country",
            # Menampilkan persentase saat kursor diarahkan ke map (hover)
            hover_data={'total_customers': True, 'cust_percentage': ':.2f'}, 
            color_continuous_scale=px.colors.sequential.YlGnBu
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)

    with col_bar:
        st.write("**Top 10 Countries by Total Customers**")
        top_10_cust = df_grouped.nlargest(10, 'total_customers')
        
        fig_cust = px.bar(
            top_10_cust,
            x='total_customers',
            y='country',
            orientation='h',
            color='total_customers',
            color_continuous_scale='Blues',
            # Menampilkan jumlah asli dan persentase di ujung bar
            text=top_10_cust.apply(lambda r: f"{int(r['total_customers'])} ({r['cust_percentage']:.1f}%)", axis=1)
        )
        fig_cust.update_traces(textposition='outside')
        fig_cust.update_layout(
            yaxis={'categoryorder':'total ascending'}, 
            showlegend=False,
            xaxis_title="Number of Customers",
            margin={"t":0}
        )
        st.plotly_chart(fig_cust, use_container_width=True)

    st.markdown("---")

    
    st.subheader("Top 10 Analysis per Country")
    # Membuat 1 blok dengan 3 kolom berjejer
    col_trans, col_rev = st.columns(2)

    with col_trans:
        st.write("**Country With the Highest Total Transactions**")
        fig_trans = px.bar(
            df_grouped.nlargest(10, 'total_transactions'),
            x='total_transactions',
            y='country',
            orientation='h',
            color='total_transactions',
            color_continuous_scale='Viridis',
            text_auto=True
        )
        fig_trans.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
        st.plotly_chart(fig_trans, use_container_width=True)

    with col_rev:
        st.write("**By Avg Transaction per Customer**")
        st.caption("(Country with > 10 Customers)")
        
        # 1. Hitung metrik rata-rata transaksi per customer
        df_grouped['avg_trans_per_cust'] = df_grouped['total_transactions'] / df_grouped['total_customers']
        
        # 2. FILTER: Hanya ambil negara yang punya customer > 10
        df_filtered_avg = df_grouped[df_grouped['total_customers'] > 10].copy()
        
        # 3. Ambil Top 10 dari hasil filter tersebut
        top_10_avg_trans = df_filtered_avg.nlargest(10, 'avg_trans_per_cust')
        
        # 4. Buat Horizontal Bar Chart
        if not top_10_avg_trans.empty:
            fig_avg_trans = px.bar(
                top_10_avg_trans,
                x='avg_trans_per_cust',
                y='country',
                orientation='h',
                color='avg_trans_per_cust',
                color_continuous_scale='Reds',
                text_auto='.2f',
                labels={'avg_trans_per_cust': 'Avg Trans/Cust'}
            )
            
            fig_avg_trans.update_layout(
                yaxis={'categoryorder':'total ascending'}, 
                showlegend=False,
                xaxis_title="Avg Transactions per Customer",
                margin={"t":0}
            )
            
            st.plotly_chart(fig_avg_trans, use_container_width=True)
        else:
            st.warning("Tidak ada negara dengan jumlah customer > 10 untuk ditampilkan.")


    # --- 1. PERHITUNGAN METRIK & THRESHOLD GLOBAL ---
    # Pastikan kolom rata-rata transaksi sudah ada
    df_grouped['avg_trans_per_cust'] = df_grouped['total_transactions'] / df_grouped['total_customers']

    # Standar Global (Rata-rata populasi)
    avg_customer = df_grouped['total_customers'].mean()
    avg_transaction = df_grouped['total_transactions'].mean()
    avg_avgtransaction = df_grouped['avg_trans_per_cust'].mean()

    # Kolom untuk ukuran visual agar perbedaan loyalty terlihat menonjol
    df_grouped['visual_size'] = df_grouped['avg_trans_per_cust'] ** 3

    # --- 2. LOGIKA SEGMENTASI NEGARA ---

    # A. TOP MARKET: High Customer (> avg) & High Transaction (> avg)
    df_top_market = df_grouped[
        (df_grouped['total_customers'] > avg_customer) & 
        (df_grouped['total_transactions'] > avg_transaction)
    ].copy()

    # B. HIGH VALUE MARKET: Low Volume (< avg) tapi High Loyalty (> avg_avg)
    df_high_value = df_grouped[
        (df_grouped['total_customers'] <= avg_customer) & 
        (df_grouped['total_transactions'] <= avg_transaction) & 
        (df_grouped['avg_trans_per_cust'] > avg_avgtransaction)
    ].copy()

    # C. GROWTH MARKET: Sisanya (Negara yang belum masuk kedua kategori di atas)
    top_high_countries = np.concatenate([df_top_market['country'].unique(), df_high_value['country'].unique()])
    df_growth_market = df_grouped[~df_grouped['country'].isin(top_high_countries)].copy()

    # --- 3. VISUALISASI DENGAN TABS ---
    st.header("Strategic Market Segmentation")
    st.markdown(f"""
    <div style='background-color: #1e1e1e; padding: 10px; border-radius: 5px; border-left: 5px solid #00c0f2;'>
        <b>Global Benchmarks:</b><br>
        Average Customer: {avg_customer:.1f} | 
        Average Transaction: {avg_transaction:.1f} | 
        Global Average Transaction per Customer: {avg_avgtransaction:.2f}
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Top Market", "High Value Market", "Growth Market"])

    def render_segmented_scatter(df, title, color_scale, subtitle):
        if df.empty:
            st.info(f"Belum ada data untuk kategori {title}.")
            return

        st.write(f"### {title}")
        st.caption(subtitle)
        
        # --- LOGIKA UNTUK POSISI TENGAH SEMPURNA ---
        # Kita hitung range sumbu agar 'avg' berada di tengah (Center Padding)
        padding_x = max(df['total_customers'].max() - avg_customer, avg_customer - df['total_customers'].min())
        padding_y = max(df['total_transactions'].max() - avg_transaction, avg_transaction - df['total_transactions'].min())
        
        range_x = [avg_customer - padding_x * 1.1, avg_customer + padding_x * 1.1]
        range_y = [avg_transaction - padding_y * 1.1, avg_transaction + padding_y * 1.1]

        fig = px.scatter(
            df, x="total_customers", y="total_transactions",
            size="visual_size", color="avg_trans_per_cust",
            hover_name="country",
            color_continuous_scale=color_scale,
            template="plotly_dark", 
            height=600,
            # Set range manual agar garis putus-putus terlihat di tengah
            range_x=range_x,
            range_y=range_y,
            labels={
                "total_customers": "Total Customers",
                "total_transactions": "Total Transactions",
                "avg_trans_per_cust": "Avg Trans/Cust"
            },
            hover_data={'visual_size': False, 'avg_trans_per_cust': ':.2f'}
        )
        
        # Tambahkan garis benchmark (Mean)
        fig.add_vline(x=avg_customer, line_dash="dot", line_color="white", opacity=0.5)
        fig.add_hline(y=avg_transaction, line_dash="dot", line_color="white", opacity=0.5)
        
        # Tambahkan kotak warna background (Opsional tapi membantu visualisasi kuadran)
        fig.add_vrect(x0=avg_customer, x1=range_x[1], fillcolor="green", opacity=0.05, line_width=0)
        fig.add_hrect(y0=avg_transaction, y1=range_y[1], fillcolor="green", opacity=0.05, line_width=0)
        
        fig.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color='white')))
        st.plotly_chart(fig, use_container_width=True)

    # Isi masing-masing Tab
    with tab1:
        render_segmented_scatter(
            df_top_market, 
            "Top Market (Priority 1)", 
            "Viridis",
            "Countries with Total Customer and Transaction Above Global Average."
        )
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.info("###  Segmentation Detail")
            st.write(f"""
            - **Number of Countries:** {len(df_top_market)} countries.
            - **Contribution:** These countries represent the largest contributors to overall business transactions.
            - **Condition:** These markets are well-established, supported by a large and stable customer base.
            """)
        with col2:
            st.success("### Strategic Recommendation")
            st.write("""
            - **Customer Retention:** Focus on loyalty programs (such as memberships) to prevent customer churn.
            - **Upselling:** Offer premium film categories or rental bundle packages.
            - **Operational Excellence:** Ensure the availability of popular film inventory is consistently maintained due to high demand volume.
            """)

    with tab2:
        render_segmented_scatter(
            df_high_value, 
            "High Value Market (Niche)", 
            "Magenta",
            "Countries with a small market size but very high customer loyalty (transactions per customer)."
        )
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.info("### Segmentation Detail")
            avg_l_niche = df_high_value['avg_trans_per_cust'].mean()
            st.write(f"""
            - **Customer Quality:** Very high ({avg_l_niche:.2f} transactions per customer).
            - **Efficiency:** Lower acquisition costs due to a small but highly active customer base.
            - **Potential:** A profitable “hidden gem” market.
            """)
        with col2:
            st.success("### Strategic Recommendation")
            st.write("""
            - **Community Engagement:** Build communities or host special events for cinephiles in these countries.
            - **Personalized Marketing:** Use highly personalized film recommendations based on their viewing history.
            - **Referral Program:** Encourage these loyal customers to invite friends or family, as they are the best promoters.
            """)

    with tab3:
        render_segmented_scatter(
            df_growth_market, 
            "Growth Market (Standard/New)", 
            "Blues",
            "Countries that fall below the average volume and require further development strategies."
        )
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.info("### Segmentation Detail")
            st.write(f"""
            - **Challenge:** The number of customers is small and the rental frequency is still low.
            - **Status:** These markets are either new or currently stagnating.
            - **Focus:** Require further market education and awareness efforts.
            """)
        with col2:
            st.success("### Strategic Recommendation")
            st.write("""
            - **Market Penetration:** Offer promotions such as “First Rental Free” or large discounts to attract initial interest.
            - **Content Localization:** Evaluate whether the available film genres match the local preferences in those countries.
            - **Brand Awareness:** Increase marketing investment (advertising) to introduce the service in these regions.
            """)

    st.divider()
    
   # --- PART: DETAIL PER LOCATION ---
    st.markdown("---")
    st.subheader("Deep Dive: Customer Detail by Location")

    # 1. Filter Baris
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_country = st.selectbox("Choose Country:", sorted(df_raw['country'].unique()))
    with col_f2:
        available_cities = sorted(df_raw[df_raw['country'] == selected_country]['city'].unique())
        selected_city = st.selectbox(f"Choose City in {selected_country}:", ["All City"] + available_cities)

    # Filter Data Berdasarkan Pilihan
    if selected_city == "All City":
        loc_data = df_raw[df_raw['country'] == selected_country].copy()
        location_name = selected_country
    else:
        loc_data = df_raw[(df_raw['country'] == selected_country) & (df_raw['city'] == selected_city)].copy()
        location_name = f"{selected_city}, {selected_country}"

    # --- 2. LOGIKA PERHITUNGAN RFM (WAJIB DI ATAS SEBELUM VISUALISASI) ---
    loc_data['payment_date'] = pd.to_datetime(loc_data['payment_date'])
    df_raw['payment_date'] = pd.to_datetime(df_raw['payment_date'])
    last_db_date = df_raw['payment_date'].max()

    customer_detail = loc_data.groupby(['customer_id', 'customer_name']).agg({
        'payment_id': 'count',
        'amount': 'sum',
        'payment_date': 'max'
    }).reset_index()

    customer_detail['Recency'] = (last_db_date - customer_detail['payment_date']).dt.days
    customer_detail = customer_detail.rename(columns={
        'customer_id': 'ID',
        'customer_name': 'Name',
        'payment_id': 'Frequency',
        'amount': 'Monetary'
    })

    # --- 3. TAMPILAN METRIK RINGKASAN ---
    st.write(f"### Summary for {location_name}")
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Total Customer", f"{len(customer_detail):,}")
    m_col2.metric("Total Revenue", f"${customer_detail['Monetary'].sum():,.2f}")
    m_col3.metric("Total Transactions", f"{customer_detail['Frequency'].sum():,}")

    a_col1, a_col2, a_col3 = st.columns(3)
    a_col1.metric("Avg Frequency", f"{customer_detail['Frequency'].mean():.1f}x")
    a_col2.metric("Avg Monetary", f"${customer_detail['Monetary'].mean():,.2f}")
    a_col3.metric("Avg Recency", f"{customer_detail['Recency'].mean():.1f} Days")

    st.markdown("---")

    # --- 1. SIAPKAN DATA PERBANDINGAN ---
    # Data Negara yang dipilih
    country_data = df_grouped[df_grouped['country'] == selected_country].iloc[0]
    
    # Data Benchmark (Rata-rata per Negara yang kita buat tadi)
    # avg_trans_per_country dan avg_spending_per_country diambil dari variabel di atas
    
    comparison_data = pd.DataFrame({
        'Category': ['Total Transactions', 'Total Revenue'],
        'Selected Country': [country_data['total_transactions'], country_data['total_revenue']],
        'Global Average': [avg_trans_per_country, avg_spending_per_country]
    })

    # --- 2. VISUALISASI PERBANDINGAN ---
    st.write(f"### {selected_country} Performance vs Global Average")
    
    # Kita buat 2 grafik bersisian agar skalanya tidak jomplang (karena transaksi puluhan vs revenue ribuan)
    comp_col1, comp_col2 = st.columns(2)

    with comp_col1:
        # Grafik Perbandingan Transaksi
        fig_comp_trans = px.bar(
            comparison_data[comparison_data['Category'] == 'Total Transactions'],
            x='Category',
            y=['Selected Country', 'Global Average'],
            barmode='group',
            title=f"Transaction Volume: {selected_country} vs Avg",
            labels={'value': 'Count', 'variable': 'Legend'},
            color_discrete_map={'Selected Country': '#3366CC', 'Global Average': '#AAAAAA'}
        )
        st.plotly_chart(fig_comp_trans, use_container_width=True)

    with comp_col2:
        # Grafik Perbandingan Revenue
        fig_comp_rev = px.bar(
            comparison_data[comparison_data['Category'] == 'Total Revenue'],
            x='Category',
            y=['Selected Country', 'Global Average'],
            barmode='group',
            title=f"Revenue Value: {selected_country} vs Avg",
            labels={'value': 'Amount ($)', 'variable': 'Legend'},
            color_discrete_map={'Selected Country': '#FF4B4B', 'Global Average': '#AAAAAA'}
        )
        st.plotly_chart(fig_comp_rev, use_container_width=True)

    # --- 3. INSIGHT DINAMIS ---
    diff_rev = country_data['total_revenue'] - avg_spending_per_country
    if diff_rev > 0:
        st.success(f"🔥 **{selected_country}** generates ${diff_rev:,.2f} **higher revenue than the global average.**")
    else:
        st.warning(f"⚠️ **{selected_country}** generates ${abs(diff_rev):,.2f} **less revenue than the global average.**")

    # --- 5. TABEL DETAIL ---
    st.write(f"**Individual Customer Data:**")
    st.dataframe(
        customer_detail[['ID', 'Name', 'Frequency', 'Monetary', 'Recency']].sort_values(by='Monetary', ascending=False),
        use_container_width=True,
        hide_index=True
    )

# Penutup blok Try-Except yang sudah ada di kode kamu
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
    st.info("Pastikan database PostgreSQL kamu menyala dan detail login sudah benar.")
        
        # with col_tab2:
        #     st.write("Data Table (Customer & Transaction)")
        #     # Menampilkan tabel yang bisa di-sort oleh user
        #     st.dataframe(
        #         df_grouped[['country', 'total_customers', 'total_transactions', 'total_revenue']],
        #         use_container_width=True,
        #         hide_index=True 
        #  )
    
# except Exception as e:
#     st.error(f"Gagal koneksi ke database: {e}")
#     st.info("Pastikan database PostgreSQL kamu menyala dan detail login sudah benar.")
