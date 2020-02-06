from .descriptors import NotifyProperty
from ui.ui_messaga_bus import Event


class Module:
    __slots__ = ('name', '_is_enabled', 'init', 'enable_changed')

    def __init__(self, name, **kwargs):
        self._is_enabled = NotifyProperty('is_enabled')

        self.name = name
        self.is_enabled = kwargs.get('is_enabled') or False
        self.init = kwargs.get('init') or None

        self.enable_changed = Event(bool)
        self._is_enabled += self.enable_changed.emit

    @property
    def is_enabled(self):
        return self._is_enabled.get()

    @is_enabled.setter
    def is_enabled(self, value):
        self._is_enabled.set(value)
