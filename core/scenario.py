
class ScenarioData:
    __slots__ = ('module_name', 'quest_type', 'lazy_init', '_data')

    def __init__(self, mod_name, quest_type, lazy_init):
        self.module_name = mod_name
        self.quest_type = quest_type
        self.lazy_init = lazy_init
        self._data = None

    @classmethod
    def empty_init(cls, mod_name):
        ins = cls(mod_name, '', None)
        ins._data = []
        return ins

    @property
    def data(self):
        if self._data is None:
            self._data = self.lazy_init()
        return self._data


class Scenario:
    __slots__ = ('name', 'required_modules', 'scenario_data')

    def __init__(self, name, **kwargs):
        self.name = name
        self.required_modules = kwargs.get('required_modules', list())
        self.scenario_data = kwargs.get('scenario_data', list())
