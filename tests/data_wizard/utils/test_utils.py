# pylint: disable=R0201, C0116
"""
Test cases for AVA.data_wizard.utils.utils
"""

import pytest
from AVAPy import is_empty_value, is_date, is_bool_field


class TestDWUtils:
    """
    Test cases for AVAPy.data_wizard.utils
    """

    def test_is_empty_value(self):
        """Unit tests for function: is_empty_value"""

        assert is_empty_value("") is True
        assert is_empty_value(None) is True
        assert is_empty_value(float("NaN")) is True
        assert is_empty_value("null") is True
        assert is_empty_value("Null") is True
        assert is_empty_value("nULL") is True
        assert is_empty_value("None") is True
        assert is_empty_value("NaN") is True
        assert is_empty_value("-") is True

        assert is_empty_value(" ") is False
        assert is_empty_value("no") is False
        assert is_empty_value("a") is False
        assert is_empty_value(0) is False
        assert is_empty_value(False) is False

        with pytest.raises(TypeError, match=r".*must be.*"):
            is_empty_value([])
        with pytest.raises(TypeError, match=r".*must be.*"):
            is_empty_value(())
        with pytest.raises(TypeError, match=r".*must be.*"):
            is_empty_value({"a": 1})

    def test_is_date(self):
        """Unit tests for function: is_date"""

        # commion date formats
        assert is_date("2020-10-01") is True
        assert is_date("20201001") is True
        assert is_date("2020/08/01") is True
        assert is_date("12/08/1999") is True
        assert is_date("1/1/1999") is True
        assert is_date("2020/02") is True
        assert is_date("2020") is True
        assert is_date("2020.01.08") is True

        # Chinese date format
        assert is_date("2020年") is True
        assert is_date("1991年3月") is True
        assert is_date("1991年3月25日") is True
        assert is_date("1991年03月25日") is True
        assert is_date("1991年 3月 25日") is True

        # leap year
        assert is_date("2004.02.29") is True
        assert is_date("2005.02.29") is False

        # integers
        assert is_date(2002) is True
        assert is_date(19910325) is True
        assert is_date(1991325) is True
        assert is_date(2010101) is True
        assert is_date(202012) is True
        assert is_date(202093) is True

        assert is_date(1234) is False
        # assert is_date(20050229) is False # todolater

    def test_is_bool_field(self):
        # true
        assert is_bool_field([True, False]) is True
        assert is_bool_field([True, False, False, False]) is True
        assert is_bool_field([True, True, True]) is True
        assert is_bool_field([False, False, False]) is True
        assert is_bool_field([False]) is True
        assert is_bool_field([True]) is True
        assert is_bool_field([0, 1, 1, 1, 1, 0, 1, 1]) is True
        assert is_bool_field(["True", "False", "False"]) is True
        assert is_bool_field(["true", "true", "false"]) is True
        assert is_bool_field(["T", "F", "F", "F", "T", "F"]) is True
        assert is_bool_field(["f", "f", "f", "f", "f", "t"]) is True
        assert is_bool_field(["0", "0", "1"]) is True
        assert is_bool_field(["是", "否"]) is True
        assert is_bool_field([True, 0, 1, 1, False]) is True

        # false
        assert is_bool_field([1, 0, "t", "f"]) is False
        assert is_bool_field(["trUe", "fAlse"]) is False
        assert is_bool_field([True, False, "a"]) is False
        assert is_bool_field([True, False, None]) is False

        assert is_bool_field([]) is False

        # invalid
        with pytest.raises(TypeError, match=r".*must be iterable.*"):
            is_bool_field(1)
