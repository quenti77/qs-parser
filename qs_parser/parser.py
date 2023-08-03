from typing import Self
from urllib.parse import parse_qs

from qs_parser.query_key_detail import QueryKeyDetail
from qs_parser.query_params import QueryParams


class Parser:
    """
    Parser class for parsing query strings.
    """

    query_string: dict[str, list[str]]

    def __init__(self: Self, query_string: str) -> None:
        """
        Constructor for Parser class. Transforms the
        query string into a dictionary of lists for easier.

        Args:
            query_string (str): The query string to parse.
        """
        self.query_string = parse_qs(query_string)

    def parse(self: Self) -> dict[str, str | list[str] | dict[str, str]]:
        """
        Parse the query string and return a dictionary of lists.

        Returns:
            dict[str, str | list[str] | dict[str, str]]: The parsed query string.
        """
        query_params = QueryParams()

        for query_key, values in self.query_string.items():
            query_param_details = QueryKeyDetail.parse_key(query_key)
            for value in values:
                query_params.add(query_param_details, value)

        return query_params.to_dict()
