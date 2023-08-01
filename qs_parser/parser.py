import re
from typing import Any
from urllib.parse import parse_qs


def parse_query_string(query_string: str) -> dict[str, Any]:
    """Parse the query string and return a dict of the query parameters.

    Args:
        query_string (str): The query string to parse.

    Returns:
        dict[str, Any]: A dict of the query parameters.
    """
    if query_string == "":
        return {}

    split_params = parse_qs(query_string, keep_blank_values=True)

    return combine_query_keys(split_params)


def combine_query_keys(
    query_keys: dict[str, Any]
) -> dict[str, list[Any] | dict[str, Any] | str]:
    """Combine the query keys into a query string.

    Args:
        query_keys (dict[str, Any]): The query keys to combine.

    Returns:
        dict[str, list[Any] | dict[str, Any] | str]: The combined query keys.
    """
    query_params: dict[str, list[Any] | dict[str, Any] | str] = {}

    for query_key, values in query_keys.items():
        for value in values:
            query_param_details = get_details_from_key(query_key)
            key: str = str(query_param_details["key"])
            index: str | int | None = query_param_details["index"]

            match index:
                case None:
                    query_params = add_simple_query_param(query_params, key, value)
                case int():
                    query_params = add_numeric_indexed_query_param(
                        query_params, key, value
                    )
                case str():
                    query_params = add_string_indexed_query_param(
                        query_params, key, value, index
                    )

    return query_params


def get_details_from_key(key: str) -> dict[str, str | int | None]:
    """Get the details from the key and value.

    Args:
        key (str): The key to get the details from.

    Returns:
        dict[str, str | None]: The details from the key and value.
    """
    if key.endswith("[]"):
        return {"key": key[:-2], "index": -1}

    regex_key = r"^(?P<key>.+)\[(?P<index>.+)\]$"
    if match := re.match(regex_key, key):
        return {"key": match.group("key"), "index": match.group("index")}

    return {"key": key, "index": None}


def add_simple_query_param(
    current: dict[str, list[Any] | dict[str, Any] | str], key: str, value: str
) -> dict[str, list[Any] | dict[str, Any] | str]:
    """Add a simple query parameter to the current query parameters.

    Args:
        current (dict[str, list[Any] | dict[str, Any] | str]):
            The current query parameters.
        key (str): The key to add.
        value (str): The value to add.

    Returns:
        dict[str, list[Any] | dict[str, Any] | str]: The updated query parameters.
    """
    if key not in current:
        current[key] = value
        return current

    if isinstance(current[key], list):
        current[key].append(value)  # type: ignore
        return current

    if isinstance(current[key], dict):
        current[key][str(find_last_numeric_index(current[key]))] = value  # type: ignore
        return current

    current[key] = [current[key], value]
    return current


def add_numeric_indexed_query_param(
    current: dict[str, list[Any] | dict[str, Any] | str], key: str, value: str
) -> dict[str, list[Any] | dict[str, Any] | str]:
    """Add a numeric indexed query parameter to the current query parameters.

    Args:
        current (dict[str, list[Any] | dict[str, Any] | str]):
            The current query parameters.
        key (str): The key to add.
        value (str): The value to add.

    Returns:
        dict[str, list[Any] | dict[str, Any] | str]: The updated query parameters.
    """
    if key not in current:
        current[key] = [value]
        return current

    if isinstance(current[key], list):
        current[key].append(value)  # type: ignore
        return current

    if isinstance(current[key], dict):
        current[key][str(find_last_numeric_index(current[key]))] = value  # type: ignore
        return current

    current[key] = [current[key], value]
    return current


def add_string_indexed_query_param(
    current: dict[str, list[Any] | dict[str, Any] | str],
    key: str,
    value: str,
    index: str,
) -> dict[str, list[Any] | dict[str, Any] | str]:
    """Add a string indexed query parameter to the current query parameters.

    Args:
        current (dict[str, list[Any] | dict[str, Any] | str]):
            The current query parameters.
        key (str): The key to add.
        value (str): The value to add.
        index (str): The index to add.

    Returns:
        dict[str, list[Any] | dict[str, Any] | str]: The updated query parameters.
    """
    if key not in current:
        current[key] = {index: value}
        return current

    if isinstance(current[key], list):
        converted = {}
        for i, item in enumerate(current[key]):
            converted[f"{i}"] = item

        converted[index] = value
        current[key] = converted
        return current

    if isinstance(current[key], dict):
        current[key][index] = value  # type: ignore
        return current

    current[key] = {"0": current[key], index: value}
    return current


def find_last_numeric_index(current: dict[str, Any] | list[Any] | str) -> int:
    """Find the last numeric index for the key.

    Args:
        current (dict[str, Any] | list[Any] | str): The current query parameters.

    Returns:
        int: The last numeric index for the key.
    """

    if isinstance(current, str):
        return 0

    last_index = 0
    for index in current:
        try:
            index = int(index)
            if index >= last_index:
                last_index = index + 1
        except ValueError:
            continue

    return last_index
