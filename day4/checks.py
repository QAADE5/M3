"""
checks.py -- add your validation checks here.

Use the if pattern in either function:

    if <condition that means failure>:
        errors.append("<message>")

get_failures()  -- pipeline stops if any of these fail
get_warnings()  -- pipeline continues but prints a warning

Move a check between the two functions to change how the pipeline responds.
"""

import pandas as pd


def get_failures(df):
    errors = []

    #if df['product_id'].isnull().sum() > 0:
    #    errors.append("product_id has null values")

    #if not pd.api.types.is_float_dtype(df['unit_price']):
    #    errors.append("unit_price should be float")

    #if not (pd.to_numeric(df['quantity'], errors='coerce') > 0).all():
    #    errors.append("quantity should be positive")

    return errors


def get_warnings(df):
    errors = []

    if not df['status'].str.lower().isin(['complete', 'refunded', 'pending']).all():
        errors.append("status has unrecognised values")

    return errors
