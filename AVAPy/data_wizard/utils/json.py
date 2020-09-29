"""
Util functions for JSON processing.
"""

import re


def remove_trailing_commas(json_like):
    """
    Removes trailing commas from `json_like` and returns the result.

    Examples
    --------
    >>> remove_trailing_commas('{"foo":"bar","baz":["blah",],}')
    '{"foo":"bar","baz":["blah"]}'
    """

    trailing_object_commas_re = re.compile(
        r'(,)\s*}(?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$)')
    trailing_array_commas_re = re.compile(
        r'(,)\s*\](?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$)')
    # Fix objects {} first
    objects_fixed = trailing_object_commas_re.sub("}", json_like)
    # Now fix arrays/lists [] and return the result
    return trailing_array_commas_re.sub("]", objects_fixed)
