from qs_parser.parser import Parser


class TestParser:
    def test_parse_query_string_return_dict(self):
        query_string = (
            "page=1&price[min]=100&price[max]=200&sort[]=price&sort[]=-created"
        )
        parser = Parser(query_string)
        assert parser.parse() == {
            "page": "1",
            "price": {"min": "100", "max": "200"},
            "sort": ["price", "-created"],
        }
