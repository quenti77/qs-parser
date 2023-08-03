import re
from typing import Self


class QueryKeyDetail:
    """
    Value object for storing the details of a query key.
    """

    key: str
    index: str | int | None

    def __init__(self: Self, key: str, index: str | int | None) -> None:
        """
        Constructor for QueryKeyDetail class.

        Args:
            key (str): The key of the query parameter.
            index (str | int | None): The index of the query parameter.
        """
        self.key = key
        self.index = index

    @classmethod
    def parse_key(cls, key: str) -> Self:
        """
        Parse a key and return a QueryKeyDetail object.

        Args:
            key (str): The key to parse.

        Returns:
            Self: The QueryKeyDetail object.
        """
        if key.endswith("[]"):
            return cls(key[:-2], -1)

        regex_key = r"^(?P<key>.+)\[(?P<index>.+)\]$"
        if match := re.match(regex_key, key):
            return cls(match.group("key"), match.group("index"))

        return cls(key, None)
