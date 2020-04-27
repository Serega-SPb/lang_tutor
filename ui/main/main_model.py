from core.data_loader import DataLoader
from core.descriptors import NotifyProperty
from ui.ui_messaga_bus import Event


class MainModel:

    modules_changed = Event(list)
    scenarios_changed = Event(list)
    locales_changed = Event(list)

    is_applied_settings_changed = Event(bool)
    is_options_enabled_changed = Event(bool)

    current_locale_changed = Event(str)
    modules_dir_changed = Event(str)
    scenarios_dir_changed = Event(str)

    def __init__(self):
        self.data_loader = DataLoader()
        self._is_options_enabled = NotifyProperty('is_options_enabled', False)
        self._is_options_enabled += self.is_options_enabled_changed.emit
        self._editor_mode = NotifyProperty('editor_mode', 0)

        self.locales = []
        self._is_applied_settings = NotifyProperty('is_applied_settings', True)
        self._is_applied_settings += self.is_applied_settings_changed.emit
        self._current_locale = NotifyProperty('current_locale')
        self._current_locale += self.current_locale_changed.emit
        self._modules_dir = ''
        self._scenarios_dir = ''

    @property
    def is_debug(self):
        return self.data_loader.is_debug

    @property
    def modules(self):
        return self.data_loader.modules.values()

    @property
    def scenarios(self):
        return self.data_loader.scenarios.values()

    def update_modules(self):
        self.modules_changed.emit(self.modules)

    def update_scenarios(self):
        self.scenarios_changed.emit(self.scenarios)

    @property
    def is_options_enabled(self):
        return self._is_options_enabled.get()

    @is_options_enabled.setter
    def is_options_enabled(self, value):
        self._is_options_enabled.set(value)

    @property
    def editor_mode(self):
        return self._editor_mode.get()

    @editor_mode.setter
    def editor_mode(self, value):
        self._editor_mode.set(value)

    def set_locales(self, values):
        self.locales = values
        self.locales_changed.emit(values)

    @property
    def is_applied_settings(self):
        return self._is_applied_settings.get()

    @is_applied_settings.setter
    def is_applied_settings(self, value):
        self._is_applied_settings.set(value)

    @property
    def current_locale(self):
        return self._current_locale.get()

    @current_locale.setter
    def current_locale(self, value):
        self._current_locale.set(value)
        self.is_applied_settings = False

    @property
    def modules_dir(self):
        return self._modules_dir

    @modules_dir.setter
    def modules_dir(self, value):
        self._modules_dir = value
        self.modules_dir_changed.emit(value)
        self.is_applied_settings = False

    @property
    def scenarios_dir(self):
        return self._scenarios_dir

    @scenarios_dir.setter
    def scenarios_dir(self, value):
        self._scenarios_dir = value
        self.is_applied_settings = False
        self.scenarios_dir_changed.emit(value)
