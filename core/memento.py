from abc import ABC, abstractmethod

from core.log_config import logger
from core.metaclasses import Singleton
from ui.ui_messaga_bus import Event


def get_attr(source, attr_path):
    path = attr_path.split('.')
    while path:
        p = path.pop(0)
        is_iter = p.startswith('[')
        if is_iter:
            p = p[1:-1]
            if p.isdigit():
                p = int(p)
        source = source[p] if is_iter else getattr(source, p)
    return source


def set_attr(source, attr_path, value):
    path = attr_path.split('.')
    while path:
        p = path.pop(0)
        is_iter = p.startswith('[')
        if is_iter:
            p = p[1:-1]
            if p.isdigit():
                p = int(p)
        if len(path) > 0:
            source = source[p] if is_iter else getattr(source, p)
        else:
            if is_iter:
                source[p] = value
            else:
                setattr(source, p, value)


class Memento(ABC):
    ATTRS = ['prop_path', 'old_value', 'new_value']

    def __init__(self, prop_path, restore_event=None):
        self.prop_path = prop_path
        self.restore_event = restore_event
        self.old_value = None
        self.new_value = None

    @abstractmethod
    def __call__(self, func):
        pass

    @abstractmethod
    def save(self, subject):
        pass

    @abstractmethod
    def undo(self, subject):
        pass

    @abstractmethod
    def redo(self, subject):
        pass

    def notify_subs(self):
        if self.restore_event:
            self.restore_event.emit()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return all([getattr(self, a) == get_attr(other, a) for a in self.ATTRS if hasattr(other, a)])


class ChangeMemento(Memento):

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            memento = ChangeMemento(self.prop_path, self.restore_event)
            MementoManager().save(memento)
            func(*args, **kwargs)
            MementoManager().save(memento)
        return wrapper

    def save(self, subject):
        value = get_attr(subject, self.prop_path)
        if not self.old_value:
            self.old_value = value
        else:
            self.new_value = value

    def undo(self, subject):
        set_attr(subject, self.prop_path, self.old_value)
        self.notify_subs()

    def redo(self, subject):
        set_attr(subject, self.prop_path, self.new_value)
        self.notify_subs()

    def __str__(self):
        return f'{self.prop_path} = {self.old_value} -> {self.new_value}'


class MoveMemento(Memento):

    def __call__(self, func):
        pass

    def save(self, subject):
        pass

    def undo(self, subject):
        pass

    def redo(self, subject):
        pass


class AddMemento(Memento):
    """ prop_path ends with an index """

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            MementoManager().save(AddMemento(self.prop_path, self.restore_event))
        return wrapper

    def save(self, subject):
        self.new_value = get_attr(subject, self.prop_path)

    def undo(self, subject):
        array = get_attr(subject, self.prop_path.rsplit('.', 1)[0])
        if self.new_value in array:
            array.remove(self.new_value)
        self.notify_subs()

    def redo(self, subject):
        array_path, index = self.prop_path.rsplit('.', 1)
        array = get_attr(subject, array_path)
        array.insert(int(index[1:-1]), self.new_value)
        self.notify_subs()

    def __str__(self):
        return f'{self.prop_path} added {self.new_value}'


class RemoveMemento(Memento):
    """ prop_path ends with an index """

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            MementoManager().save(RemoveMemento(self.prop_path, self.restore_event))
            func(*args, **kwargs)
        return wrapper

    def save(self, subject):
        self.old_value = get_attr(subject, self.prop_path)

    def undo(self, subject):
        array_path, index = self.prop_path.rsplit('.', 1)
        array = get_attr(subject, array_path)
        array.insert(int(index[1:-1]), self.old_value)
        self.notify_subs()

    def redo(self, subject):
        array = get_attr(subject, self.prop_path.rsplit('.', 1)[0])
        if self.old_value in array:
            array.remove(self.old_value)
        self.notify_subs()

    def __str__(self):
        return f'{self.prop_path} removed {self.old_value}'


def memento_dec(memento_cl, prop_path, rest_event):
    def decorator(func):
        def wrapper(*args, **kwargs):
            MementoManager().save(memento_cl(prop_path, rest_event))
            func(*args, **kwargs)
            MementoManager().save(memento_cl(prop_path, rest_event))
        return wrapper
    return decorator


class MementoManager(metaclass=Singleton):

    can_undo_changed = Event(bool)
    can_redo_changed = Event(bool)

    def __init__(self):
        self.logger = logger
        self.super_subject = None

    def set_subject(self, subject):
        self._index = -1
        self._history = []
        self.subject = subject
        self.update_status()

    @property
    def can_undo(self):
        return self._index >= 0

    @property
    def can_redo(self):
        return self._index < len(self._history) - 1

    def save(self, memento):
        memento.save(self.subject)
        if self.has_changes(memento):
            self._index += 1
            if self._index < len(self._history):
                self._history = self._history[:self._index]
            self._history.append(memento)
            self.update_status()
        self.logger.debug(f'SAVE {str(memento)} (ID={self._index})')

    def has_changes(self, memento):
        def check_equal(memento_1, memento_2):
            return type(memento_1) == type(memento_2) and memento_1.prop_path == memento_2.prop_path

        last_mementos = [m for m in self._history[:self._index+1][::-1] if check_equal(m, memento)]
        return not last_mementos[0] == memento if len(last_mementos) > 0 else True

    def cancel(self):
        while self.can_undo:
            self.undo()

    def undo(self):
        if not self.can_undo:
            return
        hist = self._history[self._index]
        hist.undo(self.subject)
        self._index -= 1
        self.logger.debug(f'UNDO {str(hist)}')
        self.update_status()

    def redo(self):
        if not self.can_redo:
            return
        self._index += 1
        hist = self._history[self._index]
        hist.redo(self.subject)
        self.logger.debug(f'REDO {str(hist)}')
        self.update_status()

    def update_status(self):
        self.can_undo_changed.emit(self.can_undo)
        self.can_redo_changed.emit(self.can_redo)