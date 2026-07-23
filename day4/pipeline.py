import pandas as pd
import sys
import os
import importlib.util

DIR = os.path.dirname(os.path.abspath(__file__))

GREEN = "\033[92m"
RED   = "\033[91m"
AMBER = "\033[93m"
RESET = "\033[0m"


def load_checks():
    spec = importlib.util.spec_from_file_location("checks", os.path.join(DIR, "checks.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    print()
    print("HomeSphere pipeline")
    print("=" * 40)

    # --- Load ---
    print()
    print("LOAD")
    df = pd.read_csv(os.path.join(DIR, "sales_raw.csv"))
    print(f"  {len(df)} rows from sales_raw.csv")

    # --- Validate ---
    print()
    print("VALIDATE")
    checks = load_checks()
    failures = checks.get_failures(df)
    warnings = checks.get_warnings(df)

    for e in warnings:
        print(f"  {AMBER}WARN{RESET}  {e}")
    for e in failures:
        print(f"  {RED}FAIL{RESET}  {e}")

    if not failures and not warnings:
        print(f"  {GREEN}PASS{RESET}  all checks passed")

    if failures:
        print()
        print(f"  {len(failures)} failure(s) -- pipeline stopped.")
        print("  Fix the data or move the check to get_warnings() to continue.")
        print()
        sys.exit(1)

    # --- Clean ---
    print()
    print("CLEAN")
    df['unit_price'] = df['unit_price'].astype(str).str.replace('£', '', regex=False).astype(float)
    df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', dayfirst=True, errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df = df.dropna(subset=['quantity'])
    df['quantity'] = df['quantity'].astype(int)
    df['status'] = df['status'].str.lower().str.strip()
    df = df.drop_duplicates()
    df = df.dropna(subset=['product_id'])
    df['region'] = df['region'].fillna('Unknown')
    df = df[df['unit_price'] > 0]
    df = df[df['quantity'] > 0]
    print(f"  {len(df)} rows after cleaning")

    # --- Output ---
    print()
    print("OUTPUT")
    out = os.path.join(DIR, "silver_sales.csv")
    df.to_csv(out, index=False)
    print(f"  silver_sales.csv ({len(df)} rows)")
    print()
    print("Pipeline complete.")
    print()


if __name__ == "__main__":
    main()
