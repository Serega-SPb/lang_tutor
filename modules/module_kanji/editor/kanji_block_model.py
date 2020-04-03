from core.descriptors import NotifyProperty
from core.memento import ChangeMemento
from ui.ui_messaga_bus import Event


class EditorBlockModel:

    keys_changed = Event(list)
    kanji_changed = Event(object)
    update_kanji_event = Event()
    update_label_event = Event()

    def __init__(self):
        self.kanji = None
        self.prop_path = ''
        self._keys = NotifyProperty('keys', list())
        self._keys += self.keys_changed.emit
        self.update_kanji_event += self.update_label_event.emit
        self.update_kanji_event += lambda: self.kanji_changed.emit(self.kanji)

    def set_kanji(self, value):
        self.kanji = value
        self.kanji_changed.emit(value)

    @property
    def keys(self):
        return self._keys.get()

    @keys.setter
    def keys(self, value):
        self._keys.set(value)

    def set_kanji_prop(self, prop_name, value):
        @ChangeMemento(f'{self.prop_path}.{prop_name}', self.update_kanji_event)
        def memento_func():
            setattr(self.kanji, prop_name, value)

        if not self.kanji or getattr(self.kanji, prop_name) == value:
            return
        memento_func()
