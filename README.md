# E-Commerce Sales, Pricing & Profitability Analysis

An end-to-end data analytics and business intelligence project tracking sales performance, pricing elasticity, discount impact, and profitability across customer segments and product categories.

---

## 📌 Project Overview & Objectives
In modern retail and e-commerce, maximizing gross revenue is often at odds with protecting net profitability. Aggressive discounting and sub-optimal shipping strategies can erode profit margins despite high sales volumes.

This project investigates and models an e-commerce business using transactional data to answer key strategic questions:
1. **Sales & Profit Dynamics**: Which product categories and sub-categories generate sustainable profit vs. volume at a net loss?
2. **Discount & Pricing Analysis**: At what discount threshold does discounting destroy margin rather than stimulate profitable sales?
3. **Customer Segmentation & Lifetime Value**: How do Consumer, Corporate, and Home Office segments perform across geographical regions?
4. **Fulfillment & Shipping Optimization**: How do shipping modes impact delivery timelines and profitability?
5. **Interactive Executive Reporting**: Deliver an end-to-end interactive dashboard for business leadership.

---

## 🛠️ Technology Stack
- **Python (3.13+)**: Scripting and workflow automation.
- **Pandas**: High-performance data ingestion, cleaning, date manipulation, and tabular transformations.
- **NumPy**: Vectorized numerical calculations and handling numeric anomalies.
- **PostgreSQL 18**: Relational database storage, schema constraints, and data integrity.
- **SQL**: Analytical data modeling, aggregate metrics (MoM growth, AOV, profit margins), and business logic.
- **Microsoft Power BI**: Interactive business intelligence dashboard, data modeling, and DAX measures.

---

## 📁 Repository Structure
```text
E-commerce-Sales-Pricing-Profitability-Analysis/
│
├── data/
│   ├── raw/                # Original, unmodified datasets (excluded from Git)
│   └── processed/          # Cleaned, standardized datasets (excluded from Git)
│
├── src/                    # Python data extraction, cleaning, and ETL scripts
│   ├── 02_clean_data.py    # Data cleaning and standardization pipeline
│   └── 03_load_to_postgres.py # Automated PostgreSQL schema creation & loader
│
├── sql/                    # SQL scripts for database modeling and analysis
│   ├── 01_schema.sql       # Database schema and table constraints (DDL)
│   └── 02_analysis.sql     # 7 Core business KPI queries and analytical views
│
├── power_bi/               # Power BI project files (.pbix) and report assets
│   └── .gitkeep
│
├── .env.example            # Environment variable template for database credentials
├── .gitignore              # Specifies intentionally untracked files
├── requirements.txt        # Python dependency manifest
└── README.md               # Project documentation and guide
```

---

## 📊 Key Business Findings (Verified in PostgreSQL)

| Business Metric | Value | Analytical Finding |
| :--- | :---: | :--- |
| **Total Gross Revenue** | **$2,297,200.65** | 5,009 unique checkout orders across 793 customers. |
| **Total Net Profit** | **$286,396.54** | Overall net profit margin of **12.47%**. |
| **Average Order Value (AOV)** | **$458.61** | Healthy basket size across 9,994 line items. |
| **Average Delivery Time** | **4.0 days** | Consistent fulfillment duration across all four regions. |

### Strategic Insights:
1. **The 20% Discount Cliff:**
   - Orders discounted at **0% - 20%** produce strong positive profit margins (+29.5% and +11.9%).
   - Orders discounted **> 20%** generate steep net losses (-19.7% margin for 21-50% discounts, and -119.2% margin for >50% discounts).
2. **The Furniture Margin Squeeze:**
   - **Technology** generates $836k revenue and **$145.5k profit** (17.4% margin).
   - **Office Supplies** generates $719k revenue and **$122.5k profit** (17.0% margin).
   - **Furniture** generates $742k revenue but only **$18.5k profit** (2.5% margin), dragged down heavily by the **Tables** sub-category.
3. **Regional Profit Disparity:**
   - **West** ($108.4k profit, 14.9% margin) and **East** ($91.5k profit, 13.5% margin) outperform **Central** ($39.7k profit, 7.9% margin).

---

## 📈 Project Roadmap
- [x] **Phase 0 & 1:** Project architecture, environment setup, and raw data inspection.
- [x] **Phase 2:** Data cleaning & standardization pipeline (Pandas & NumPy).
- [x] **Phase 3:** Relational database schema design & loading (PostgreSQL 18).
- [x] **Phase 4:** Advanced SQL business metrics and KPI calculations (`sql/02_analysis.sql`).
- [ ] **Phase 5:** Microsoft Power BI dashboard development.
- [ ] **Phase 6:** Project validation and final documentation.
