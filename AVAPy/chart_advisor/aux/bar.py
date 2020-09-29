"""
The functions tend to configure auxiliaries
on plotting single bar charts
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


def get_bar(df, mks=1, deg=3):
    """
    Generate bar chart with auxiliaries by given DataFrame.

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

    chart = alt.Chart(df).mark_bar().encode(x=colnames[0], y=colnames[1])

    auxutil.add_trend_line(df, deg)

    quant_line = auxutil.add_quant_line(chart, df, mks)

    trend_line = chart.mark_line(color="red",
                                 opacity=0.75).encode(y="trend_line")

    (chart + trend_line + quant_line).save("/tmp/bar.html")
    return (chart + trend_line + quant_line).to_json()


def get_bar_xy(x, y):
    """
    Generate bar chart with auxiliaries by given columns `x` and `y`.

    The return is JSON in vega-lite schema.
    """

    df = pd.DataFrame({"x": x, "y": y})
    return get_bar(df)


def get_bar_json(json_data):
    """
    Generate bar chart with auxiliaries by given data in JSON.

    The return is JSON in vega-lite schema.
    """

    df = pd.read_json(json_data, orient="records")
    return get_bar(df)
