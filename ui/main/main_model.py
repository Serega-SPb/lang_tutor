from core.data_loader import DataLoader
from core.descriptors import NotifyProperty
from ui.ui_messaga_bus import Event


class MainModel:

    modules_changed = Event()
    scenarios_changed = Event()

    def __init__(self):
        self.data_loader = DataLoader()
        self._editor_mode = NotifyProperty('editor_mode', 0)

    @property
    def modules(self):
        return self.data_loader.modules.values()

    @property
    def scenarios(self):
        return self.data_loader.scenarios.values()

    @property
    def editor_mode(self):
        return self._editor_mode.get()

    @editor_mode.setter
    def editor_mode(self, value):
        self._editor_mode.set(value)
