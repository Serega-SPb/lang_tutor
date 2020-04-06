from core.memento import ChangeMemento, get_attr, set_attr
from ui.ui_messaga_bus import Event


class EditorBlockModel:
    
    number_changed = Event(object)
    update_number_event = Event()
    update_label_event = Event()

    def __init__(self):
        self.number = None
        self.prop_path = ''
        self.update_number_event += self.update_label_event.emit
        self.update_number_event += lambda: self.number_changed.emit(self.number)

    def set_number(self, value):
        self.number = value
        self.number_changed.emit(value)

    def set_number_prop(self, prop_name, value):
        @ChangeMemento(f'{self.prop_path}.{prop_name}', self.update_number_event)
        def memento_func():
            set_attr(self.number, prop_name, value)

        if not self.number or get_attr(self.number, prop_name) == value:
            return
        memento_func()
