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
- **PostgreSQL**: Relational database storage, schema constraints, and data integrity.
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
├── scripts/                # Python data extraction, cleaning, and ETL scripts
│   └── .gitkeep
│
├── sql/                    # SQL scripts for database modeling and analysis
│   ├── 01_schema.sql       # Database schema and table constraints (DDL)
│   └── 02_analysis.sql     # Business KPI queries and analytical views
│
├── power_bi/               # Power BI project files (.pbix) and report assets
│   └── .gitkeep
│
├── .gitignore              # Specifies intentionally untracked files
├── requirements.txt        # Python dependency manifest
└── README.md               # Project documentation and guide
```

---

## 📊 Dataset Information & Download Instructions
This project uses the standard **Sample Superstore** e-commerce dataset (historical transactional records covering order fulfillment, products, customer segments, sales, discounts, and profits).

- **Source:** [Kaggle Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
- **File Name:** `Sample - Superstore.csv`
- **Rows:** 9,994 line items
- **Columns:** 21 features

### How to set up the dataset locally:
1. Download `Sample - Superstore.csv` from the Kaggle link above.
2. Place the file inside the local directory:
   ```text
   data/raw/Sample - Superstore.csv
   ```
*(Note: As defined in `.gitignore`, raw data files are kept locally and are not committed to GitHub to comply with licensing and repository size best practices).*

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/maniishh/E-commerce-Sales-Pricing-Profitability-Analysis.git
cd E-commerce-Sales-Pricing-Profitability-Analysis
```

### 2. Set up the Python Virtual Environment
On Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 📈 Project Roadmap
- [x] **Phase 0 & 1:** Project architecture, environment setup, and raw data inspection.
- [ ] **Phase 2:** Data cleaning & transformation pipeline (Pandas & NumPy).
- [ ] **Phase 3:** Relational database schema design & loading (PostgreSQL).
- [ ] **Phase 4:** Advanced SQL business metrics and KPI calculations.
- [ ] **Phase 5:** Microsoft Power BI dashboard development.
- [ ] **Phase 6:** Project validation and final documentation.
