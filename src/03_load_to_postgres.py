"""
=============================================================================
Project: E-Commerce Sales, Pricing & Profitability Analysis
Script: 03_load_to_postgres.py
Purpose: Connect to local PostgreSQL, create database & schema tables,
         and load cleaned dataset into PostgreSQL with verification.
=============================================================================
"""

import os
import sys
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def main():
    print("=" * 70)
    print("  PHASE 3: POSTGRESQL DATABASE LOADER")
    print("=" * 70)

    # 1. Load connection settings from .env file
    load_dotenv()

    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "ecommerce_analytics")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "")

    if not db_password or db_password == "your_password_here":
        print("\n[ERROR] PostgreSQL password is not set!")
        print("Please create or edit the '.env' file in the project root with:")
        print("  DB_PASSWORD=your_actual_postgres_password")
        sys.exit(1)

    # 2. Check if the target database exists; create it if not
    print(f"\n[INFO] Connecting to PostgreSQL server at {db_host}:{db_port}...")
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database="postgres"  # Connect to default admin db to inspect/create target db
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';")
        exists = cur.fetchone()
        if not exists:
            print(f"[INFO] Database '{db_name}' does not exist. Creating it now...")
            cur.execute(f"CREATE DATABASE {db_name};")
            print(f"  -> Database '{db_name}' created successfully.")
        else:
            print(f"  -> Database '{db_name}' already exists.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"\n[CONNECTION ERROR] Failed to connect to PostgreSQL server: {e}")
        sys.exit(1)

    # 3. Connect to the target database with SQLAlchemy (using URL.create to safely handle special characters in password)
    from sqlalchemy.engine import URL
    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=db_user,
        password=db_password,
        host=db_host,
        port=int(db_port),
        database=db_name
    )
    engine = create_engine(connection_url)

    # 4. Execute sql/01_schema.sql to create tables and indexes
    schema_path = os.path.join("sql", "01_schema.sql")
    print(f"\n[INFO] Applying SQL schema definitions from: {schema_path}")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    with engine.begin() as conn:
        # Split statements on semicolon while ignoring comments
        statements = [stmt.strip() for stmt in schema_sql.split(";") if stmt.strip()]
        for stmt in statements:
            conn.execute(text(stmt))
    print("  -> Schema, tables, and indexes created successfully.")

    # 5. Ingest cleaned CSV data
    cleaned_csv_path = os.path.join("data", "processed", "cleaned_superstore.csv")
    if not os.path.exists(cleaned_csv_path):
        print(f"[ERROR] Cleaned dataset not found at: {cleaned_csv_path}")
        sys.exit(1)

    print(f"\n[INFO] Loading cleaned data from: {cleaned_csv_path}")
    df = pd.read_csv(cleaned_csv_path)

    # Ensure dates are parsed as datetime before loading
    df["order_date"] = pd.to_datetime(df["order_date"]).dt.date
    df["ship_date"] = pd.to_datetime(df["ship_date"]).dt.date

    # 6. Load into superstore_orders (primary analytical table)
    print("\n[INFO] Loading rows into 'superstore_orders' table...")
    df.to_sql(
        name="superstore_orders",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=1000
    )
    print(f"  -> Successfully inserted {len(df):,} rows into 'superstore_orders'.")

    # 7. Populate Dimension Tables
    print("\n[INFO] Populating normalized dimension tables...")

    # A. Customers Dimension
    customers_df = df[["customer_id", "customer_name", "segment"]].drop_duplicates()
    customers_df.to_sql(name="customers", con=engine, if_exists="append", index=False)
    print(f"  -> Inserted {len(customers_df):,} distinct records into 'customers'.")

    # B. Locations Dimension
    locations_df = df[["postal_code", "city", "state", "region", "country"]].drop_duplicates()
    locations_df.to_sql(name="locations", con=engine, if_exists="append", index=False)
    print(f"  -> Inserted {len(locations_df):,} distinct records into 'locations'.")

    # C. Products Dimension
    products_df = df[["product_id", "category", "sub_category", "product_name"]].drop_duplicates()
    products_df.to_sql(name="products", con=engine, if_exists="append", index=False)
    print(f"  -> Inserted {len(products_df):,} distinct records into 'products'.")

    # 8. Verification Audit
    print("\n" + "=" * 70)
    print("                   DATABASE AUDIT REPORT")
    print("=" * 70)
    with engine.connect() as conn:
        for tbl in ["superstore_orders", "customers", "locations", "products"]:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {tbl};")).scalar()
            print(f"  Table: {tbl:<20} | Verified Row Count: {count:,}")
    print("=" * 70)
    print("[SUCCESS] Phase 3 Database Setup & Loading Complete!\n")


if __name__ == "__main__":
    main()
