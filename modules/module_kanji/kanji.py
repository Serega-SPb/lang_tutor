
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


class KanjiKey:
    __slots__ = ['number', 'value', 'name', 'has_reduction', 'reductions']

    INIT_ATTRS = ['number', 'value', 'name']

    def __init__(self, number, value, name):
        self.number = int(number)
        self.value = value
        self.name = name
        self.has_reduction = False
        self.reductions = []
