-- =============================================================================
-- Project: E-Commerce Sales, Pricing & Profitability Analysis
-- Script:  01_schema.sql
-- Purpose: PostgreSQL Database Schema Definition
-- =============================================================================

-- Drop existing tables/views if re-running
DROP VIEW IF EXISTS vw_superstore_analytics;
DROP TABLE IF EXISTS superstore_orders;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS locations;

-- =============================================================================
-- 1. PRIMARY ANALYTICAL TABLE: superstore_orders
-- =============================================================================
-- Complete tabular fact table (all 9,994 line items) optimized for analytical
-- queries, aggregations, window functions, and Microsoft Power BI reporting.
CREATE TABLE superstore_orders (
    row_id                  INTEGER PRIMARY KEY,
    order_id                VARCHAR(30) NOT NULL,
    order_date              DATE NOT NULL,
    ship_date               DATE NOT NULL,
    ship_mode               VARCHAR(50) NOT NULL,
    customer_id             VARCHAR(20) NOT NULL,
    customer_name           VARCHAR(100) NOT NULL,
    segment                 VARCHAR(50) NOT NULL,
    country                 VARCHAR(50) NOT NULL,
    city                    VARCHAR(100) NOT NULL,
    state                   VARCHAR(100) NOT NULL,
    postal_code             VARCHAR(10) NOT NULL,
    region                  VARCHAR(50) NOT NULL,
    product_id              VARCHAR(50) NOT NULL,
    category                VARCHAR(50) NOT NULL,
    sub_category            VARCHAR(50) NOT NULL,
    product_name            VARCHAR(255) NOT NULL,
    sales                   NUMERIC(10, 2) NOT NULL CHECK (sales >= 0),
    quantity                INTEGER NOT NULL CHECK (quantity > 0),
    discount                NUMERIC(4, 2) NOT NULL CHECK (discount >= 0 AND discount <= 1.0),
    profit                  NUMERIC(10, 2) NOT NULL,
    shipping_duration_days  INTEGER NOT NULL CHECK (shipping_duration_days >= 0)
);

-- Performance Indexes for Analytical Queries
CREATE INDEX idx_orders_date      ON superstore_orders(order_date);
CREATE INDEX idx_orders_customer  ON superstore_orders(customer_id);
CREATE INDEX idx_orders_category  ON superstore_orders(category);
CREATE INDEX idx_orders_region    ON superstore_orders(region);
CREATE INDEX idx_orders_segment   ON superstore_orders(segment);

-- =============================================================================
-- 2. NORMALIZED DIMENSION TABLES (Star Schema / Relational Model)
-- =============================================================================

-- Customers Dimension
CREATE TABLE customers (
    customer_id     VARCHAR(20) PRIMARY KEY,
    customer_name   VARCHAR(100) NOT NULL,
    segment         VARCHAR(50) NOT NULL
);

-- Locations Dimension (handles multi-city ZIP codes via composite primary key)
CREATE TABLE locations (
    location_id     SERIAL PRIMARY KEY,
    postal_code     VARCHAR(10) NOT NULL,
    city            VARCHAR(100) NOT NULL,
    state           VARCHAR(100) NOT NULL,
    region          VARCHAR(50) NOT NULL,
    country         VARCHAR(50) NOT NULL,
    CONSTRAINT uq_location UNIQUE (postal_code, city, state)
);

-- Products Dimension
CREATE TABLE products (
    product_key     SERIAL PRIMARY KEY,
    product_id      VARCHAR(50) NOT NULL,
    category        VARCHAR(50) NOT NULL,
    sub_category    VARCHAR(50) NOT NULL,
    product_name    VARCHAR(255) NOT NULL,
    CONSTRAINT uq_product UNIQUE (product_id, product_name)
);
