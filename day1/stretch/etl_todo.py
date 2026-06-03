"""
HomeSphere ETL — stretch task (Day 1)

Your job: turn the notebook steps into a working Python script.

The script should:
  1. Clean sales_raw.csv
  2. Flatten products_raw.json
  3. Join and calculate revenue
  4. Print a revenue-by-category summary
  5. Save cleaned_sales.csv and sales_joined.csv

Run from the folder that contains the data files:
  python etl_todo.py
"""

import pandas as pd
import json


def clean_sales(path="../data/sales_raw.csv"):
    df = pd.read_csv(path)
    print(f"Loaded sales: {df.shape[0]} rows, {df.shape[1]} columns")

    # TODO: strip the £ sign from unit_price and convert to float

    # TODO: parse order_date — use format='mixed', dayfirst=True, errors='coerce'

    # TODO: convert quantity to numeric (coerce errors), drop rows where it is NaN,
    #       then cast to int

    # TODO: lowercase and strip whitespace from status

    # TODO: drop duplicate rows and print how many were removed

    # TODO: drop rows where product_id is missing and print how many were removed

    # TODO: fill missing region values with 'Unknown'

    # TODO: keep only rows where unit_price > 0 and quantity > 0

    print(f"  Clean sales: {len(df)} rows remaining")
    return df


def flatten_products(path="../data/products_raw.json"):
    with open(path) as f:
        data = json.load(f)

    # TODO: use pd.json_normalize to flatten data['products'] into a DataFrame

    # TODO: rename the dot-notation columns that json_normalize creates:
    #       'specs.rrp'             -> 'rrp'
    #       'specs.warranty_years'  -> 'warranty_years'
    #       'specs.colour'          -> 'colour'
    #       'specs.connectivity'    -> 'connectivity'

    # TODO: keep only the columns you need for the join: product_id, name, category

    print(f"Loaded products: {len(products)} rows")
    return products


def join_and_aggregate(sales, products):
    # TODO: merge sales and products on product_id using a left join

    # TODO: add a line_value column (quantity * unit_price)

    # TODO: group by category, sum line_value, sort descending
    #       round total_revenue to 2 decimal places

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

    print("="*50)


if __name__ == "__main__":
    main()
