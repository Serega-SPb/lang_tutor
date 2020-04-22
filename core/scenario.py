from core.descriptors import NotifyProperty
from ui.ui_messaga_bus import Event


class QuestType:

    def __init__(self, value, ui_func):
        self.value = value
        self.ui_func = ui_func

    @property
    def ui(self):
        return self.ui_func(self.value)

    def __eq__(self, other):
        return other.value == self.value if isinstance(other, QuestType) else False


class ScenarioData:
    __slots__ = ('module', '_quest_type', 'lazy_init', '_data', 'quest_type_changed')

    def __init__(self, mod, quest_type, lazy_init):
        self.module = mod
        self.quest_type_changed = Event(str)
        func = self.module.init.translate_local if self.module.init else lambda x: quest_type
        qt = QuestType(quest_type, func)
        self._quest_type = NotifyProperty('quest_type', qt)
        self._quest_type += self.quest_type_changed.emit
        self.lazy_init = lazy_init
        self._data = None

    @classmethod
    def empty_init(cls, module):
        ins = cls(module, module.init.get_question_types()[0], None)
        ins._data = []
        return ins

    @property
    def quest_type(self):
        return self._quest_type.get()

    @quest_type.setter
    def quest_type(self, value):
        self._quest_type.set(value)

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
