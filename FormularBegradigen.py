# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formular_Begradigen.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(703, 471)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Containerx = QtWidgets.QVBoxLayout()
        self.Containerx.setObjectName("Containerx")
        self.horizontalLayout.addLayout(self.Containerx)
        self.Containery = QtWidgets.QVBoxLayout()
        self.Containery.setObjectName("Containery")
        self.horizontalLayout.addLayout(self.Containery)
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonBegradigen = QtWidgets.QPushButton(Form)
        self.pushButtonBegradigen.setObjectName("pushButtonBegradigen")
        self.gridLayout.addWidget(self.pushButtonBegradigen, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.pushButtonLaden = QtWidgets.QPushButton(Form)
        self.pushButtonLaden.setObjectName("pushButtonLaden")
        self.gridLayout.addWidget(self.pushButtonLaden, 1, 0, 1, 1)
        self.textEditCount = QtWidgets.QTextEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEditCount.sizePolicy().hasHeightForWidth())
        self.textEditCount.setSizePolicy(sizePolicy)
        self.textEditCount.setObjectName("textEditCount")
        self.gridLayout.addWidget(self.textEditCount, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButtonBegradigen.setText(_translate("Form", "Begradigen"))
        self.pushButton_2.setText(_translate("Form", "PushButton"))
        self.pushButtonLaden.setText(_translate("Form", "Laden"))

