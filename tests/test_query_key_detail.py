from qs_parser.parser import QueryKeyDetail


class TestQueryKeyDetail:
    def test_simple_key_returns_key(self):
        instance = QueryKeyDetail.parse_key("key")

        assert instance.key == "key"
        assert instance.index is None

    def test_key_with_index_returns_key_and_index(self):
        instance = QueryKeyDetail.parse_key("key[0]")

        assert instance.key == "key"
        assert instance.index == "0"

    def test_key_with_associative_index_returns_key_and_index(self):
        instance = QueryKeyDetail.parse_key("key[first]")

        assert instance.key == "key"
        assert instance.index == "first"

    def test_key_with_brackets_returns_key(self):
        instance = QueryKeyDetail.parse_key("key[]")

        assert instance.key == "key"
        assert instance.index == -1
