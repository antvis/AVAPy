"""
Class for analyzing data field.
"""

import AVAPy.data_wizard.utils as dwutil


def infer_type_from_types(types):
    """
    Infer types of a field from its original type list.
    """

    type_kinds = len(types)

    if type_kinds == 0:
        field_type = "empty"
        implied_type = "empty"
    elif type_kinds == 1:
        field_type = types[0]
        implied_type = types[0]
    elif type_kinds == 2:
        field_type = "mixed"
        if "integer" in types and "float" in types:
            implied_type = "float"
        else:
            implied_type = "string"
    else:
        field_type = "mixed"
        implied_type = "string"

    return field_type, implied_type


class FieldInfo:
    """
    Statistical characteristics and properties of a field obtained
    through analysis.

    Attributes
    ----------
    field : list
        List of data as a column or field.

    Methods
    -------
    count()
        Return number of values in the field, including empty/invalid values.
    nulls()
        Return number of empty values.
    """

    BOOL_SUFFICIENT_LENGTH = 100

    def __init__(self, field=None):
        """
        Parameters
        ----------
        field : list
            List of data as a column or field.
        """

        if field is None:
            raise TypeError("Argument field can not be None.")
        if not isinstance(field, list):
            raise TypeError("Argument field must be a list.")
        if len(field) == 0:
            raise ValueError("Argument field can not be an empty list.")

        self.__field = field

        # One-round traversal (for performance)

        count = 0
        empty_val_indices = []
        value_map = {}
        types = []

        for idx, val in enumerate(field):

            count += 1

            if dwutil.is_empty_value(val):
                empty_val_indices.append(idx)
            else:
                if val in value_map:
                    value_map[val] += 1
                else:
                    value_map[val] = 1

                type_str = FieldInfo.meta_type(val)
                if type_str not in types:
                    types.append(type_str)

        field_type, implied_type = infer_type_from_types(types)

        data_list = list(
            map(lambda x: None if dwutil.is_empty_value(x) else x, field))
        self.__data_list = data_list

        distinct = len(value_map)

        if distinct == 2 and implied_type != "date" and (
                len(data_list) >= self.BOOL_SUFFICIENT_LENGTH
                or dwutil.is_bool_field(list(value_map.keys()))):
            implied_type = "boolean"

        info = {
            "count": count,
            "distinct": distinct,
            "type": field_type,
            "implied": implied_type,
            "missing": len(empty_val_indices),
            "valuemap": value_map
        }

        self.__info = info

    @staticmethod
    def meta_type(value):
        """
        Return the 1st level inference for the type of a value.
        """

        if dwutil.is_empty_value(value):
            return "empty"

        if dwutil.is_date(value):
            return "date"

        if isinstance(value, bool):
            return "string"

        if isinstance(value, float):
            return "float"

        if isinstance(value, int):
            return "integer"
        try:
            int(value)
            return "integer"
        except ValueError:
            pass

        if isinstance(value, str):
            try:
                int(value)
                return "integer"
            except ValueError:
                try:
                    float(value)
                    return "float"
                except ValueError:
                    return "string"
        else:
            raise TypeError("Argument is in invalid type.")

    @property
    def info(self):
        """
        Return all information collected for the field.
        """

        return self.__info

    @property
    def data_list(self):
        """
        Return a copy of the field, replace all empty values with None.
        """

        return self.__data_list

    @property
    def count(self):
        """
        Return number of values in the field, including empty/invalid values.

        It is like the number of rows in a data column.

        Returns
        -------
        int
            Number of values in the field, including empty/invalid values.

        Examples
        --------
        >>> fi = FieldInfo([1, 2, None, "a"])
        >>> fi.count()
        4
        """

        return self.__info["count"]

    @property
    def distinct(self):
        """
        Number of kinds of non-empty value in the field.
        """

        return self.__info["distinct"]

    @property
    def type(self):
        """
        Return the 1st level inference for the type of field.
        """

        return self.__info["type"]

    @property
    def implied(self):
        """
        Return the 2nd level inference for the type of field.
        """

        return self.__info["implied"]

    @property
    def missing(self):
        """
        Number of empty values in the field.

        Returns
        -------
        int
            Number of empty values.

        See Also
        --------
        is_empty_value : Whether a value is "empty value".

        Examples
        --------
        >>> fi = FieldInfo([1, 2, None, "a"])
        >>> fi.missing
        1
        """

        return self.__info["missing"]

    @property
    def valuemap(self):
        """
        Return a dict that records all non-empty values and their counts.
        """

        return self.__info["valuemap"]

    def nonempty_list(self):
        """
        Return the field with all empty-value filtered.
        """

        return list(filter(lambda x: x is not None, self.__data_list))
