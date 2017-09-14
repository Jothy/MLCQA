# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Pyramids.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1034, 538)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.cmap1 = QtWidgets.QComboBox(Form)
        self.cmap1.setObjectName("cmap1")
        self.cmap1.addItem("")
        self.cmap1.addItem("")
        self.cmap1.addItem("")
        self.cmap1.addItem("")
        self.cmap1.addItem("")
        self.cmap1.addItem("")
        self.cmap1.addItem("")
        self.verticalLayout.addWidget(self.cmap1)
        self.pyramid1 = MatplotlibWidget(Form)
        self.pyramid1.setObjectName("pyramid1")
        self.verticalLayout.addWidget(self.pyramid1)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cmap2 = QtWidgets.QComboBox(Form)
        self.cmap2.setObjectName("cmap2")
        self.cmap2.addItem("")
        self.cmap2.addItem("")
        self.cmap2.addItem("")
        self.cmap2.addItem("")
        self.cmap2.addItem("")
        self.cmap2.addItem("")
        self.cmap2.addItem("")
        self.verticalLayout_2.addWidget(self.cmap2)
        self.pyramid2 = MatplotlibWidget(Form)
        self.pyramid2.setObjectName("pyramid2")
        self.verticalLayout_2.addWidget(self.pyramid2)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Pyramids"))
        self.cmap1.setItemText(0, _translate("Form", "gray"))
        self.cmap1.setItemText(1, _translate("Form", "prism"))
        self.cmap1.setItemText(2, _translate("Form", "autumn"))
        self.cmap1.setItemText(3, _translate("Form", "cool"))
        self.cmap1.setItemText(4, _translate("Form", "spring"))
        self.cmap1.setItemText(5, _translate("Form", "summer"))
        self.cmap1.setItemText(6, _translate("Form", "winter"))
        self.cmap2.setItemText(0, _translate("Form", "gray"))
        self.cmap2.setItemText(1, _translate("Form", "prism"))
        self.cmap2.setItemText(2, _translate("Form", "autumn"))
        self.cmap2.setItemText(3, _translate("Form", "cool"))
        self.cmap2.setItemText(4, _translate("Form", "spring"))
        self.cmap2.setItemText(5, _translate("Form", "summer"))
        self.cmap2.setItemText(6, _translate("Form", "winter"))

from matplotlibwidget import MatplotlibWidget
