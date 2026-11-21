-- =============================================================================
-- Project: E-Commerce Sales, Pricing & Profitability Analysis
-- Script:  02_analysis.sql
-- Purpose: 7 Core Business Analytics & Strategic KPI Queries for PostgreSQL 18
-- Database: ecommerce_analytics
-- =============================================================================

-- =============================================================================
-- QUERY 1: EXECUTIVE BUSINESS KPI SUMMARY
-- =============================================================================
-- Business Question: What is the high-level health of the e-commerce business?
-- Concepts Used:
--   - COUNT(DISTINCT ...): Counts unique entities (avoids duplicate counting of multi-item orders).
--   - NULLIF(divisor, 0): Prevents Division by Zero errors gracefully.
--   - ROUND(..., 2): Formats currency and percentages to standard 2-decimal display.
SELECT 
    COUNT(DISTINCT order_id)                                            AS total_orders,
    COUNT(DISTINCT customer_id)                                         AS total_customers,
    COUNT(*)                                                            AS total_line_items,
    ROUND(SUM(sales), 2)                                                AS total_revenue,
    ROUND(SUM(profit), 2)                                               AS total_profit,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100, 2)               AS overall_profit_margin_pct,
    ROUND(SUM(sales) / NULLIF(COUNT(DISTINCT order_id), 0), 2)          AS average_order_value_usd,
    ROUND(AVG(shipping_duration_days), 1)                               AS avg_shipping_days
FROM superstore_orders;


-- =============================================================================
-- QUERY 2: CATEGORY-WISE SALES, PROFITABILITY & REVENUE CONTRIBUTION
-- =============================================================================
-- Business Question: Which categories generate profit vs. which only generate volume?
-- Concepts Used:
--   - GROUP BY: Aggregates numerical facts per distinct product category.
--   - SUM(SUM(sales)) OVER (): SQL Window function calculating total sales across all rows
--     without collapsing the dataset, enabling percentage of total contribution.
SELECT 
    category,
    COUNT(DISTINCT order_id)                                            AS total_orders,
    ROUND(SUM(sales), 2)                                                AS total_sales,
    ROUND((SUM(sales) / SUM(SUM(sales)) OVER ()) * 100, 2)              AS sales_share_pct,
    ROUND(SUM(profit), 2)                                               AS total_profit,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100, 2)               AS profit_margin_pct
FROM superstore_orders
GROUP BY category
ORDER BY total_sales DESC;


-- =============================================================================
-- QUERY 3: TOP 10 MOST PROFITABLE PRODUCTS (STAR PRODUCTS)
-- =============================================================================
-- Business Question: What are our most profitable catalog items?
-- Concepts Used:
--   - ORDER BY total_profit DESC LIMIT 10: Ranks items from highest to lowest earnings.
SELECT 
    product_name,
    category,
    sub_category,
    SUM(quantity)                                                       AS units_sold,
    ROUND(SUM(sales), 2)                                                AS total_sales,
    ROUND(SUM(profit), 2)                                               AS total_profit,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100, 2)               AS profit_margin_pct
FROM superstore_orders
GROUP BY product_name, category, sub_category
ORDER BY total_profit DESC
LIMIT 10;


-- =============================================================================
-- QUERY 4: TOP 10 LOSS-MAKING PRODUCTS (MARGIN DESTROYERS)
-- =============================================================================
-- Business Question: Which products cause the greatest net losses, and why?
-- Concepts Used:
--   - HAVING SUM(profit) < 0: Filters post-aggregated results to only include unprofitable items.
--   - AVG(discount) * 100: Shows if aggressive discounting is connected to net loss.
SELECT 
    product_name,
    category,
    sub_category,
    SUM(quantity)                                                       AS units_sold,
    ROUND(AVG(discount) * 100, 1)                                       AS avg_discount_pct,
    ROUND(SUM(sales), 2)                                                AS total_sales,
    ROUND(SUM(profit), 2)                                               AS total_loss,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100, 2)               AS profit_margin_pct
