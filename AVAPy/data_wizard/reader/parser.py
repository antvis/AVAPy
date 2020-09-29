"""
Dataset parser functions.
"""

import pandas as pd
import AVAPy.data_wizard.utils as dwutil


def json2df(json):
    """
    Convert common JSON to pandas DataFrame.
    """

    clean_json = dwutil.remove_trailing_commas(json)
    return pd.read_json(clean_json, orient='records')
