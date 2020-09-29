"""
The functions tend to configure auxiliaries
on plotting single-class scatterplots
as vega specifications.

Data format:
    1. x = [], y = []
    2. json {x:..., y:...}
    *x.dtype == Number or String
    *y.dtype == Number
"""

import numpy as np
import pandas as pd
import altair as alt

from . import auxiliary as auxutil


def estimate_gaussian(data):
    """
    Return Gaussian Estimation for data.
    """

    mu = np.mean(data)
    sigma = np.std(data)
    limit = sigma * 1.5

    min_threshold = mu - limit
    max_threshold = mu + limit

    return mu, sigma, min_threshold, max_threshold


def add_outliers_by_zscore(data, threshold=3):
    """
    Add a new created column `color_outlier` to data and
    return the index of outliers.

    Outliers determined by z-score will be "outlier" in `color_outlier` column.
    """

    colnames = list(data.columns)
    mean_x = np.mean(data[colnames[0]])
    std_x = np.std(data[colnames[0]])

    mean_y = np.mean(data[colnames[1]])
    std_y = np.std(data[colnames[1]])

    outliers = []

    for index in range(len(data[colnames[0]])):
        x = data[colnames[0]][index]
        y = data[colnames[1]][index]
        z_score_y = (y - mean_y) / std_y
        z_score_x = (x - mean_x) / std_x
        if np.abs(z_score_x) >= threshold and np.abs(z_score_y) >= threshold:
            outliers.append(index)
            data["color_outlier"][index] = "outlier"
    return outliers


def add_outliers_by_gaussian(data):
    """
    Add a new created column `color_outlier` to data and
    return the index of outliers.

    Outliers determined by gaussian will be "outlier" in `color_outlier`
    column.
    """

    colnames = list(data.columns)
    min_threshold, max_threshold = estimate_gaussian(data)[2:]

    outliers = []

    for index in range(len(data[colnames[0]])):
        x = data[colnames[0]][index]
        y = data[colnames[1]][index]
        if (x > max_threshold[0]
                and y > max_threshold[1]) or (x < min_threshold[0]
                                              and y < min_threshold[1]):
            outliers.append(index)
            data.loc[index, "color_outlier"] = "outlier"
    return outliers


def add_outliers_by_iqr(data):
    """
    Add a new created column `color_outlier` to data and
    return the index of outliers.

    Outliers determined by IQR will be "outlier" in `color_outlier` column.
    """

    colnames = list(data.columns)
    q1 = data[colnames[1]].quantile(0.25)
    q3 = data[colnames[1]].quantile(0.75)
    iqr = q3 - q1
    lby = q1 - 1.5 * iqr
    uby = q3 + 1.5 * iqr

    q1 = data[colnames[0]].quantile(0.25)
    q3 = data[colnames[0]].quantile(0.75)
    iqr = q3 - q1
    lbx = q1 - 1.5 * iqr
    ubx = q3 + 1.5 * iqr

    outliers = []

    for index in range(len(data[colnames[1]])):
        x = data[colnames[0]][index]
        y = data[colnames[1]][index]
        if ((y < lby) or (y > uby) or (x < lbx) or (x > ubx)):
            outliers.append(index)
            data["color_outlier"][index] = "outlier"
    return outliers


def get_scatter(df, deg=3):
    """
    Generate scatterplot with auxiliaries by given DataFrame.

    The return is JSON in vega-lite schema.
    """

    df["color_outlier"] = "normal"
    colnames = list(df.columns)

    add_outliers_by_zscore(df)

    chart = alt.Chart(df).mark_point().encode(x=colnames[0],
                                              y=colnames[1],
                                              color="color_outlier")

    if df[colnames[0]].dtype in (int, float):
        auxutil.add_trend_line(df, deg)
    else:
        auxutil.add_trend_line_nonnum(df, deg)

    line = chart.mark_line(color="red",
                           opacity=0.75).encode(y="trend_line",
                                                color="trend_line_col")

    return (chart + line).to_json()


def get_scatter_xy(x, y):
    """
    Generate scatterplot with auxiliaries by given columns `x` and `y`.

    The return is JSON in vega-lite schema.
    """

    df = pd.DataFrame({"x": x, "y": y})
    return get_scatter(df)


def get_scatter_json(json_data):
    """
    Generate scatterplot with auxiliaries by given data in JSON.

    The return is JSON in vega-lite schema.
    """

    df = pd.read_json(json_data, orient="records")
    return get_scatter(df)
