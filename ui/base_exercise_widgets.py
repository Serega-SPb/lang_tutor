from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLineEdit, \
    QLabel, QGroupBox, QRadioButton, QSizePolicy


QUEST_LBL_CSS = '''
font-size: 18px
'''

QUEST_KAN_LBL_CSS = '''
font-family: "Yu Mincho";
font-size: 60pt
'''


class BaseExerciseWidget(QWidget):

    def __init__(self, exercise, parent=None):
        super().__init__(parent)
        self.data = exercise
        self.__init_ui()

    def __init_ui(self):
        self.grid = QGridLayout(self)
        self.setLayout(self.grid)

        self._init_quest_field()
        self._init_answer_field()

    def _init_quest_field(self):
        self.questTypeLbl = QLabel(self)
        self.questTypeLbl.setText(self.data.question_type)
        self.questTypeLbl.setAlignment(Qt.AlignCenter)
        self.questTypeLbl.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.grid.addWidget(self.questTypeLbl, 0, 0, 1, 1)

        self.questLbl = QLabel(self)
        style = QUEST_LBL_CSS if len(self.data.question) > 1 else QUEST_KAN_LBL_CSS
        self.questLbl.setStyleSheet(style)
        self.questLbl.setAlignment(Qt.AlignCenter)
        self.questLbl.setText(self.data.question)
        self.grid.addWidget(self.questLbl, 1, 0, 1, 1)

    def _init_answer_field(self):
        pass


class ExerciseWidget(BaseExerciseWidget):

    def _init_answer_field(self):
        self.answerLnEd = QLineEdit(self)
        self.grid.addWidget(self.answerLnEd, 2, 0, 1, 1)

    @property
    def answer(self):
        return self.answerLnEd.text()


class ExerciseOptWidget(BaseExerciseWidget):

    def __init__(self, exercise, parent=None):
        super().__init__(exercise, parent)
        self.answer_btn = None

    def _init_answer_field(self):
        self.answersGroup = QGroupBox(self)
        v_box = QVBoxLayout(self.answersGroup)
        self.answersGroup.setLayout(v_box)
        for i, opt in enumerate(self.data.options_answers):
            raddbtn = QRadioButton()
            raddbtn.setStyleSheet(QUEST_LBL_CSS)
            raddbtn.setText(', '.join(opt) if isinstance(opt, list) else opt)
            raddbtn.data = opt

            raddbtn.toggled.connect(lambda x: self.rbtn_toggled_handler(raddbtn.sender(), x))
            v_box.addWidget(raddbtn)
        self.grid.addWidget(self.answersGroup, 2, 0, 1, 1)

    @property
    def answer(self):
        return self.answer_btn.data

    def rbtn_toggled_handler(self, sender, value):
        if value:
            self.answer_btn = sender
