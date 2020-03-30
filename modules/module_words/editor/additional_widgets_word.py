from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel


class WordWidget(QWidget):

    def __init__(self, word, parent=None):
        super().__init__(parent)
        self.word = word
        self.ui()

    def ui(self):
        grid = QGridLayout(self)

        self.titleLbl = QLabel()
        self.update_title()
        self.titleLbl.setStyleSheet('font-size: 18px')
        grid.addWidget(self.titleLbl)

    def update_title(self):
        self.titleLbl.setText(f'{self.word.spelling} ({self.word.reading})')
