import pandas as pd
import sys
import os

print("HomeSphere pipeline starting...")
print()

# --- Load ---
print("Loading...")
df = pd.read_csv('../HomeSphere/data/sales_raw.csv')
print(f"  {len(df)} rows loaded")
print()

# --- Validate ---
print("Validating...")
errors = []

# Copy checks from this morning, or uncomment one of these to get started:
#
# try:
#     assert df['product_id'].isnull().sum() == 0, "product_id has null values"
# except Exception as e:
#     errors.append(str(e))
#
# try:
#     assert pd.api.types.is_float_dtype(df['unit_price']), "unit_price should be float"
# except Exception as e:
#     errors.append(str(e))


# Option A: fail fast -- pipeline stops, no output written
if errors:
    print(f"  {len(errors)} check(s) failed:")
    for e in errors:
        print(f"    FAIL: {e}")
    print()
    print("Pipeline stopped. Fix the data and run again.")
    sys.exit(1)

# Option B: warn and continue
# Comment out Option A above and uncomment the block below.
#
# if errors:
#     print(f"  {len(errors)} check(s) failed - pipeline continuing with warnings:")
#     for e in errors:
#         print(f"    WARNING: {e}")
#     print()

if not errors:
    print("  All checks passed")
print()

# --- Clean ---
print("Cleaning...")
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
print()

# --- Output ---
print("Writing output...")
os.makedirs('output', exist_ok=True)
df.to_csv('output/silver_sales.csv', index=False)
print(f"  output/silver_sales.csv ({len(df)} rows)")
print()
print("Pipeline complete.")
