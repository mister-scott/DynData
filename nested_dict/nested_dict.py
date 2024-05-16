from collections import defaultdict

class NestedDict(defaultdict):
    def __init__(self):
        super().__init__(NestedDict)

    def asdict(self):
        def convert_to_dict(d):
            if isinstance(d, NestedDict):
                return {k: convert_to_dict(v) for k, v in d.items()}
            return d

        return convert_to_dict(self)

    def __dict__(self):
        return self.asdict()