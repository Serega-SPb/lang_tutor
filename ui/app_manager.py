from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, \
                            QStackedWidget, QMessageBox

from core.data_loader import DataLoader, Constants
from core.metaclasses import Singleton
from ui import main as main_widget, scenario as scenario_widget, editor as editor_widget
from ui.cross_widget_events import CrossWidgetEvents, MessageType as MsgType
from ui.translator import Translator


def init_locale():
    dataloader = DataLoader()
    Translator.set_locale(dataloader.get_config_param(Constants.LOCALE))
    Translator.register_translator('main', './')


class AppManager(metaclass=Singleton):
    APP_NAME = 'Lang tutor'
    WIDGETS = [
        main_widget,
        scenario_widget,
        editor_widget
    ]

    MSB_TYPE = {
        MsgType.INFO: QMessageBox.information,
        MsgType.WARN: QMessageBox.warning,
    }

    def __init__(self):
        init_locale()
        self.translator = Translator.get_translator('main')
        self.__init_main_window()
        self.__init_widgets()
        self.__init_event_handlers()

    def __init_main_window(self):
        self.main_window = QMainWindow()
        self.main_window.resize(1024, 768)
        self.main_window.setWindowTitle(self.APP_NAME)

        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.main_window.setFont(font)

        self.centralwidget = QWidget(self.main_window)
        self.centralwidget.setMinimumSize(QSize(1024, 768))
        grid = QGridLayout(self.centralwidget)
        self.mainStackWidget = QStackedWidget(self.centralwidget)
        self.mainStackWidget.setObjectName("mainStackWidget")

        grid.addWidget(self.mainStackWidget, 0, 0, 1, 1)
        grid.setColumnMinimumWidth(0, 200)
        self.main_window.setCentralWidget(self.centralwidget)

    def __init_widgets(self):
        for wid in self.WIDGETS:
            self.mainStackWidget.addWidget(wid.init())

    def __init_event_handlers(self):
        CrossWidgetEvents.change_screen_event += self.select_active_widget
        CrossWidgetEvents.show_message_event += self.show_info_msb
        CrossWidgetEvents.show_question_event += self.show_question_msb
        CrossWidgetEvents.clsoe_main_window_event += self.main_window.close

    def get_main_window(self):
        return self.main_window

    def select_active_widget(self, wid_id):
        self.mainStackWidget.setCurrentIndex(wid_id)

    def show_info_msb(self, t, title, message):
        if t not in self.MSB_TYPE.keys():
            t = MsgType.INFO
        self.MSB_TYPE[t](self.main_window, title, message)

    def __init_quest_msb(self):
        quest_msb = QMessageBox()
        quest_msb.setIcon(QMessageBox.Question)
        quest_msb.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        yes_btn = quest_msb.button(QMessageBox.Yes)
        yes_btn.setText(self.translator.translate('YES_ANSWER'))
        no_btn = quest_msb.button(QMessageBox.No)
        no_btn.setText(self.translator.translate('NO_ANSWER'))
        return quest_msb

    def show_question_msb(self, title, message, yes_action):
        quest_msb = self.__init_quest_msb()
        quest_msb.setWindowTitle(title)
        quest_msb.setText(message)
        answer = quest_msb.exec()
        if answer == QMessageBox.Yes:
            yes_action()
