# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ComplexAB.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(822, 882)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.cmap = QtWidgets.QComboBox(Form)
        self.cmap.setObjectName("cmap")
        self.cmap.addItem("")
        self.cmap.addItem("")
        self.cmap.addItem("")
        self.cmap.addItem("")
        self.cmap.addItem("")
        self.cmap.addItem("")
        self.cmap.addItem("")
        self.verticalLayout.addWidget(self.cmap)
        self.mplwidget = MatplotlibWidget(Form)
        self.mplwidget.setObjectName("mplwidget")
        self.verticalLayout.addWidget(self.mplwidget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ComplexAB"))
        self.cmap.setItemText(0, _translate("Form", "gray"))
        self.cmap.setItemText(1, _translate("Form", "prism"))
        self.cmap.setItemText(2, _translate("Form", "autumn"))
        self.cmap.setItemText(3, _translate("Form", "cool"))
        self.cmap.setItemText(4, _translate("Form", "spring"))
        self.cmap.setItemText(5, _translate("Form", "summer"))
        self.cmap.setItemText(6, _translate("Form", "winter"))

from matplotlibwidget import MatplotlibWidget
