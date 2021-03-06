from .module_manager import get_module_init
from ui.ui_messaga_bus import Event


class Module:
    __slots__ = ('name', '_is_enabled', '_init', 'enable_changed')

    def __init__(self, name, **kwargs):
        self.enable_changed = Event(str, bool)
        self.enable_changed += self.on_enabled_changed
        self._is_enabled = False
        self._init = None

        self.name = name
        self.is_enabled = kwargs.get('is_enabled', True)

    @property
    def ui_name(self):
        return self.init.get_name() if self.init else self.name

    @property
    def is_enabled(self):
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, value):
        if self._is_enabled == value:
            return
        self._is_enabled = value
        self.enable_changed.emit(self.name, value)

    @property
    def init(self):
        return self._init

    def activate_module(self):
        self._init = get_module_init(self.name)
        self._is_enabled = self._init is not None

    def deactivate_module(self):
        self._is_enabled = False
        self._init = None

    def on_enabled_changed(self, name, value):
        self.activate_module() if value \
            else self.deactivate_module()
