"""
Util functions for type inference.
"""

import re
import math
import numbers
from datetime import datetime


def is_empty_value(value) -> bool:
    """
    Whether a value is "empty value".

    Empty values include '', None, NaN and strings like 'null', 'none',
    'nan', '-' (ignore case).

    Parameters
    ----------
    value : str, Number or None
        Passing invalid `value` will raise a ``TypeError``. Instead, the value
        will be checked.

    Returns
    -------
    bool
        `True` if the `value` is an "empty value".

    Raises
    ------
    TypeError
      * If `value` is invalid.

    Examples
    --------
    >>> is_empty_value(3)
    >>> False

    >>> is_empty_value('')
    >>> True
    """

    if not isinstance(value, (type(None), numbers.Number, str)):
        raise TypeError("Argument must be a Number or str or None.")

    empty_strs = ['null', 'none', 'nan', '-']
    return value == '' or value is None or (isinstance(
        value, numbers.Number) and math.isnan(value)) or (isinstance(
            value, str) and value.lower() in empty_strs)


def is_date(value) -> bool:
    """
    Whether a string/int can be interpreted as a date.

    Most common date formats can be parsed.

    Parameters
    ----------
    value : str or int
        A string/int containing a date/time stamp.

    Returns
    -------
    bool
        `True` if the `value` is in a valid date format.

    Raises
    ------
    TypeError
      * If `value` is invalid.

    Examples
    --------
    >>> is_date("2020-10-01")
    >>> True

    >>> is_date(20201001)
    >>> True

    >>> is_date("1234")
    >>> False
    """

    int_date_patterns = [
        r"^(19|20)\d{2}$", r"^\d{4}(0?[1-9]|1[012])$",
        r"^\d{4}(0?[1-9]|1[012])(0?[1-9]|[12]\d|3[01])$"
    ]

    fmts = [
        "%Y年%m月%d日", "%Y年", "%Y年%m月", "%Y-%m-%d", "%Y%m%d", "%Y/%m/%d",
        "%m/%d/%Y", "%Y/%m", "%Y", "%Y.%m.%d"
    ]

    isdate = False

    if isinstance(value, str):
        for fmt in fmts:
            try:
                datetime.strptime(value.replace(" ", ""), fmt)
                isdate = True
            except ValueError:
                pass
    elif isinstance(value, int):
        for pattern in int_date_patterns:
            if re.match(pattern, str(value)):
                isdate = True

    return isdate


def is_bool_field(ary) -> bool:
    """
    Whether a field can be interpreted as booleans.

    Parameters
    ----------
    ary : iterable object
        A field containing values that could be booleans.

    Returns
    -------
    bool
        `True` if the `ary` is determined as booleans.

    Raises
    ------
    TypeError
      * If `ary` is not iterable.

    Examples
    --------
    >>> is_bool_field(["True", "False", "False"])
    >>> True

    >>> is_bool_field([True, 0, 1, 1, False])
    >>> True

    >>> is_bool_field([True, False, "a"])
    >>> False
    """

    try:
        iter(ary)
    except TypeError as error:
        raise TypeError("Argument must be iterable.") from error

    bools = [
        [True, False],
        [0, 1],
        ["True", "False"],
        ["true", "false"],
        ["T", "F"],
        ["t", "f"],
        ["0", "1"],
        ["是", "否"],
    ]

    if not ary:
        return False

    return any(all(x in b for x in ary) for b in bools)
