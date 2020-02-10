
class Kanji:
    __slots__ = ('key', 'value', 'dash_count', 'on', 'kun', 'translate')

    INIT_ATTRS = ['key', 'value', 'dash_count']

    def __init__(self, key, value, dash_count):
        self.key = key
        self.value = value
        self.dash_count = dash_count
        self.on = []
        self.kun = []
        self.translate = []

    def __eq__(self, other):
        if not isinstance(other, Kanji):
            return False
        if other.value != self.value:
            return False
        return True


class KanjiKey(Kanji):
    __slots__ = ['number', 'has_reduction', 'reductions']

    INIT_ATTRS = ['number', 'value', 'dash_count']

    def __init__(self, number, value, dash_count):
        super().__init__(self, value, dash_count)
        self.__slots__.extend(super().__slots__)
        self.number = int(number)
        self.has_reduction = False
        self.reductions = []
