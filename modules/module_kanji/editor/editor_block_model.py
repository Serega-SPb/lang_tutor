from core.descriptors import NotifyProperty
from core.memento import ChangeMemento, AddMemento, RemoveMemento
from ui.ui_messaga_bus import Event


class EditorBlockModel:

    quest_type_changed = Event(str)
    quest_types_changed = Event(list)
    keys_changed = Event(list)
    kanjis_changed = Event(list)
    current_kanji_changed = Event(object)
    current_kanji_index_changed = Event(int)
    update_label_event = Event()
    update_quest_type_event = Event()
    update_kanji_event = Event()
    update_kanjis_event = Event()

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
        self.update_kanji_event += lambda: self.current_kanji_changed.emit(self.current_kanji)
        self.update_quest_type_event += lambda: self.quest_type_changed.emit(self.quest_type)
        self.update_kanjis_event += self.update_kanjis
        self.data_index = -1

    @property
    def quest_type(self):
        return self.sc_data.quest_type

    @quest_type.setter
    def quest_type(self, value):

        @ChangeMemento(self.get_prop_path('quest_type'), self.update_quest_type_event)
        def wrapper():
            self.sc_data.quest_type = value
            self.quest_type_changed.emit(value)

        if self.sc_data.quest_type == value:
            return
        wrapper()

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
        prop_path = f"{self.get_prop_path('data')}.[{len(self.sc_data.data)}]"
        AddMemento(prop_path, self.update_kanjis_event)(self.sc_data.data.append)(value)
        self.kanjis_changed.emit(self.kanjis)
        self.current_kanji_index = len(self.kanjis) - 1

    def remove_kanji(self, value):
        prop_path = f"{self.get_prop_path('data')}.[{self.sc_data.data.index(value)}]"
        RemoveMemento(prop_path, self.update_kanjis_event)(self.sc_data.data.remove)(value)
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

    def update_quest_type(self):
        self.quest_type_changed.emit(self.quest_type)

    def update_kanjis(self):
        if self.current_kanji_index > len(self.kanjis) - 1:
            self.current_kanji_index = -1
        self.kanjis_changed.emit(self.kanjis)

    BASE_PROP_PATH = 'scenario_data'

    def get_prop_path(self, prop_name):
        return f'{self.BASE_PROP_PATH}.[{self.data_index}].{prop_name}'

    def get_kanji_prop_path(self, prop_name):
        return f'{self.BASE_PROP_PATH}.[{self.data_index}].data.[{self.current_kanji_index}].{prop_name}'

    def set_data_index(self, value):
        self.data_index = value

    def set_kanji_index(self, value):
        self._current_kanji_index.set(value)

    def set_kanji_prop(self, prop_name, value):
        @ChangeMemento(self.get_kanji_prop_path(prop_name), self.update_kanji_event)
        def memento_func():
            setattr(self.current_kanji, prop_name, value)

        if not self.current_kanji or getattr(self.current_kanji, prop_name) == value:
            return
        memento_func()
