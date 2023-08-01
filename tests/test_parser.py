from qs_parser.parser import parse_query_string


def test_parser_with_empty_string_returns_empty_dict() -> None:
    assert parse_query_string("") == {}
