from core.memento import ChangeMemento
from ui.ui_messaga_bus import Event


class EditorBlockModel:

    word_changed = Event(object)
    update_word_event = Event()
    update_label_event = Event()

    def __init__(self):
        self.word = None
        self.prop_path = ''
        self.update_word_event += self.update_label_event.emit
        self.update_word_event += lambda: self.word_changed.emit(self.word)

    def set_word(self, value):
        self.word = value
        self.word_changed.emit(value)

    def set_word_prop(self, prop_name, value):
        @ChangeMemento(f'{self.prop_path}.{prop_name}', self.update_word_event)
        def memento_func():
            setattr(self.word, prop_name, value)

        if not self.word or getattr(self.word, prop_name) == value:
            return
        memento_func()
