import pytest

from qs_parser.query_params import QueryParam
from qs_parser.query_params import QueryParamValue


class TestQueryParam:
    def test_init_object_has_valid_properties(self):
        instance = QueryParam("key")
        assert instance.key == "key"
        assert instance.values is None
        assert instance.last_index == 0
        assert instance.has_associated_values is False

    def test_add_value_keep_as_a_simple_value(self):
        instance = QueryParam("key")
        instance.add_value("first")

        assert isinstance(instance.values, QueryParamValue)
        assert instance.values.index == 0
        assert instance.values.value == "first"

    def test_add_simple_value_without_list_creates_list_of_values(self):
        instance = QueryParam("key")
        instance.add_value("first")
        instance.add_value("second")

        assert isinstance(instance.values, list)
        assert len(instance.values) == 2
        assert instance.values[0].index == 0
        assert instance.values[0].value == "first"
        assert instance.values[1].index == 1
        assert instance.values[1].value == "second"

    def test_add_simple_value_in_list_append_value(self):
        instance = QueryParam("key")
        instance.add_value("first", force_append=True)
        instance.add_value("second")

        assert isinstance(instance.values, list)
        assert len(instance.values) == 2
        assert instance.values[0].index == 0
        assert instance.values[0].value == "first"
        assert instance.values[1].index == 1
        assert instance.values[1].value == "second"

    def test_add_associative_value_creates_dict(self):
        instance = QueryParam("key")
        instance.add_associated_value("first", "value")

        assert isinstance(instance.values, list)
        assert len(instance.values) == 1
        assert instance.values[0].index == "first"
        assert instance.values[0].value == "value"
        assert instance.has_associated_values is True

    def test_add_forced_value_creates_list_of_values(self):
        instance = QueryParam("key")
        instance.add_value("first", force_append=True)

        assert isinstance(instance.values, list)
        assert len(instance.values) == 1
        assert instance.values[0].index == 0

    def test_add_numeric_associative_value_updates_last_index(self):
        instance = QueryParam("key")
        instance.add_associated_value("5", "value")

        assert isinstance(instance.values, list)
        assert len(instance.values) == 1
        assert instance.values[0].index == 5
        assert instance.values[0].value == "value"
        assert instance.last_index == 6

    def test_add_associative_value_after_simple_value_append_to_list(self):
        instance = QueryParam("key")
        instance.add_value("first")
        instance.add_associated_value("second", "value")

        assert isinstance(instance.values, list)
        assert len(instance.values) == 2
        assert instance.values[0].index == 0
        assert instance.values[0].value == "first"
        assert instance.values[1].index == "second"
        assert instance.values[1].value == "value"

    def test_raise_value_error_when_query_param_has_no_values(self):
        instance = QueryParam("key")

        with pytest.raises(ValueError) as exc_info:
            instance.to_dict()

        assert str(exc_info.value) == "QueryParam has no values"

    def test_instance_has_simple_value(self):
        instance = QueryParam("key")
        instance.add_value("first")

        assert {"key": "first"} == instance.to_dict()

    def test_instance_has_list_of_values(self):
        instance = QueryParam("key")
        instance.add_value("first")
        instance.add_value("second")

        assert {"key": ["first", "second"]} == instance.to_dict()

    def test_instance_has_associative_values(self):
        instance = QueryParam("key")
        instance.add_associated_value("first", "value")
        instance.add_associated_value("second", "value")

        assert {"key": {"first": "value", "second": "value"}} == instance.to_dict()

    def test_combine_index_and_associative_values(self):
        instance = QueryParam("key")
        instance.add_value("first")
        instance.add_associated_value("second", "value")
        instance.add_associated_value("10", "ben")
        instance.add_value("eleven")
        instance.add_associated_value("msg", "twelve")

        assert {
            "key": {
                "0": "first",
                "second": "value",
                "10": "ben",
                "11": "eleven",
                "msg": "twelve",
            }
        } == instance.to_dict()
