from core.descriptors import NotifyProperty
from ui.ui_messaga_bus import Event


class EditorBlockModel:

    quest_type_changed = Event(str)
    quest_types_changed = Event(list)
    keys_changed = Event(list)
    kanjis_changed = Event(list)
    current_kanji_changed = Event(object)
    current_kanji_index_changed = Event(int)
    update_label_event = Event()

    def __init__(self):
        self.sc_data = None
        self._quest_types = NotifyProperty('quest_types', list())
        self._quest_types += self.quest_types_changed.emit
        self._keys = NotifyProperty('keys', list())
        self._keys += self.keys_changed.emit
        self._current_kanji = NotifyProperty('current_kanji')
        self._current_kanji += self.current_kanji_changed.emit
        self._current_kanji_index = NotifyProperty('current_kanji_index', -1)
        self._current_kanji_index += self.current_kanji_index_changed.emit

    @property
    def quest_type(self):
        return self.sc_data.quest_type

    @quest_type.setter
    def quest_type(self, value):
        if self.sc_data.quest_type == value:
            return
        self.sc_data.quest_type = value
        self.quest_type_changed.emit(value)

    @property
    def quest_types(self):
        return self._quest_types.get()

    @quest_types.setter
    def quest_types(self, value):
        self._quest_types.set(value)

    @property
    def keys(self):
        return self._keys.get()

    @keys.setter
    def keys(self, value):
        self._keys.set(value)

    @property
    def kanjis(self):
        return self.sc_data.data

    def append_kanji(self, value):
        self.sc_data.data.append(value)
        self.kanjis_changed.emit(self.kanjis)
        self.current_kanji_index = len(self.kanjis) - 1

    def remove_kanji(self, value):
        self.sc_data.data.remove(value)
        self.kanjis_changed.emit(self.kanjis)
        self.current_kanji_index = -1

    @property
    def current_kanji(self):
        return self._current_kanji.get()

    @current_kanji.setter
    def current_kanji(self, value):
        self._current_kanji.set(value)

    @property
    def current_kanji_index(self):
        return self._current_kanji_index.get()

    @current_kanji_index.setter
    def current_kanji_index(self, value):
        self._current_kanji_index.set(value)
