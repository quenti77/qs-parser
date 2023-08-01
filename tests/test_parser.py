from qs_parser.parser import add_numeric_indexed_query_param
from qs_parser.parser import add_simple_query_param
from qs_parser.parser import add_string_indexed_query_param
from qs_parser.parser import find_last_numeric_index
from qs_parser.parser import get_details_from_key
from qs_parser.parser import parse_query_string


# test for "parse_query_string" function
def test_parser_with_empty_string_returns_empty_dict() -> None:
    assert parse_query_string("") == {}


def test_parser_with_non_empty_string_returns_dict_of_query_params() -> None:
    assert parse_query_string("a=1&b=2&b[]=3&b[other]=4") == {
        "a": "1",
        "b": {"0": "2", "1": "3", "other": "4"},
    }


# test for "combine_query_keys" function


# test for "get_details_from_key" function
def test_get_details_with_simple_data_returns_index_as_none() -> None:
    assert get_details_from_key("a") == {"key": "a", "index": None}


def test_get_details_with_empty_array_data_returns_index_as_zero() -> None:
    assert get_details_from_key("a[]") == {"key": "a", "index": -1}


def test_get_details_with_index_array_data_returns_index_passed() -> None:
    assert get_details_from_key("a[price]") == {"key": "a", "index": "price"}


# test for "add_simple_query_param" function
def test_add_simple_value_without_key_exist_returns_dict_with_key_and_value() -> None:
    assert add_simple_query_param({}, "a", "1") == {"a": "1"}


def test_add_simple_value_with_key_exist_returns_dict_with_list() -> None:
    assert add_simple_query_param({"a": "1"}, "a", "2") == {"a": ["1", "2"]}


def test_add_simple_value_with_key_exist_and_is_list_returns_dict_with_list() -> None:
    assert add_simple_query_param({"a": ["1"]}, "a", "2") == {"a": ["1", "2"]}


def test_add_simple_value_with_key_exist_and_is_dict_returns_dict_with_dict() -> None:
    assert add_simple_query_param({"a": {"key": "1"}}, "a", "2") == {
        "a": {"key": "1", "0": "2"}
    }


# test for "add_numeric_indexed_query_param" function
def test_add_value_without_key_exist_returns_dict_with_key_and_value() -> None:
    assert add_numeric_indexed_query_param({}, "a", "1") == {"a": ["1"]}


def test_add_value_with_key_exist_returns_dict_with_list() -> None:
    assert add_numeric_indexed_query_param({"a": "1"}, "a", "2") == {"a": ["1", "2"]}


def test_add_value_with_key_exist_and_is_list_returns_dict_with_list() -> None:
    assert add_numeric_indexed_query_param({"a": ["1"]}, "a", "2") == {"a": ["1", "2"]}


def test_add_value_with_key_exist_and_is_dict_returns_dict_with_dict() -> None:
    assert add_numeric_indexed_query_param({"a": {"key": "1"}}, "a", "2") == {
        "a": {"key": "1", "0": "2"}
    }


# test for "add_string_indexed_query_param" function
def test_add_string_indexed_value_without_key_exist_returns_dict_with_key_and_value() -> (
    None
):
    assert add_string_indexed_query_param({}, "a", "1", "key") == {"a": {"key": "1"}}


def test_add_string_indexed_value_with_key_exist_returns_dict_with_list() -> None:
    assert add_string_indexed_query_param({"a": "1"}, "a", "2", "key") == {
        "a": {"0": "1", "key": "2"}
    }


def test_add_string_indexed_value_with_key_exist_and_is_list_returns_dict_with_list() -> (
    None
):
    assert add_string_indexed_query_param({"a": ["1"]}, "a", "2", "key") == {
        "a": {"0": "1", "key": "2"}
    }


def test_add_string_indexed_value_with_key_exist_and_is_dict_returns_replace_key_with_dict() -> (
    None
):
    assert add_string_indexed_query_param({"a": {"key": "1"}}, "a", "2", "key") == {
        "a": {"key": "2"}
    }


def test_add_string_indexed_value_with_key_exist_and_is_dict_returns_dict_with_dict() -> (
    None
):
    assert add_string_indexed_query_param(
        {"a": {"key": "1"}}, "a", "2", "another_key"
    ) == {"a": {"key": "1", "another_key": "2"}}


# test for "find_last_numeric_index" function
def test_find_index_returns_zero_when_keys_match_but_is_simple() -> None:
    assert find_last_numeric_index("1") == 0


def test_find_index_returns_zero_when_keys_match_but_are_not_numeric() -> None:
    assert find_last_numeric_index({"b": "1"}) == 0


def test_find_index_returns_one_when_keys_match() -> None:
    assert find_last_numeric_index({"0": "1"}) == 1


def test_find_index_returns_two_when_keys_match() -> None:
    assert find_last_numeric_index({"0": "1", "1": "2"}) == 2


def test_find_index_returns_max_more_one_when_keys_match() -> None:
    assert find_last_numeric_index({"0": "1", "5": "2", "2": "3"}) == 6
