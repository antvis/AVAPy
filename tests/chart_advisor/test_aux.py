# pylint: disable=R0201, C0116
"""
The file tests the specifications of auxiliaries.

Data format:
    1. x = [], y = []
    2. json {x:..., y:...}
"""

import json
import pytest
import numpy as np

from AVAPy import get_scatter_xy
from AVAPy import get_line_xy
from AVAPy import get_bar_xy


def layer_is_in_mark(layer, mark):
    """
    Whether the given layer is in the given mark.
    """
    return layer["mark"] == mark or ("type" in layer["mark"]
                                     and layer["mark"]["type"] == mark)


def type_layer_number(layers, marktype):
    """
    Return how many layers is in given mark type `marktype`.
    """
    return len(
        list(filter(lambda layer: layer_is_in_mark(layer, marktype), layers)))


class TestAux:
    """
    Test cases for AVAPy.chart_advisor.aux
    """

    rng = np.random.RandomState(1)
    x = rng.rand(40)**2
    y = x * 10 + rng.randn(40)

    data_samples = [(x, y)]

    @pytest.mark.parametrize(("x", "y"), data_samples)
    def test_scatter(self, x, y):
        schema = get_scatter_xy(x, y)
        dic = json.loads(s=schema)
        assert len(dic["layer"]) == 2
        assert type_layer_number(dic["layer"], "point") == 1
        assert type_layer_number(dic["layer"], "line") == 1

    @pytest.mark.parametrize(("x", "y"), data_samples)
    def test_line(self, x, y):
        schema = get_line_xy(x, y)
        dic = json.loads(s=schema)
        assert len(dic["layer"]) == 3
        assert type_layer_number(dic["layer"], "line") == 3

    @pytest.mark.parametrize(("x", "y"), data_samples)
    def test_bar(self, x, y):
        x = list(range(len(y)))
        schema = get_bar_xy(x, y)
        dic = json.loads(s=schema)
        assert len(dic["layer"]) == 3
        assert type_layer_number(dic["layer"], "line") == 2
        assert type_layer_number(dic["layer"], "bar") == 1
