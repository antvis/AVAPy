import pandas as pd


def json2df(json):
    # TODO: remove last comma in each array, if exists
    return pd.read_json(json, orient='records')
