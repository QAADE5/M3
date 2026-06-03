"""
HomeSphere ETL — stretch task (Day 1)

Runs the full pipeline in a single script:
  1. Clean sales_raw.csv
  2. Flatten products_raw.json
  3. Join and calculate revenue
  4. Print a revenue-by-category summary
  5. Save cleaned_sales.csv and sales_joined.csv

Run from the folder that contains the data files:
  python etl_solution.py
"""

import pandas as pd
import json


def clean_sales(path="../data/sales_raw.csv"):
    df = pd.read_csv(path)
    print(f"Loaded sales: {df.shape[0]} rows, {df.shape[1]} columns")

    df["unit_price"] = df["unit_price"].astype(str).str.replace("£", "", regex=False).astype(float)
    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", dayfirst=True, errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df = df.dropna(subset=["quantity"])
    df["quantity"] = df["quantity"].astype(int)
    df["status"] = df["status"].str.lower().str.strip()

    before = len(df)
    df = df.drop_duplicates()
    print(f"  Removed {before - len(df)} duplicate rows")

    before = len(df)
    df = df.dropna(subset=["product_id"])
    print(f"  Removed {before - len(df)} rows with missing product_id")

    df["region"] = df["region"].fillna("Unknown")

    before = len(df)
    df = df[df["unit_price"] > 0]
    df = df[df["quantity"] > 0]
    print(f"  Removed {before - len(df)} rows with invalid price or quantity")

    print(f"  Clean sales: {len(df)} rows remaining")
    return df


def flatten_products(path="../data/products_raw.json"):
    with open(path) as f:
        data = json.load(f)

    products = pd.json_normalize(data["products"])
    products = products.rename(columns={
        "specs.rrp": "rrp",
        "specs.warranty_years": "warranty_years",
        "specs.colour": "colour",
        "specs.connectivity": "connectivity",
    })
    products = products[["product_id", "name", "category"]]
    print(f"Loaded products: {len(products)} rows")
    return products


def join_and_aggregate(sales, products):
    df = sales.merge(products, on="product_id", how="left")
    df["line_value"] = df["quantity"] * df["unit_price"]

    unmatched = df["category"].isnull().sum()
    if unmatched:
        print(f"  Warning: {unmatched} sales rows did not match a product")

    revenue = (
        df.groupby("category")["line_value"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    revenue.columns = ["category", "total_revenue"]
    revenue["total_revenue"] = revenue["total_revenue"].round(2)
    return df, revenue


def main():
    print("=== HomeSphere ETL ===\n")

    sales = clean_sales()
    sales.to_csv("cleaned_sales.csv", index=False)
    print("  Saved: cleaned_sales.csv\n")

    products = flatten_products()

    joined, revenue = join_and_aggregate(sales, products)
    joined.to_csv("sales_joined.csv", index=False)
    print("  Saved: sales_joined.csv\n")

    total = joined["line_value"].sum()
    print(f"=== Revenue by Category (total £{total:,.2f}) ===")
    for _, row in revenue.iterrows():
        print(f"  {row['category']:<20} £{row['total_revenue']:>8,.2f}")

    print(f"="*50)


if __name__ == "__main__":
    main()
