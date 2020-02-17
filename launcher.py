from PyQt5.QtWidgets import QApplication

from ui.app_manager import AppManager


def main():
    app = QApplication([])
    app_man = AppManager()
    main_window = app_man.main_window
    main_window.show()
    app.exec_()


if __name__ == '__main__':
    main()
