# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Repositories\lang_tutor\ui\editor\editor_view.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1024, 768)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.backMenuBtn = QtWidgets.QPushButton(Form)
        self.backMenuBtn.setObjectName("backMenuBtn")
        self.gridLayout_2.addWidget(self.backMenuBtn, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.undoBtn = QtWidgets.QPushButton(Form)
        self.undoBtn.setObjectName("undoBtn")
        self.horizontalLayout.addWidget(self.undoBtn)
        self.redoBtn = QtWidgets.QPushButton(Form)
        self.redoBtn.setObjectName("redoBtn")
        self.horizontalLayout.addWidget(self.redoBtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.saveBtn = QtWidgets.QPushButton(Form)
        self.saveBtn.setObjectName("saveBtn")
        self.horizontalLayout.addWidget(self.saveBtn)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.scenarioNameLed = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scenarioNameLed.sizePolicy().hasHeightForWidth())
        self.scenarioNameLed.setSizePolicy(sizePolicy)
        self.scenarioNameLed.setObjectName("scenarioNameLed")
        self.gridLayout.addWidget(self.scenarioNameLed, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.scenarioBlocksList = QtWidgets.QListWidget(Form)
        self.scenarioBlocksList.setObjectName("scenarioBlocksList")
        self.gridLayout.addWidget(self.scenarioBlocksList, 2, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 2)
        self.addBlockLayout = QtWidgets.QHBoxLayout()
        self.addBlockLayout.setSpacing(12)
        self.addBlockLayout.setObjectName("addBlockLayout")
        self.label_3 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.addBlockLayout.addWidget(self.label_3)
        self.blocksCmbBx = QtWidgets.QComboBox(Form)
        self.blocksCmbBx.setObjectName("blocksCmbBx")
        self.addBlockLayout.addWidget(self.blocksCmbBx)
        self.addBlockBtn = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addBlockBtn.sizePolicy().hasHeightForWidth())
        self.addBlockBtn.setSizePolicy(sizePolicy)
        self.addBlockBtn.setObjectName("addBlockBtn")
        self.addBlockLayout.addWidget(self.addBlockBtn)
        self.gridLayout.addLayout(self.addBlockLayout, 3, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.scenarioBlockWidget = QtWidgets.QWidget(Form)
        self.scenarioBlockWidget.setObjectName("scenarioBlockWidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.scenarioBlockWidget)
        self.gridLayout_4.setContentsMargins(15, 20, -1, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.questTypeLayout = QtWidgets.QHBoxLayout()
        self.questTypeLayout.setSpacing(12)
        self.questTypeLayout.setObjectName("questTypeLayout")
        self.label_10 = QtWidgets.QLabel(self.scenarioBlockWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName("label_10")
        self.questTypeLayout.addWidget(self.label_10)
        self.questTypeCmbBx = QtWidgets.QComboBox(self.scenarioBlockWidget)
        self.questTypeCmbBx.setObjectName("questTypeCmbBx")
        self.questTypeLayout.addWidget(self.questTypeCmbBx)
        self.gridLayout_4.addLayout(self.questTypeLayout, 0, 0, 1, 1)
        self.blockDataContainer = QtWidgets.QWidget(self.scenarioBlockWidget)
        self.blockDataContainer.setEnabled(True)
        self.blockDataContainer.setObjectName("blockDataContainer")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.blockDataContainer)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_4.addWidget(self.blockDataContainer, 0, 1, 2, 1)
        self.blockDataLayout = QtWidgets.QVBoxLayout()
        self.blockDataLayout.setObjectName("blockDataLayout")
        self.blockDataList = QtWidgets.QListWidget(self.scenarioBlockWidget)
        self.blockDataList.setObjectName("blockDataList")
        self.blockDataLayout.addWidget(self.blockDataList)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addBtn = QtWidgets.QPushButton(self.scenarioBlockWidget)
        self.addBtn.setObjectName("addBtn")
        self.horizontalLayout_2.addWidget(self.addBtn)
        self.removeBtn = QtWidgets.QPushButton(self.scenarioBlockWidget)
        self.removeBtn.setObjectName("removeBtn")
        self.horizontalLayout_2.addWidget(self.removeBtn)
        self.blockDataLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_4.addLayout(self.blockDataLayout, 1, 0, 1, 1)
        self.gridLayout_4.setColumnStretch(0, 1)
        self.gridLayout_4.setColumnStretch(1, 2)
        self.gridLayout_2.addWidget(self.scenarioBlockWidget, 1, 1, 1, 1)
        self.gridLayout_2.setColumnMinimumWidth(0, 200)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.backMenuBtn.setText(_translate("Form", "Back to menu"))
        self.undoBtn.setText(_translate("Form", "<-"))
        self.redoBtn.setText(_translate("Form", "->"))
        self.saveBtn.setText(_translate("Form", "SAVE"))
        self.label.setText(_translate("Form", "Name"))
        self.label_2.setText(_translate("Form", "Blocks"))
        self.label_3.setText(_translate("Form", "Block"))
        self.addBlockBtn.setText(_translate("Form", "Add"))
        self.label_10.setText(_translate("Form", "Quest type"))
        self.addBtn.setText(_translate("Form", "Add"))
        self.removeBtn.setText(_translate("Form", "Remove"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
