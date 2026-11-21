# Power BI Setup & Dashboard Build Guide

This guide walks you through connecting **Microsoft Power BI Desktop** to your live **PostgreSQL 18** database (`ecommerce_analytics`), creating your data model, adding DAX measures, and constructing the interactive executive dashboard.

---

## 1. Connecting Power BI Desktop to PostgreSQL (Import Mode)

Power BI Desktop has been opened on your screen. Follow these simple steps:

1. On the Power BI home ribbon, click **Get Data** (or **Home** > **Get Data** > **More...**).
2. Under the **Database** category, select **PostgreSQL database** and click **Connect**.
3. In the PostgreSQL connection window, enter:
   - **Server:** `127.0.0.1:5433` *(Note the port :5433 for your PostgreSQL 18 instance)*
   - **Database:** `ecommerce_analytics`
   - **Data Connectivity mode:** Select **Import**
   - Click **OK**.
4. If an Encryption prompt appears:
   - Click **OK** or choose **Unencrypted connection** (standard for local loopback connections).
5. In the Credentials window:
   - On the left sidebar, click **Database** (do **not** select Windows credentials).
   - **User name:** `postgres`
   - **Password:** `Manish@071`
   - Click **Connect**.
6. In the **Navigator** window:
   - Select the table: **`superstore_orders`**.
   - *(Optional: Also select `customers`)*.
   - Click **Load**.

Power BI will import all 9,994 rows in seconds.

---

## 2. Actual Data Model & Relationships

### Why `superstore_orders` is the Primary Table:
We inspected the actual database schema in PostgreSQL:
- **`superstore_orders`** already contains all 22 transaction columns: customer names, segments, cities, states, regions, categories, sub-categories, product names, sales, quantities, discounts, and profits.
- Because `superstore_orders` is fully denormalized at the line-item grain, using it as your primary table ensures **zero Cartesian joins** and eliminates duplicate counting.

### Valid Relationship (if importing `customers`):
- If you also import the `customers` table:
  - Drag `customers[customer_id]` to `superstore_orders[customer_id]`.
  - Relationship: **One-to-Many (`1:*`)**, Single cross-filter direction (`customers` filters `superstore_orders`).

---

## 3. Creating the 5 DAX Measures

In Power BI Desktop, click **Modeling** > **New Measure** (or right-click `superstore_orders` in the Data pane and select **New Measure**).

Create each measure below (also available in `dashboard/DAX_Measures.dax`):

```dax
Total Sales = SUM(superstore_orders[sales])
// Format as Currency: $#,##0.00
```

```dax
Total Profit = SUM(superstore_orders[profit])
// Format as Currency: $#,##0.00
```

```dax
Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0)
// Format as Percentage: 0.00%
```

```dax
Total Orders = DISTINCTCOUNT(superstore_orders[order_id])
// Format as Whole Number: #,##0
```

```dax
Average Order Value = DIVIDE([Total Sales], [Total Orders], 0)
// Format as Currency: $#,##0.00
```

### Verification Benchmarks (Must match exactly):
- **Total Sales:** `$2,297,200.65`
- **Total Profit:** `$286,396.54`
- **Profit Margin %:** `12.47%`
- **Total Orders:** `5,009`
- **Average Order Value:** `$458.61`

---

## 4. Building the Dashboard Visuals

On the report canvas, construct the executive layout in 5 sections:

### A. Top Row: Executive KPI Cards (5 Cards)
- Card 1: `[Total Sales]`
- Card 2: `[Total Profit]`
- Card 3: `[Profit Margin %]`
- Card 4: `[Total Orders]`
- Card 5: `[Average Order Value]`

### B. Middle-Left: Monthly Sales & Profit Trend (Line & Clustered Column Chart)
- **X-Axis:** `superstore_orders[order_date]` (Hierarchy: Year and Month)
- **Column Y-Axis:** `[Total Sales]`
- **Line Y-Axis:** `[Total Profit]`

### C. Middle-Right: Category & Sub-Category Performance (Clustered Bar Chart)
- **Y-Axis:** `superstore_orders[category]` (drill-down to `sub_category`)
- **X-Axis:** `[Total Sales]` and `[Total Profit]`

### D. Bottom-Left: Discount vs. Profitability (Column / Scatter Chart)
- **X-Axis:** `superstore_orders[discount]`
- **Y-Axis:** `[Total Profit]`
- *Visual finding:* Shows how profit turns negative as discounts rise above 20%.

### E. Top/Side: Interactive Slicers (3 Slicers)
- Slicer 1: `superstore_orders[order_date]` (Date range slider)
- Slicer 2: `superstore_orders[region]` (Tile or Dropdown: Central, East, South, West)
- Slicer 3: `superstore_orders[segment]` (Consumer, Corporate, Home Office)

---

## 5. Saving the File

1. In Power BI Desktop, click **File** > **Save As**.
2. Save into your project directory at:
   ```text
   dashboard/ecommerce_analytics_dashboard.pbix
   ```
