

class Word:
    __slots__ = ('spelling', 'reading', 'translate')

    def __init__(self, spelling, reading, translate):
        self.spelling = spelling
        self.reading = reading
        self.translate = translate

    def __eq__(self, other):
        if not isinstance(other, Word):
            return False
        return all([getattr(other, attr) == getattr(self, attr) for attr in self.__slots__])
