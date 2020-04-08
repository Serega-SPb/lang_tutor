from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QWidget, QGridLayout, QComboBox, QLabel


class KanjiWidget(QWidget):

    def __init__(self, kanji, parent=None):
        super().__init__(parent)
        self.kanji = kanji
        self.ui()

    def ui(self):
        grid = QGridLayout(self)

        self.titleLbl = QLabel()
        self.titleLbl.setText(self.kanji.value)
        self.titleLbl.setStyleSheet('font-size: 18px')
        grid.addWidget(self.titleLbl)

    def update_title(self):
        self.titleLbl.setText(self.kanji.value)


class KeyComboBox(QComboBox):

    items = {}

    def __init__(self, parent=None):
        super().__init__(parent)

    @classmethod
    def morph_from(cls, cmbx: QComboBox):
        ins = cls(cmbx.parent())
        ins.setSizePolicy(cmbx.sizePolicy())
        ins.setObjectName(cmbx.objectName())
        cmbx.deleteLater()
        return ins

    def load_data(self, data):
        self.clear()
        model = self.model()
        for i, d in enumerate(data):
            txt = f'{d.number}. {d.value}'
            if d.has_reduction:
                txt += f' ({", ".join(d.reductions)})'
            item = QStandardItem(txt)
            item.data = d
            model.appendRow(item)
            self.items[i] = item

    def select_by_value(self, value):
        ind = [num for num, item in self.items.items() if item.data == value]
        if ind:
            self.setCurrentIndex(ind.pop())

    def get_currect_data(self):
        ind = self.currentIndex()
        return self.items[ind].data if ind in self.items.keys() else None
