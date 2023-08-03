from qs_parser.parser import QueryKeyDetail
from qs_parser.query_params import QueryParam
from qs_parser.query_params import QueryParams


class TestQueryParams:
    def test_add_simple_key(self):
        instance = QueryParams()
        instance.add(QueryKeyDetail.parse_key("key"), "value")

        assert isinstance(instance.params, dict)
        assert len(instance.params) == 1
        assert instance.params["key"].key == "key"
        assert isinstance(instance.params["key"], QueryParam)

    def test_add_simple_key_with_index(self):
        instance = QueryParams()
        instance.add(QueryKeyDetail.parse_key("key[0]"), "value")

        assert isinstance(instance.params, dict)
        assert len(instance.params) == 1
        assert instance.params["key"].key == "key"
        assert isinstance(instance.params["key"], QueryParam)

    def test_add_simple_key_with_push(self):
        instance = QueryParams()
        instance.add(QueryKeyDetail.parse_key("key[]"), "value")

        assert isinstance(instance.params, dict)
        assert len(instance.params) == 1
        assert instance.params["key"].key == "key"
        assert isinstance(instance.params["key"], QueryParam)

    def test_add_simple_key_with_string_index(self):
        instance = QueryParams()
        instance.add(QueryKeyDetail.parse_key("key[first]"), "value")

        assert isinstance(instance.params, dict)
        assert len(instance.params) == 1
        assert instance.params["key"].key == "key"
        assert isinstance(instance.params["key"], QueryParam)

    def test_add_multiple_keys_return_dict(self):
        instance = QueryParams()
        instance.add(QueryKeyDetail.parse_key("page"), "1")
        instance.add(QueryKeyDetail.parse_key("price[min]"), "100")
        instance.add(QueryKeyDetail.parse_key("price[max]"), "200")
        instance.add(QueryKeyDetail.parse_key("sort[]"), "+price")
        instance.add(QueryKeyDetail.parse_key("sort[]"), "-created")

        assert isinstance(instance.params, dict)
        assert len(instance.params) == 3
        assert instance.params["page"].key == "page"
        assert instance.params["price"].key == "price"
        assert instance.params["sort"].key == "sort"

        assert instance.to_dict() == {
            "page": "1",
            "price": {"min": "100", "max": "200"},
            "sort": ["+price", "-created"],
        }
