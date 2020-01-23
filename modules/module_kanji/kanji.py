
class Kanji:
    __slots__ = ('key', 'value', 'dash_count', 'on', 'kun', 'translate')

    def __init__(self, key):
        self.key = key
        self.value = ''
        self.dash_count = 0
        self.on = self.kun = self.translate = []


class KanjiKey(Kanji):
    __slots__ = ['number', 'has_reduction', 'reductions']

    def __init__(self, number):
        super().__init__(self)
        self.__slots__.extend(super().__slots__)
        self.number = number
        self.has_reduction = False
        self.reductions = []
