from core.descriptors import NotifyProperty
from core.memento import AddMemento, RemoveMemento
from ui.ui_messaga_bus import Event


class EditorModel:

    SC_DATA = 'scenario_data'

    scenario_changed = Event(object)
    scenario_name_changed = Event(str)
    can_undo_changed = Event(bool)
    can_redo_changed = Event(bool)
    blocks_changed = Event(list)

    quest_types_changed = Event(list)
    current_sc_block_index_changed = Event(int)
    current_data_index_changed = Event(int)
    current_sc_block_changed = Event(object)
    current_data_changed = Event(object, str)

    listitem_widget_changed = Event(object)
    block_widget_changed = Event(object)

    update_scenario_event = Event()
    update_curr_sc_block = Event()

    def __init__(self):
        self._scenario = NotifyProperty('scenario')
        self._scenario += self.scenario_changed.emit
        self._can_undo = NotifyProperty('can_undo', False)
        self._can_undo += self.can_undo_changed.emit
        self._can_redo = NotifyProperty('can_redo', False)
        self._can_redo += self.can_redo_changed.emit
        self._blocks = NotifyProperty('blocks', list())
        self._blocks += self.blocks_changed.emit

        self._quest_types = NotifyProperty('quest_types_changed', list())
        self._quest_types += self.quest_types_changed.emit
        self._current_sc_block_index = NotifyProperty('current_sc_block_index', -1)
        self._current_sc_block_index += self.current_sc_block_index_changed.emit
        self._current_data_index = NotifyProperty('current_data_index', -1)
        self._current_data_index += self.current_data_index_changed.emit
        self._current_data_index += lambda x: self.send_data()

        self._listitem_widget = NotifyProperty('listitem_widget')
        self._listitem_widget += self.listitem_widget_changed.emit
        self._block_widget = NotifyProperty('_block_widget')
        self._block_widget += self.block_widget_changed.emit
        self.update_scenario_event += self.update_scenario
        self.update_curr_sc_block += self.send_sc_block

    # region Top lvl
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

    def append_scenario_data(self, sc_data):
        prop_path = f'{self.SC_DATA}.[{len(self.scenario.scenario_data)}]'
        AddMemento(prop_path, self.update_scenario_event)\
            (self.scenario.scenario_data.append)(sc_data)
        self.scenario_changed.emit(self.scenario)

    def remove_scenario_data(self, sc_data):
        prop_path = f'{self.SC_DATA}.[{self.scenario.scenario_data.index(sc_data)}]'
        RemoveMemento(prop_path, self.update_scenario_event)\
            (self.scenario.scenario_data.remove)(sc_data)
        self.scenario_changed.emit(self.scenario)

    # endregion

    # region Mid lvl

    @property
    def quest_types(self):
        return self._quest_types.get()

    @quest_types.setter
    def quest_types(self, value):
        self._quest_types.set(value)

    @property
    def current_sc_block_index(self):
        return self._current_sc_block_index.get()

    @current_sc_block_index.setter
    def current_sc_block_index(self, value):
        self._current_sc_block_index.set(value)

    @property
    def current_data_index(self):
        return self._current_data_index.get()

    @current_data_index.setter
    def current_data_index(self, value):
        self._current_data_index.set(value)

    def get_current_sc_block(self):
        index = self.current_sc_block_index
        return self.scenario.scenario_data[index] \
            if 0 <= index < len(self.scenario.scenario_data) else None

    def get_current_data(self):
        index = self.current_data_index
        sc_block = self.get_current_sc_block()
        return sc_block.data[index] \
            if 0 <= index < len(sc_block.data) else None

    def get_block_prop_path(self, prop_name):
        return f'{self.SC_DATA}.[{self.current_sc_block_index}].{prop_name}'

    def append_block_data(self, value):
        data = self.scenario.scenario_data[self.current_sc_block_index].data
        prop_path = f"{self.get_block_prop_path('data')}.[{len(data)}]"
        AddMemento(prop_path, self.update_curr_sc_block)(data.append)(value)
        self.current_kanji_index = len(data) - 1
        self.send_sc_block()

    def remove_block_data(self, value):
        data = self.scenario.scenario_data[self.current_sc_block_index].data
        prop_path = f"{self.get_block_prop_path('data')}.[{data.index(value)}]"
        RemoveMemento(prop_path, self.update_curr_sc_block)(data.remove)(value)
        self.current_kanji_index = -1
        self.send_sc_block()

    # endregion

    @property
    def listitem_widget(self):
        return self._listitem_widget.get()

    @listitem_widget.setter
    def listitem_widget(self, value):
        self._listitem_widget.set(value)

    @property
    def block_widget(self):
        return self._block_widget.get()

    @block_widget.setter
    def block_widget(self, value):
        self._block_widget.set(value)

    def update_scenario(self):
        self.scenario_changed.emit(self.scenario)

    def update_scenario_name(self):
        self.scenario_name_changed.emit(self.scenario.name)

    def send_sc_block(self):
        self.current_sc_block_changed.emit(self.get_current_sc_block())

    def send_data(self):
        prop_path = f"{self.get_block_prop_path('data')}.[{self.current_data_index}]"
        self.current_data_changed.emit(self.get_current_data(), prop_path)
