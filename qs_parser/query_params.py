from typing import Self

from qs_parser.query_key_detail import QueryKeyDetail


class QueryParamValue:
    """
    QueryParamValue is a class that represents a single query
    parameter value with a key and value.
    """

    index: str | int
    value: str

    def __init__(self: Self, index: str | int, value: str) -> None:
        """
        Constructor for QueryParamValue class.

        Args:
            index (str | int): The index of the query parameter.
            value (str): The value of the query parameter.
        """
        self.index = index
        self.value = value


class QueryParam:
    """
    QueryParam is a class that represents a single query parameter
    with a key and a list of QueryParamValue.
    """

    key: str
    values: list[QueryParamValue] | QueryParamValue | None = None
    last_index: int = 0
    has_associated_values: bool = False

    def __init__(self: Self, key: str) -> None:
        """
        Constructor for QueryParam class.

        Args:
            key (str): The key of the query parameter.
        """
        self.key = key

    def add_value(self: Self, value: str, force_append: bool = False) -> None:
        """
        Add a value to the query parameter.

        Args:
            value (str): The value to add.
            force_append (bool): Whether to force the value
                to be appended to the list of values.
        """
        append_value = QueryParamValue(self.last_index, value)

        if self.values is None:
            self.values = [append_value] if force_append else append_value
        elif isinstance(self.values, list):
            self.values.append(append_value)
        else:
            self.values = [self.values, append_value]
        self.last_index += 1

    def add_associated_value(self: Self, key: str, value: str) -> None:
        """
        Add a value to the query parameter.

        Args:
            key (str): The key of the query parameter.
            value (str): The value to add.
        """
        try:
            key_int = int(key)
            if key_int > self.last_index:
                self.last_index = key_int
            self.add_value(value, force_append=True)
        except ValueError:
            if self.values is None:
                self.values = []
            if isinstance(self.values, QueryParamValue):
                self.values = [self.values]

            self.values.append(QueryParamValue(key, value))  # type: ignore
            self.has_associated_values = True

    def to_dict(self: Self) -> dict[str, str | list[str] | dict[str, str]]:
        """
        Convert the query parameter to a dictionary.

        Returns:
            dict[str, str | list[str]]: The query parameter as a dictionary.
        """
        if self.values is None:
            raise ValueError("QueryParam has no values")

        if self.has_associated_values:
            associated_values: dict[str, str] = {}
            for value in self.values:  # type: ignore
                associated_values[str(value.index)] = str(value.value)
            return {self.key: associated_values}

        if isinstance(self.values, list):
            return {self.key: [value.value for value in self.values]}

        return {self.key: self.values.value}


class QueryParams:
    """
    QueryParams is a class that represents a list of query parameters.
    """

    params: dict[str, QueryParam]

    def __init__(self: Self) -> None:
        """
        Constructor for QueryParams class.
        """
        self.params = {}

    def add(self: Self, key: QueryKeyDetail, value: str) -> None:
        """
        Add a value to the query parameters.

        Args:
            key (QueryKeyDetail): The key of the query parameter.
            value (str): The value to add.
        """
        if key.key not in self.params:
            self.params[key.key] = QueryParam(key.key)

        if key.index is None or key.index == -1:
            self.params[key.key].add_value(value)
        else:
            self.params[key.key].add_associated_value(key.index, value)

    def to_dict(self: Self) -> dict[str, str | list[str] | dict[str, str]]:
        """
        Convert the query parameters to a dictionary.

        Returns:
            dict[str, str | list[str] | dict[str, str]]:
            The query parameters as a dictionary.
        """
        result = {}
        for param in self.params.values():
            result[param.key] = param.to_dict()[param.key]

        return result
