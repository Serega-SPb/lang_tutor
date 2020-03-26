from core.descriptors import NotifyProperty
from core.memento import AddMemento, RemoveMemento
from ui.ui_messaga_bus import Event


class EditorModel:

    scenario_changed = Event(object)
    scenario_name_changed = Event(str)
    can_undo_changed = Event(bool)
    can_redo_changed = Event(bool)
    blocks_changed = Event(list)
    block_widget_changed = Event(object)
    update_scenario_event = Event()

    def __init__(self):
        self._scenario = NotifyProperty('scenario')
        self._scenario += self.scenario_changed.emit
        self._can_undo = NotifyProperty('can_undo', False)
        self._can_undo += self.can_undo_changed.emit
        self._can_redo = NotifyProperty('can_redo', False)
        self._can_redo += self.can_redo_changed.emit
        self._blocks = NotifyProperty('blocks', list())
        self._blocks += self.blocks_changed.emit
        self._block_widget = NotifyProperty('_block_widget')
        self._block_widget += self.block_widget_changed.emit
        self.update_scenario_event += self.update_scenario

    @property
    def scenario(self):
        return self._scenario.get()

    @scenario.setter
    def scenario(self, value):
        self._scenario.set(value)

    @property
    def can_undo(self):
        return self._can_undo.get()

    @can_undo.setter
    def can_undo(self, value):
        self._can_undo.set(value)

    @property
    def can_redo(self):
        return self._can_redo.get()

    @can_redo.setter
    def can_redo(self, value):
        self._can_redo.set(value)

    @property
    def blocks(self):
        return self._blocks.get()

    @blocks.setter
    def blocks(self, value):
        self._blocks.set(value)

    @property
    def block_widget(self):
        return self._block_widget.get()

    @block_widget.setter
    def block_widget(self, value):
        self._block_widget.set(value)

    def append_scenario_data(self, sc_data):
        prop_path = f'scenario_data.[{len(self.scenario.scenario_data)}]'
        AddMemento(prop_path,self.update_scenario_event)\
            (self.scenario.scenario_data.append)(sc_data)
        self.scenario_changed.emit(self.scenario)

    def remove_scenario_data(self, sc_data):
        prop_path = f'scenario_data.[{self.scenario.scenario_data.index(sc_data)}]'
        RemoveMemento(prop_path, self.update_scenario_event)\
            (self.scenario.scenario_data.remove)(sc_data)
        self.scenario_changed.emit(self.scenario)

    def update_scenario(self):
        self.scenario_changed.emit(self.scenario)

    def update_scenario_name(self):
        self.scenario_name_changed.emit(self.scenario.name)