FROM superstore_orders
GROUP BY product_name, category, sub_category
HAVING SUM(profit) < 0
ORDER BY total_loss ASC
LIMIT 10;


-- =============================================================================
-- QUERY 5: MONTHLY SALES TRENDS & MONTH-OVER-MONTH (MoM) GROWTH
-- =============================================================================
-- Business Question: How do revenue and profit trend over time, and what is the MoM velocity?
-- Concepts Used:
--   - WITH CTE (Common Table Expression): Modularizes intermediate monthly aggregations.
--   - DATE_TRUNC('month', ...): Truncates dates to the first day of each month.
--   - LAG(total_sales) OVER (ORDER BY sales_month): Window function that fetches the preceding
--     month's sales value to calculate percentage growth without self-joins.
WITH monthly_metrics AS (
    SELECT 
        DATE_TRUNC('month', order_date)::DATE                           AS sales_month,
        ROUND(SUM(sales), 2)                                            AS total_sales,
        ROUND(SUM(profit), 2)                                           AS total_profit,
        COUNT(DISTINCT order_id)                                        AS total_orders
    FROM superstore_orders
    GROUP BY DATE_TRUNC('month', order_date)::DATE
)
SELECT 
    TO_CHAR(sales_month, 'YYYY-MM')                                     AS year_month,
    total_sales,
    LAG(total_sales) OVER (ORDER BY sales_month)                        AS prev_month_sales,
    ROUND(
        ((total_sales - LAG(total_sales) OVER (ORDER BY sales_month)) 
        / NULLIF(LAG(total_sales) OVER (ORDER BY sales_month), 0)) * 100, 
        2
    )                                                                   AS mom_sales_growth_pct,
    total_profit,
    ROUND((total_profit / NULLIF(total_sales, 0)) * 100, 2)             AS profit_margin_pct
FROM monthly_metrics
ORDER BY sales_month;


-- =============================================================================
-- QUERY 6: DISCOUNT TIERS VS. PROFITABILITY ELASTICITY
-- =============================================================================
-- Business Question: At what discount percentage does discounting begin eroding net margin?
-- Concepts Used:
--   - CASE WHEN ... THEN ... ELSE ... END: Conditional binning into pricing tiers.
--   - GROUP BY 1: Groups by the first selected expression (discount_tier).
SELECT 
    CASE 
        WHEN discount = 0 THEN '0% (No Discount)'
        WHEN discount > 0 AND discount <= 0.20 THEN '1% - 20% (Low Discount)'
        WHEN discount > 0.20 AND discount <= 0.50 THEN '21% - 50% (Moderate Discount)'
        ELSE '> 50% (Heavy Discount)'
    END                                                                 AS discount_tier,
    COUNT(*)                                                            AS total_line_items,
    ROUND(SUM(sales), 2)                                                AS total_sales,
    ROUND(SUM(profit), 2)                                               AS total_profit,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100, 2)               AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 1)                                       AS avg_discount_pct
FROM superstore_orders
GROUP BY 1
ORDER BY MIN(discount);


-- =============================================================================
-- QUERY 7: REGIONAL BUSINESS PERFORMANCE & FULFILLMENT SPEED
-- =============================================================================
-- Business Question: Which geographic regions yield the strongest margins and delivery speed?
-- Concepts Used:
--   - Aggregate functions across geographic dimensions.
SELECT 
    region,
    COUNT(DISTINCT order_id)                                            AS total_orders,
    COUNT(DISTINCT customer_id)                                         AS unique_customers,
    ROUND(SUM(sales), 2)                                                AS total_sales,
    ROUND(SUM(profit), 2)                                               AS total_profit,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100, 2)               AS profit_margin_pct,
    ROUND(AVG(shipping_duration_days), 1)                               AS avg_shipping_days
FROM superstore_orders
GROUP BY region
ORDER BY total_profit DESC;
