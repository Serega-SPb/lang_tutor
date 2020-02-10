from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLineEdit, \
    QLabel, QGroupBox, QRadioButton


class ExerciseWidget(QWidget):

    def __init__(self, exercise, parent=None):
        super().__init__(parent)
        self.data = exercise
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout(self)
        self.setLayout(grid)

        self.questLbl = QLabel(self)
        self.questLbl.setStyleSheet('font-weight: bold; font-size: 22px')
        self.questLbl.setAlignment(Qt.AlignCenter)
        self.questLbl.setText(self.data.question)
        grid.addWidget(self.questLbl, 0, 0, 1, 1)

        self.answerLnEd = QLineEdit(self)
        grid.addWidget(self.answerLnEd, 1, 0, 1, 1)

    @property
    def answer(self):
        return self.answerLnEd.text()


class ExerciseOptWidget(QWidget):

    def __init__(self, exercise, parent=None):
        super().__init__(parent)
        self.data = exercise
        self.init_ui()
        self.answer_btn = None

    def init_ui(self):
        grid = QGridLayout(self)
        self.setLayout(grid)

        self.questLbl = QLabel(self)
        self.questLbl.setStyleSheet('font-weight: bold; font-size: 22px')
        self.questLbl.setAlignment(Qt.AlignCenter)
        self.questLbl.setText(self.data.question)
        grid.addWidget(self.questLbl, 0, 0, 1, 1)

        self.answersGroup = QGroupBox(self)
        v_box = QVBoxLayout(self.answersGroup)
        self.answersGroup.setLayout(v_box)
        for i, opt in enumerate(self.data.options_answers):
            raddbtn = QRadioButton()
            raddbtn.setText(', '.join(opt))
            raddbtn.data = opt

            raddbtn.toggled.connect(lambda x: self.rbtn_toggled_handler(raddbtn.sender(), x))
            v_box.addWidget(raddbtn)
        grid.addWidget(self.answersGroup, 1, 0, 1, 1)

    @property
    def answer(self):
        return self.answer_btn.data

    def rbtn_toggled_handler(self, sender, value):
        if value:
            self.answer_btn = sender
