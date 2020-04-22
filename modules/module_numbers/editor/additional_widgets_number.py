from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel


class NumberWidget(QWidget):

    def __init__(self, number, parent=None):
        super().__init__(parent)
        self.number = number
        self.ui()
        print(self.__module__)

    def ui(self):
        grid = QGridLayout(self)

        self.titleLbl = QLabel()
        self.update_title()
        self.titleLbl.setStyleSheet('font-size: 18px')
        grid.addWidget(self.titleLbl)

    def rangerd_text(self):
        r_text = "-".join(map(lambda x: str(x), self.number.value_range))
        return f'{r_text} ({self.number.step})'

    def update_title(self):
        text = self.rangerd_text() if self.number.is_range else str(self.number.value)
        self.titleLbl.setText(text)
