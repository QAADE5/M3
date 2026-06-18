"""
checks.py -- add your validation checks here.

Use the try/except pattern in either function:

    try:
        assert <condition>, "<message if it fails>"
    except Exception as e:
        errors.append(str(e))

get_failures()  -- pipeline stops if any of these fail
get_warnings()  -- pipeline continues but prints a warning

Move a check between the two functions to change how the pipeline responds.
"""

import pandas as pd


def get_failures(df):
    errors = []

    #try:
    #    assert df['product_id'].isnull().sum() == 0, "product_id has null values"
    #except Exception as e:
    #    errors.append(str(e))

    #try:
    #    assert pd.api.types.is_float_dtype(df['unit_price']), "unit_price should be float"
    #except Exception as e:
    #    errors.append(str(e))

    #try:
    #    assert (df['quantity'] > 0).all(), "quantity should be positive"
    #except Exception as e:
    #    errors.append(str(e))

    return errors


def get_warnings(df):
    errors = []

    try:
        assert df['status'].str.lower().isin(['complete', 'refunded', 'pending']).all(), \
            "status has unrecognised values"
    except Exception as e:
        errors.append(str(e))

    return errors
