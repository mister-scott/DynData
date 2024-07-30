# dynData

A library of flexible datatypes for use in any old operation.


## Installation

You can install the package using pip:

`pip install git+https://github.com/mister-scott/dynData.git`

## nested_dict

A nested dictionary class for Python.

## DynamicClass

A class type which can construct its parameters from a dictionary.


## Usage

```python
from nested_dict import NestedDict

nested = NestedDict()
nested['a']['b']['c'] = 'nonsense'
nested['a']['g'] = 'more of the same'

print(nested)
print(nested.asdict())
```
