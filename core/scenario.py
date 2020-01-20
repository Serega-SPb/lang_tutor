class Scenario:
    __slots__ = ('name', 'required_modules', 'data')

    def __init__(self, name, **kwargs):
        self.name = name
        for s in self.__slots__:
            if s in kwargs.keys():
                setattr(self, s, kwargs[s])
