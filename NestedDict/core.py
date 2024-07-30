import numpy as np

class NestedDict:
    def __init__(self, data_dict=None):
        self._data = {}
        if data_dict:
            self.update(data_dict)

    def update(self, data_dict):
        for key, value in data_dict.items():
            self[key] = value

    def __getattr__(self, name):
        if name.startswith('_'):
            return super().__getattribute__(name)
        if name not in self._data:
            self._data[name] = NestedDict()
        return self._data[name]

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self[name] = value

    def __getitem__(self, key):
        if key not in self._data:
            self._data[key] = NestedDict()
        return self._data[key]

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            self._data[key] = NestedDict(value)
        else:
            self._data[key] = value

    def asdict(self):
        def convert_to_dict(d):
            if isinstance(d, NestedDict):
                return {k: convert_to_dict(v) for k, v in d._data.items()}
            return d
        return convert_to_dict(self)

    def __repr__(self):
        return repr(self.asdict())

    def print_structure(self, with_values=True, indent=0):
        for key, value in self._data.items():
            print('  ' * indent + str(key), end='')
            if isinstance(value, NestedDict):
                print(':')
                value.print_structure(with_values, indent + 1)
            elif with_values:
                print(f': {value}')
            else:
                print()

    def __dir__(self):
        return list(self._data.keys()) + list(self.__dict__.keys())

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __contains__(self, key):
        return key in self._data

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def to_numpy(self, fill_value=None):
        """
        Transform the nested data into a multi-dimensional numpy array.
        
        Args:
        fill_value: Value to use for filling 'holes' in the data structure.
                    If None, the method will raise an error for irregular structures.
        
        Returns:
        np.ndarray: A numpy array representing the nested structure.
        """
        def get_shape(d):
            if not isinstance(d, NestedDict):
                return ()
            shapes = [get_shape(v) for v in d._data.values()]
            if not shapes:
                return (0,)
            if len(set(shapes)) > 1:
                if fill_value is None:
                    raise ValueError("Irregular nested structure. Provide a fill_value to handle this.")
                max_shape = tuple(max(s) for s in zip(*shapes))
                return (len(d._data),) + max_shape
            return (len(d._data),) + shapes[0]

        def fill_array(arr, d, index):
            if not isinstance(d, NestedDict):
                arr[index] = d
                return
            for i, (k, v) in enumerate(d._data.items()):
                new_index = index + (i,)
                if isinstance(v, NestedDict):
                    fill_array(arr, v, new_index)
                else:
                    arr[new_index] = v

        shape = get_shape(self)
        if fill_value is not None:
            arr = np.full(shape, fill_value)
        else:
            arr = np.empty(shape)
        fill_array(arr, self, ())
        return arr
    
    def to_labeled_numpy(self, fill_value=None):
        """
        Transform the nested data into a multi-dimensional numpy array
        while preserving axis labels.
        
        Args:
        fill_value: Value to use for filling 'holes' in the data structure.
                    If None, the method will raise an error for irregular structures.
        
        Returns:
        tuple: (np.ndarray, list of axis labels)
            - np.ndarray: A numpy array representing the nested structure.
            - list: A list of dictionaries, each containing the labels for an axis.
        """
        def get_shape_and_labels(d):
            if not isinstance(d, NestedDict):
                return (), []
            shapes_and_labels = [get_shape_and_labels(v) for v in d._data.values()]
            shapes, labels = zip(*shapes_and_labels) if shapes_and_labels else ((), [])
            
            if len(set(shapes)) > 1:
                if fill_value is None:
                    raise ValueError("Irregular nested structure. Provide a fill_value to handle this.")
                max_shape = tuple(max(s) for s in zip(*shapes))
                current_shape = (len(d._data),) + max_shape
                current_labels = [list(d._data.keys())] + [
                    list(set().union(*[l[i] for l in labels if i < len(l)]))
                    for i in range(len(max_shape))
                ]
            else:
                current_shape = (len(d._data),) + shapes[0] if shapes else (len(d._data),)
                current_labels = [list(d._data.keys())] + (labels[0] if labels else [])
            
            return current_shape, current_labels

        def fill_array(arr, d, index, label_indices):
            if not isinstance(d, NestedDict):
                arr[tuple(label_indices)] = d
                return
            for i, (k, v) in enumerate(d._data.items()):
                new_index = index + (i,)
                new_label_indices = label_indices + [axis_labels[len(new_index)-1].index(k)]
                if isinstance(v, NestedDict):
                    fill_array(arr, v, new_index, new_label_indices)
                else:
                    arr[tuple(new_label_indices)] = v

        shape, axis_labels = get_shape_and_labels(self)
        if fill_value is not None:
            arr = np.full(shape, fill_value)
        else:
            arr = np.empty(shape)
        fill_array(arr, self, (), [])
        
        # Convert axis labels to dictionaries
        axis_label_dicts = [
            {label: i for i, label in enumerate(axis)}
            for axis in axis_labels
        ]
        
        return arr, axis_label_dicts