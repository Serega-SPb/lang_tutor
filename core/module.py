import importlib

from .decorators import try_except_wrapper
from ui.ui_messaga_bus import Event


class Module:
    __slots__ = ('name', '_is_enabled', '_init', 'enable_changed')

    get_mod_dir = None

    def __init__(self, name, **kwargs):
        self.enable_changed = Event(bool)

        self.name = name
        self._is_enabled = kwargs.get('is_enabled') or False
        self._init = kwargs.get('init') or None

        self.enable_changed += self.on_enabled_changed

    @property
    def is_enabled(self):
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, value):
        self._is_enabled = value
        self.enable_changed.emit(value)

    @property
    def init(self):
        return self._init

    @try_except_wrapper
    def activate_module(self):
        self._init = importlib.import_module(f'{self.get_mod_dir()}.{self.name}.init').Init()
        self._is_enabled = True

    def deactivate_module(self):
        self._is_enabled = False
        self._init = None

    def on_enabled_changed(self, value):
        self.activate_module() if value \
            else self.deactivate_module()
