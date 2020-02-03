from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QLabel


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
