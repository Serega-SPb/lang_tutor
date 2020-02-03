class Scenario:
    __slots__ = ('name', 'required_modules', '_data', 'lazy_init')

    def __init__(self, name, **kwargs):
        self.name = name
        self.required_modules = kwargs.get('required_modules', list())
        self.lazy_init = kwargs.get('lazies', dict())
        self._data = None

    def get_data(self):
        if self._data is None:
            self.__execute_init()
        return self._data

    def __execute_init(self):
        self._data = {}
        for mod, init in self.lazy_init.items():
            self._data[mod] = init()
