from core.descriptors import NotifyProperty
from core.memento import ChangeMemento, AddMemento, RemoveMemento
from ui.ui_messaga_bus import Event


class EditorBlockModel:

    quest_type_changed = Event(str)
    quest_types_changed = Event(list)
    words_changed = Event(list)
    current_word_changed = Event(object)
    current_word_index_changed = Event(int)
    update_label_event = Event()
    update_quest_type_event = Event()
    update_word_event = Event()
    update_words_event = Event()

    def __init__(self):
        self.sc_data = None
        self._quest_types = NotifyProperty('quest_types', list())
        self._quest_types += self.quest_types_changed.emit
        self._current_word = NotifyProperty('current_word')
        self._current_word += self.current_word_changed.emit
        self._current_word_index = NotifyProperty('current_word_index', -1)
        self._current_word_index += self.current_word_index_changed.emit
        self.update_word_event += lambda: self.current_word_changed.emit(self.current_word)
        self.update_quest_type_event += lambda: self.quest_type_changed.emit(self.quest_type)
        self.update_words_event += self.update_words
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
    def words(self):
        return self.sc_data.data

    def append_word(self, value):
        prop_path = f"{self.get_prop_path('data')}.[{len(self.sc_data.data)}]"
        AddMemento(prop_path, self.update_words_event)(self.sc_data.data.append)(value)
        self.words_changed.emit(self.words)
        self.current_word_index = len(self.words) - 1

    def remove_word(self, value):
        prop_path = f"{self.get_prop_path('data')}.[{self.sc_data.data.index(value)}]"
        RemoveMemento(prop_path, self.update_words_event)(self.sc_data.data.remove)(value)
        self.words_changed.emit(self.words)
        self.current_word_index = -1

    @property
    def current_word(self):
        return self._current_word.get()

    @current_word.setter
    def current_word(self, value):
        self._current_word.set(value)

    @property
    def current_word_index(self):
        return self._current_word_index.get()

    @current_word_index.setter
    def current_word_index(self, value):
        self._current_word_index.set(value)

    def update_quest_type(self):
        self.quest_type_changed.emit(self.quest_type)

    def update_words(self):
        if self.current_word_index > len(self.words) - 1:
            self.current_word_index = -1
        self.words_changed.emit(self.words)

    BASE_PROP_PATH = 'scenario_data'

    def get_prop_path(self, prop_name):
        return f'{self.BASE_PROP_PATH}.[{self.data_index}].{prop_name}'

    def get_word_prop_path(self, prop_name):
        return f'{self.BASE_PROP_PATH}.[{self.data_index}].data.[{self.current_word_index}].{prop_name}'

    def set_data_index(self, value):
        self.data_index = value

    def set_word_index(self, value):
        self._current_word_index.set(value)

    def set_word_prop(self, prop_name, value):
        @ChangeMemento(self.get_word_prop_path(prop_name), self.update_word_event)
        def memento_func():
            setattr(self.current_word, prop_name, value)

        if not self.current_word or getattr(self.current_word, prop_name) == value:
            return
        memento_func()
