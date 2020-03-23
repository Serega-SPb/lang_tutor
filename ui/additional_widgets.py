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


class ModuleWidget(QWidget):

    def __init__(self, module, parent=None):
        super().__init__(parent)
        self.module = module
        self.ui()

    def ui(self):
        grid = QGridLayout(self)
        self.setLayout(grid)
        self.modChbx = QCheckBox(self)
        self.modChbx.setText(self.module.name)
        self.modChbx.setChecked(self.module.is_enabled)
        self.modChbx.toggled['bool'].connect(self.update_status)

        grid.addWidget(self.modChbx)

    def update_status(self, status):
        self.module.is_enabled = status


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
        self.reqModsLbl.setText(','.join(self.scenario.required_modules))
        self.reqModsLbl.setAlignment(Qt.AlignRight)
        grid.addWidget(self.reqModsLbl, 0, 2, 0, 1)


class ScenarioDataWidget(QWidget):

    def __init__(self, sc_data, remove_action, parent=None):
        super().__init__(parent)
        self.sc_data = sc_data
        self.rem_action = remove_action
        self.ui()

    def ui(self):
        grid = QGridLayout(self)

        self.titleLbl = QLabel()
        title_txt = f'{self.sc_data.module_name} | {self.sc_data.quest_type}'
        self.titleLbl.setText(title_txt)
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
