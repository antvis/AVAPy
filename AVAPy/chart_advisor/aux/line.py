"""
The functions tend to configure auxiliaries
on plotting single line charts
as vega specifications.

Data format:
    1. x = [], y = []
    2. json {x:..., y:...}
    *y.dtype == Number
    *x.dtype == Number or String
"""

import pandas as pd
import altair as alt

from . import auxiliary as auxutil


def get_line(df, mks=1, deg=3):
    """
    Generate line chart with auxiliaries by given DataFrame.

    The return is JSON in vega-lite schema.

    Parameters
    ----------
    df : DataFrame
        Given data.
    mks : int
        Expect number of auxiliary lines.
    deg : int
        Degree of the fitting polynomial.
    """

    colnames = list(df.columns)

    chart = alt.Chart(df).mark_line().encode(x=colnames[0], y=colnames[1])

    if df[colnames[0]].dtype in (int, float):
        auxutil.add_trend_line(df, deg)
    else:
        auxutil.add_trend_line_nonnum(df, deg)

    quant_line = auxutil.add_quant_line(chart, df, mks)

    trend_line = chart.mark_line(color='red',
                                 opacity=0.75).encode(y='trend_line')

    return (chart + trend_line + quant_line).to_json()


def get_line_xy(x, y):
    """
    Generate line chart with auxiliaries by given columns `x` and `y`.

    The return is JSON in vega-lite schema.
    """

    df = pd.DataFrame({"x": x, "y": y})
    return get_line(df)


def get_line_json(json_data):
    """
    Generate line chart with auxiliaries by given data in JSON.

    The return is JSON in vega-lite schema.
    """

    df = pd.read_json(json_data, orient='records')
    return get_line(df)
