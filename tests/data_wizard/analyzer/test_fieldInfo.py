# pylint: disable=R0201, C0116
"""
Test cases for AVA.data_wizard.FieldInfo
"""

import random
import pytest
from AVAPy import FieldInfo


class TestClassFieldInfo:
    """
    Test cases for AVAPy.FieldInfo
    """
    def test_valid_args(self):
        """
        Invalid arguments should be handled.
        """

        # None args
        with pytest.raises(TypeError, match=r".*not be None.*"):
            FieldInfo()
        with pytest.raises(TypeError, match=r".*not be None.*"):
            FieldInfo(None)

        # Empty list
        with pytest.raises(ValueError, match=r".*not.*empty.*"):
            FieldInfo([])

        # arg is not list
        with pytest.raises(TypeError, match=r".*must be a list.*"):
            FieldInfo(1)
        with pytest.raises(TypeError, match=r".*must be a list.*"):
            FieldInfo(1.1)
        with pytest.raises(TypeError, match=r".*must be a list.*"):
            FieldInfo("a")
        with pytest.raises(TypeError, match=r".*must be a list.*"):
            FieldInfo(True)
        with pytest.raises(TypeError, match=r".*must be a list.*"):
            FieldInfo((1, 2, 3))
        with pytest.raises(TypeError, match=r".*must be a list.*"):
            FieldInfo({"a": 1, "b": 2})

        # arg is valid
        FieldInfo([1, 2, "a", False])

    def test_count(self):
        fi = FieldInfo([1, 2, 3])
        assert fi.count == 3

        fi = FieldInfo([1, 2, None, "a", ""])
        assert fi.count == 5

    def test_missing(self):
        fi = FieldInfo([1, 2, 3])
        assert fi.missing == 0

        fi = FieldInfo([1, 2, None, "a"])
        assert fi.missing == 1

        fi = FieldInfo([1, 2, "", "a"])
        assert fi.missing == 1

    def test_distinct(self):
        fi = FieldInfo(["a", "b", "c", "a", "b", "a"])
        assert fi.distinct == 3

        fi = FieldInfo([9, 9, 9])
        assert fi.distinct == 1

        fi = FieldInfo([1, 2, None, ""])
        assert fi.distinct == 2

        fi = FieldInfo([None, None, None])
        assert fi.distinct == 0

    def test_type(self):
        fi = FieldInfo([1, 2, 3])
        assert fi.type == "integer"

        fi = FieldInfo([1.1, 1.2, 1.3])
        assert fi.type == "float"

        fi = FieldInfo([1, 2, 3.2])
        assert fi.type == "mixed"

    def test_nonempty_list(self):
        fi = FieldInfo([1, 2, "a", "-", "null", None, False])
        assert fi.nonempty_list() == [1, 2, "a", False]

    def test_meta_type(self):
        # empty values
        assert FieldInfo.meta_type("") == "empty"
        assert FieldInfo.meta_type(None) == "empty"
        assert FieldInfo.meta_type(float("NaN")) == "empty"
        assert FieldInfo.meta_type("null") == "empty"
        assert FieldInfo.meta_type("Null") == "empty"
        assert FieldInfo.meta_type("nULL") == "empty"
        assert FieldInfo.meta_type("None") == "empty"
        assert FieldInfo.meta_type("NaN") == "empty"

        # date
        assert FieldInfo.meta_type("2020-10-01") == "date"
        assert FieldInfo.meta_type("20201001") == "date"
        assert FieldInfo.meta_type("2020/08/01") == "date"
        assert FieldInfo.meta_type("12/08/1999") == "date"
        assert FieldInfo.meta_type("1/1/1999") == "date"
        assert FieldInfo.meta_type("2020/02") == "date"
        assert FieldInfo.meta_type("2020") == "date"
        assert FieldInfo.meta_type("2020.01.08") == "date"
        assert FieldInfo.meta_type("2020年") == "date"
        assert FieldInfo.meta_type("1991年3月") == "date"
        assert FieldInfo.meta_type("1991年3月25日") == "date"
        assert FieldInfo.meta_type("1991年03月25日") == "date"
        assert FieldInfo.meta_type("1991年 3月 25日") == "date"
        assert FieldInfo.meta_type(2002) == "date"
        assert FieldInfo.meta_type(19910325) == "date"
        assert FieldInfo.meta_type(1991325) == "date"
        assert FieldInfo.meta_type(2010101) == "date"
        assert FieldInfo.meta_type(202012) == "date"
        assert FieldInfo.meta_type(202093) == "date"

        # bool as string
        assert FieldInfo.meta_type(True) == "string"
        assert FieldInfo.meta_type(False) == "string"

        # float
        assert FieldInfo.meta_type(0.0) == "float"
        assert FieldInfo.meta_type(1.0) == "float"
        assert FieldInfo.meta_type(1.1) == "float"
        assert FieldInfo.meta_type(1.11) == "float"
        assert FieldInfo.meta_type(-1.1) == "float"
        assert FieldInfo.meta_type("1.0") == "float"
        assert FieldInfo.meta_type("1.1") == "float"

        # integer
        assert FieldInfo.meta_type(0) == "integer"
        assert FieldInfo.meta_type(1) == "integer"
        assert FieldInfo.meta_type(1000) == "integer"
        assert FieldInfo.meta_type(-10) == "integer"
        assert FieldInfo.meta_type("0") == "integer"
        assert FieldInfo.meta_type("1") == "integer"
        assert FieldInfo.meta_type("10") == "integer"
        assert FieldInfo.meta_type("-10") == "integer"

        # string
        assert FieldInfo.meta_type("abc") == "string"

        # invalid
        with pytest.raises(TypeError):
            FieldInfo.meta_type([])
        with pytest.raises(TypeError):
            FieldInfo.meta_type(())

    class TestPropertyInfo:
        """
        Unit tests cases for the core method.
        """
        def test_integer(self):
            fi = FieldInfo([0, 1, 2, 3, 4, 5, 6, 7, "+8", 9])
            info = fi.info
            assert info["count"] == 10
            assert info["distinct"] == 10
            assert info["type"] == "integer"
            assert info["implied"] == "integer"
            assert info["missing"] == 0
            assert info["valuemap"] == {
                0: 1,
                1: 1,
                2: 1,
                3: 1,
                4: 1,
                5: 1,
                6: 1,
                7: 1,
                "+8": 1,
                9: 1
            }

        def test_string_integer(self):
            fi = FieldInfo(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
            info = fi.info
            assert info["count"] == 10
            assert info["distinct"] == 10
            assert info["type"] == "integer"
            assert info["implied"] == "integer"
            assert info["missing"] == 0
            assert info["valuemap"] == {
                "0": 1,
                "1": 1,
                "2": 1,
                "3": 1,
                "4": 1,
                "5": 1,
                "6": 1,
                "7": 1,
                "8": 1,
                "9": 1
            }

        def test_string_float(self):
            fi = FieldInfo([
                "0.1", "1.1", "2.1", "3.1", "4.1", "5.1", "6.1", "7.1", "8.1",
                "9.1"
            ])
            info = fi.info
            assert info["type"] == "float"
            assert info["implied"] == "float"

        def test_number_float(self):
            fi = FieldInfo([0.1, 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1])
            info = fi.info
            assert info["type"] == "float"
            assert info["implied"] == "float"

        def test_mixed_float(self):
            fi = FieldInfo([1, 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1])
            info = fi.info
            assert info["type"] == "mixed"
            assert info["implied"] == "float"

        def test_bool(self):
            fi = FieldInfo([True, False, True, None])
            info = fi.info
            assert info["count"] == 4
            assert info["distinct"] == 2
            assert info["type"] == "string"
            assert info["implied"] == "boolean"

        def test_01_bool(self):
            fi = FieldInfo([random.randrange(0, 2, 1) for _ in range(100)])
            info = fi.info
            assert info["count"] == 100
            assert info["distinct"] == 2
            assert info["type"] == "integer"
            assert info["implied"] == "boolean"

        def test_ab_bool(self):
            # Male/Female bool
            choices = ["Male", "Female"]
            fi = FieldInfo(
                [choices[random.randrange(0, 2, 1)] for _ in range(100)])
            info = fi.info
            assert info["count"] == 100
            assert info["distinct"] == 2
            assert info["type"] == "string"
            assert info["implied"] == "boolean"

            fi = FieldInfo(
                [choices[random.randrange(0, 2, 1)] for _ in range(99)])
            info = fi.info
            assert info["implied"] == "string"

        def test_string_bool(self):
            choices = ["true", "false", None]
            fi = FieldInfo(
                [choices[random.randrange(0, 2, 1)] for _ in range(100)])
            info = fi.info
            assert info["count"] == 100
            assert info["distinct"] == 2
            assert info["type"] == "string"
            assert info["implied"] == "boolean"

        def test_empty(self):
            fi = FieldInfo([
                "", "none",
                float("NaN"), "null", None, "null", "-", "nan", ""
            ])
            info = fi.info
            assert info["count"] == 9
            assert info["distinct"] == 0
            assert info["type"] == "empty"
            assert info["implied"] == "empty"

        def test_string(self):
            fi = FieldInfo([
                "type113", "type14", "type11321", "type", "type23", "type2",
                "type2", "type2", "type2", "type2"
            ])
            info = fi.info
            assert info["count"] == 10
            assert info["distinct"] == 6
            assert info["type"] == "string"
            assert info["implied"] == "string"

        def test_mixed_string(self):
            fi = FieldInfo([
                "1", "a", "2019-01-01", "type", "type23", "type2", "type2",
                "type2", "type2", "type2"
            ])
            info = fi.info
            assert info["count"] == 10
            assert info["distinct"] == 6
            assert info["type"] == "mixed"
            assert info["implied"] == "string"

        def test_date(self):
            fi = FieldInfo([
                "2015-01-01",
                "2015-01-02",
                "2015-01-03",
                "2015-01-04",
                "2015-01-05",
                "2015-01-06",
                "2015-01-07",
                "2015-01-08",
                "2015-01-09",
                "2015-01-10",
            ])
            info = fi.info
            assert info["count"] == 10
            assert info["distinct"] == 10
            assert info["type"] == "date"
            assert info["implied"] == "date"

        # def test_original_date(self): # TODOlater
        # fi = FieldInfo([
        #     datetime.strptime("20150101", "%Y%m%d").date(),
        #     datetime.strptime("20150102", "%Y%m%d").date(),
        #     datetime.strptime("20150103", "%Y%m%d").date(),
        # ])
        # info = fi.info
        # assert info["count"] == 3
        # assert info["distinct"] == 3
        # assert info["type"] == "date"
        # assert info["implied"] == "date"

        def test_string_like_number(self):
            fi = FieldInfo([
                "0.1", "1.1.1", "2.1.b", "3.1.c", "4.1.d", "5.1.e", "6.1.f",
                "7.1.g", "8.1.a", "9.1.c"
            ])
            info = fi.info
            assert info["count"] == 10
            assert info["distinct"] == 10
            assert info["type"] == "mixed"
            assert info["implied"] == "string"
