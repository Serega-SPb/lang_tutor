# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Repositories\lang_tutor\ui\scenario\scenario_view.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1024, 768)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.exerciseWidget = QtWidgets.QWidget(Form)
        self.exerciseWidget.setObjectName("exerciseWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.exerciseWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.exerciseLayout = QtWidgets.QGridLayout()
        self.exerciseLayout.setObjectName("exerciseLayout")
        self.gridLayout_2.addLayout(self.exerciseLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.exerciseWidget, 1, 0, 1, 3)
        self.backMenuBtn = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backMenuBtn.sizePolicy().hasHeightForWidth())
        self.backMenuBtn.setSizePolicy(sizePolicy)
        self.backMenuBtn.setMinimumSize(QtCore.QSize(100, 35))
        self.backMenuBtn.setMaximumSize(QtCore.QSize(0, 16777215))
        self.backMenuBtn.setObjectName("backMenuBtn")
        self.gridLayout.addWidget(self.backMenuBtn, 0, 0, 1, 1)
        self.scenarioLbl = QtWidgets.QLabel(Form)
        self.scenarioLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.scenarioLbl.setObjectName("scenarioLbl")
        self.gridLayout.addWidget(self.scenarioLbl, 0, 1, 1, 1)
        self.counterLayout = QtWidgets.QHBoxLayout()
        self.counterLayout.setObjectName("counterLayout")
        self.currentLbl = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.currentLbl.sizePolicy().hasHeightForWidth())
        self.currentLbl.setSizePolicy(sizePolicy)
        self.currentLbl.setObjectName("currentLbl")
        self.counterLayout.addWidget(self.currentLbl)
        self.separatorLbl = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.separatorLbl.sizePolicy().hasHeightForWidth())
        self.separatorLbl.setSizePolicy(sizePolicy)
        self.separatorLbl.setObjectName("separatorLbl")
        self.counterLayout.addWidget(self.separatorLbl)
        self.totalLbl = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.totalLbl.sizePolicy().hasHeightForWidth())
        self.totalLbl.setSizePolicy(sizePolicy)
        self.totalLbl.setObjectName("totalLbl")
        self.counterLayout.addWidget(self.totalLbl)
        self.gridLayout.addLayout(self.counterLayout, 0, 2, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.answerBtn = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.answerBtn.sizePolicy().hasHeightForWidth())
        self.answerBtn.setSizePolicy(sizePolicy)
        self.answerBtn.setMinimumSize(QtCore.QSize(150, 35))
        self.answerBtn.setAutoDefault(False)
        self.answerBtn.setDefault(False)
        self.answerBtn.setObjectName("answerBtn")
        self.horizontalLayout.addWidget(self.answerBtn)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 3)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setRowStretch(1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.backMenuBtn.setText(_translate("Form", "Back to menu"))
        self.scenarioLbl.setText(_translate("Form", "SCENARIO_NAME"))
        self.currentLbl.setText(_translate("Form", "0"))
        self.separatorLbl.setText(_translate("Form", "/"))
        self.totalLbl.setText(_translate("Form", "0"))
        self.answerBtn.setText(_translate("Form", "Answer"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
