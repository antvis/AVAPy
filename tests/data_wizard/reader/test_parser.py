# pylint: disable=R0201, C0116
"""
Test cases for AVA.data_wizard.FieldInfo
"""

import pandas as pd
from AVAPy.data_wizard.reader.parser import json2df


def test_json2df():
    df = pd.DataFrame([['a', 100], ['b', 110], ['c', 120]],
                      columns=['name', 'value'])

    result = json2df('['
                     '{"name": "a", "value": 100},'
                     '{"name": "b", "value": 110},'
                     '{"name": "c", "value": 120}'
                     ']')
    assert df.equals(result)
