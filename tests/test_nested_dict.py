import unittest
from nested_dict import NestedDict

class TestNestedDict(unittest.TestCase):
    def test_nested_dict(self):
        nested = NestedDict()
        nested['a']['b']['c'] = 'nonsense'
        nested['a']['g'] = 'more of the same'

        self.assertEqual(nested['a']['b']['c'], 'nonsense')
        self.assertEqual(nested['a']['g'], 'more of the same')
        self.assertEqual(nested.asdict(), {'a': {'b': {'c': 'nonsense'}, 'g': 'more of the same'}})

if __name__ == '__main__':
    unittest.main()