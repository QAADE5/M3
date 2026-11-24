"""
checks.py -- add your validation checks here.

Use the if pattern in any function:

    if <condition that means failure>:
        errors.append("<message>")

get_failures()         -- raw data: pipeline stops if any of these fail
get_warnings()         -- raw data: pipeline continues but prints a warning
get_silver_failures()  -- cleaned data: pipeline stops before writing the output

Move a check between get_failures() and get_warnings() to change how the pipeline responds.
"""

import pandas as pd


def get_failures(df):
    # The checks from this morning's notebook.
    # Select from the first #if to the last #errors line, then press Ctrl+/ to switch them on.
    errors = []

    #if df['product_id'].isnull().sum() > 0:
    #    errors.append("product_id has null values")

    #if df.duplicated().sum() > 0:
    #    errors.append("duplicate rows found")

    #quantity = pd.to_numeric(df['quantity'], errors='coerce')
    #if not (quantity > 0).all():
    #    errors.append("quantity is not a number, or is zero or less")

    #price = df['unit_price'].astype(str).str.replace('£', '', regex=False).astype(float)
    #if (price <= 0).any():
    #    errors.append("unit_price is zero or less")

    #if df['region'].isnull().sum() > 0:
    #    errors.append("region has null values")

    return errors


def get_warnings(df):
    errors = []

    if not df['status'].str.lower().isin(['complete', 'pending', 'cancelled']).all():
        errors.append("status has unrecognised values")

    return errors


def get_silver_failures(df, raw_rows):
    # Stretch - runs after cleaning.
    # df is the cleaned data, raw_rows is how many rows were loaded.
    errors = []

    # TODO: fail if cleaning dropped more than 25% of raw_rows

    # TODO: fail if any order_date could not be read (NaT)

    # TODO: fail if any status is not complete, pending or cancelled

    return errors
