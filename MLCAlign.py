# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MLCAlign.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1022, 962)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Wedge1Layout = QtWidgets.QVBoxLayout()
        self.Wedge1Layout.setObjectName("Wedge1Layout")
        self.comboBox_cmap1 = QtWidgets.QComboBox(Form)
        self.comboBox_cmap1.setObjectName("comboBox_cmap1")
        self.comboBox_cmap1.addItem("")
        self.comboBox_cmap1.addItem("")
        self.comboBox_cmap1.addItem("")
        self.comboBox_cmap1.addItem("")
        self.comboBox_cmap1.addItem("")
        self.comboBox_cmap1.addItem("")
        self.comboBox_cmap1.addItem("")
        self.Wedge1Layout.addWidget(self.comboBox_cmap1)
        self.MLCAlignWidget = MatplotlibWidget(Form)
        self.MLCAlignWidget.setObjectName("MLCAlignWidget")
        self.Wedge1Layout.addWidget(self.MLCAlignWidget)
        self.horizontalLayout_2.addLayout(self.Wedge1Layout)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "MLC Alignment"))
        self.comboBox_cmap1.setItemText(0, _translate("Form", "gray"))
        self.comboBox_cmap1.setItemText(1, _translate("Form", "prism"))
        self.comboBox_cmap1.setItemText(2, _translate("Form", "autumn"))
        self.comboBox_cmap1.setItemText(3, _translate("Form", "cool"))
        self.comboBox_cmap1.setItemText(4, _translate("Form", "spring"))
        self.comboBox_cmap1.setItemText(5, _translate("Form", "summer"))
        self.comboBox_cmap1.setItemText(6, _translate("Form", "winter"))

from matplotlibwidget import MatplotlibWidget
