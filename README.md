# qs-parser

## Install

For use this lib with poetry :
```sh
poetry add query-parser
```

For use this lib with pip :
```sh
pip install query-parser
```

## Usage

```python
from query_parser.parser import parse_query_string

print(parse_query_string("a=1&b=2&c=3&b[]=4&b[]=5&b[other]=6"))
# {'a': '1', 'b': {'0': '2', '1': '4', '2': '5', 'other': '6'}, 'c': '3'}
```
