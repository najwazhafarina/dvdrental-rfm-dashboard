# 🎬 DVDRental Customer Intelligence Dashboard

A multi-page interactive analytics dashboard built with **Streamlit** and **PostgreSQL**, analyzing 16,000+ rental transactions from the DVDRental database across 599 customers and 109 countries.

> 📌 **Group project** — Data Science Mid Exam, President University  
> 👤 **My contribution:** Section 04 — RFM Customer Segmentation (`pages/ENJA.py`)

---

## 📊 Dashboard Sections

| Section | Topic | Analyst |
|---------|-------|---------|
| 01 | Customer Profile & Demographics | Tita |
| 02 | Geographic Analysis | Abel |
| 03 | Rental Activity & History | Abigail |
| **04** | **RFM Customer Segmentation** | **Enja (me)** |

---

## 🎯 My Section — RFM Segmentation

RFM (Recency, Frequency, Monetary) is a behavioral customer segmentation framework. This section:

- **Calculates RFM scores** using quantile-based scoring (Q3 bins) for each customer
- **Classifies customers** into 6 segments based on R/F/M score combinations:

| Segment | Criteria | Strategy |
|---------|----------|----------|
| Champions | R=3, F=3, M=3 | Reward & upsell |
| Loyal | R=3, F≥2 | Loyalty program |
| Potential | R≥2, F≥2 | Nurture to loyal |
| Regular | Others | Standard engagement |
| At Risk | R=1 | Win-back campaign |
| Hibernating | R=1, F=1 | Reactivation offer |

- **Computes Customer Lifetime Value (CLV):** `CLV = monetary × frequency`
- **Visualizes** segment composition (donut chart), revenue by segment (bar chart), and distribution histograms for all 4 RFM metrics
- **Interactive filter** — toggle segments on/off in real time
- **Customer search** — searchable detail table sorted by CLV

---

## 🛠️ Tech Stack

- **Python** — Pandas, Plotly, psycopg2
- **Streamlit** — multi-page app with custom sidebar navigation
- **PostgreSQL** — DVDRental standard database
- **Plotly** — interactive charts (pie, bar, histogram, scatter)

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/najwazhafarina/dvdrental-rfm-dashboard.git
cd dvdrental-rfm-dashboard
```

### 2. Install dependencies
```bash
pip install streamlit psycopg2-binary pandas plotly python-dotenv
```

### 3. Set up PostgreSQL
Make sure you have the [DVDRental database](https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-sample-database/) loaded in PostgreSQL.

### 4. Configure environment variables
Create a `.env` file in the root directory:
```env
DB_HOST=localhost
DB_NAME=dvdrental
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_PORT=5432
```

> ⚠️ **Important:** Never commit your `.env` file. It is already listed in `.gitignore`.

### 5. Update database connection in `pages/ENJA.py`
Replace the hardcoded connection with:
```python
import os
from dotenv import load_dotenv
load_dotenv()

def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
```

### 6. Run the app
```bash
streamlit run home.py
```

---

## 📁 Project Structure

```
dvdrental-rfm-dashboard/
├── home.py              # Landing page & navigation overview
├── sidebar_nav.py       # Shared sidebar component
├── rental_model.pkl     # Pre-trained ML model (Random Forest)
├── .env                 # Local DB credentials (not committed)
├── .gitignore
└── pages/
    ├── ENJA.py          # RFM Segmentation (my contribution)
    ├── TITA.py          # Customer Profile & Demographics
    ├── ABEL.py          # Geographic Analysis
    └── ABIGAIL.py       # Rental Activity & History
```

---

## 📈 Key Insights

- **599 customers** across **109 countries** with **16,044 total rentals**
- RFM segmentation reveals hidden high-value customer clusters (Champions) for targeted marketing
- Hibernating customers identified for immediate reactivation campaigns
- CLV metric enables prioritization of retention budget allocation

---

## 🔗 Related Projects

- [Customer Overdue Risk Prediction](https://github.com/najwazhafarina/overdue-risk-prediction) — Django + ML model predicting rental overdue risk using the same DVDRental dataset
