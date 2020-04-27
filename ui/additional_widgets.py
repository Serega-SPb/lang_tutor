from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QLabel, QPushButton, QListWidgetItem


def load_data_in_list(list_wid, data_wid, data, *args):
    item = QListWidgetItem()
    item.data = data
    widget = data_wid(data, *args, list_wid)
    item.wid = widget

    item.setSizeHint(widget.sizeHint())
    list_wid.addItem(item)
    list_wid.setItemWidget(item, widget)


def translate_widget(wid, translator):
    if hasattr(wid, 'text'):
        if not hasattr(wid, 'text_var'):
            wid.text_var = wid.text()
        wid.setText(translator.translate(wid.text_var))
    elif hasattr(wid, 'title'):
        if not hasattr(wid, 'title_var'):
            wid.title_var = wid.title()
        wid.setTitle(translator.translate(wid.title_var))


class ModuleWidget(QWidget):

    def __init__(self, module, parent=None):
        super().__init__(parent)
        self.module = module
        self.ui()

    def ui(self):
        grid = QGridLayout(self)
        self.setLayout(grid)
        self.modChbx = QCheckBox(self)
        self.update_lbl()
        self.modChbx.setChecked(self.module.is_enabled)
        self.modChbx.toggled['bool'].connect(self.update_status)

        grid.addWidget(self.modChbx)

    def update_status(self, status):
        self.module.is_enabled = status
        self.modChbx.setChecked(self.module.is_enabled)
        self.update_lbl()

    def update_lbl(self):
        self.modChbx.setText(self.module.ui_name)


class ScenarioWidget(QWidget):

    def __init__(self, scenario, parent=None):
        super().__init__(parent)
        self.scenario = scenario
        self.ui()

    def ui(self):
        grid = QGridLayout(self)

        self.titleLbl = QLabel()
        self.titleLbl.setText(self.scenario.name)
        grid.addWidget(self.titleLbl)

        self.reqModsLbl = QLabel()
        mod_names = [mod.ui_name for mod in self.scenario.required_modules]
        self.reqModsLbl.setText(', '.join(mod_names))
        self.reqModsLbl.setAlignment(Qt.AlignRight)
        grid.addWidget(self.reqModsLbl, 0, 2, 0, 1)


class ScenarioDataWidget(QWidget):

    def __init__(self, sc_data, remove_action, parent=None):
        super().__init__(parent)
        self.sc_data = sc_data
        self.rem_action = remove_action
        self.ui()

        self.sc_data.quest_type_changed += self.update_title
        self.titleLbl.destroyed.connect(self.unsubscribe)

    def ui(self):
        grid = QGridLayout(self)

        self.titleLbl = QLabel()
        self.update_title()
        grid.addWidget(self.titleLbl)

        self.countLbl = QLabel()
        self.countLbl.setText(f'({len(self.sc_data.data)})')
        self.countLbl.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.countLbl, 0, 3, 0, 1)

        self.removeBtn = QPushButton()
        self.removeBtn.setText('X')
        self.removeBtn.setFixedSize(25, 25)
        self.removeBtn.clicked.connect(lambda: self.rem_action(self.sc_data))
        grid.addWidget(self.removeBtn, 0, 4, 0, 1)

    def update_title(self, *args):
        mod_name = self.sc_data.module.init.get_name()
        q_type = self.sc_data.quest_type.ui
        title_txt = f'{mod_name} | {q_type}'
        self.titleLbl.setText(title_txt)

    def unsubscribe(self):
        self.sc_data.quest_type_changed -= self.update_title
