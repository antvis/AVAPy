"""
Util functions for adding auxiliaries to chart.
"""

import numpy as np


def add_trend_line(data, deg=5):
    """
    Add new created columns `trend_line` and `trend_line_col` to data.

      * The `trend_line` describe a polynomial trend on `x`.
      * The `trend_line_col` is the column name "trend_line".
    """

    colnames = list(data.columns)
    x = data[colnames[0]]
    y = data[colnames[1]]

    parameter = np.polyfit(x, y, deg)
    f = np.poly1d(parameter)

    data["trend_line"] = f(x)
    data["trend_line_col"] = "trend_line"


def add_trend_line_nonnum(data, deg=5):
    """
    Add new created columns `trend_line` and `trend_line_col` to data,
    while `x` is not numbers.

      * The `trend_line` describe a polynomial trend on `x`.
      * The `trend_line_col` is the column name "trend_line".
    """

    colnames = list(data.columns)
    y = data[colnames[1]]
    x = list(range(len(y)))

    parameter = np.polyfit(x, y, deg)
    f = np.poly1d(parameter)

    data["trend_line"] = f(x)
    data["trend_line_col"] = "trend_line"


def get_marks(data):
    """
    Return mean, Q3, Q1 of data.
    """
    colnames = list(data.columns)

    mean = np.mean(data[colnames[1]])
    q75 = data[colnames[1]].quantile(0.75)
    q25 = data[colnames[1]].quantile(0.25)

    return mean, q75, q25


def add_quant_line(chart, data, mks=1):
    """
    Add auxiliary lines for mean, (Q1, Q3) of data to the chart.
    """
    mean, q75, q25 = get_marks(data)

    data['mark_line_avg'] = mean
    data['mark_line_25'] = q25
    data['mark_line_75'] = q75

    quant_line = chart.mark_line(color='gray',
                                 opacity=0.5).encode(y='mark_line_avg')

    if mks == 2:
        if abs(mean - q25) > abs(mean - q75):
            quant_line = quant_line + chart.mark_line(
                color='gray', opacity=0.5).encode(y='mark_line_q25')
        else:
            quant_line = quant_line + chart.mark_line(
                color='gray', opacity=0.5).encode(y='mark_line_q75')
    elif mks == 3:
        quant_line = quant_line + chart.mark_line(
            color='gray', opacity=0.5).encode(y='mark_line_q25')
        quant_line = quant_line + chart.mark_line(
            color='gray', opacity=0.5).encode(y='mark_line_q75')

    return quant_line
