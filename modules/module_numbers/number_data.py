from .number_converter import convert as convert_func


class NumberData:
    __slots__ = ('is_range', 'value', 'value_range', 'step')

    def __init__(self, is_range, value, value_range, step):
        self.is_range = is_range
        self.value = value
        self.step = step
        self.value_range = value_range

    def __eq__(self, other):
        if not isinstance(other, NumberData):
            return False
        return all([getattr(other, attr) == getattr(self, attr) for attr in self.__slots__])

    def get_numbers(self):
        return [convert_func(num) for num in range(self.value_range[0], self.value_range[-1] + 1, self.step)] \
            if self.is_range else [convert_func(self.value)]
