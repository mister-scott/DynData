# nested_dict

A nested dictionary class for Python.

## Installation

You can install the package using pip:

`pip install git+https://github.com/yourusername/nested_dict.git`


## Usage

```python
from nested_dict import NestedDict

nested = NestedDict()
nested['a']['b']['c'] = 'nonsense'
nested['a']['g'] = 'more of the same'

print(nested)
print(nested.asdict())
```
