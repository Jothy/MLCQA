import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from MLCAlign import Ui_Form

import numpy as np


from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar


class MLCAlignWidget(QtWidgets.QDialog,Ui_Form):
    def __init__(self,parent=None):
        super(MLCAlignWidget,self).__init__(parent)
        self.setupUi(self)
        self.cmapType1='gray'
        self.Img1='None'
        self.Img2='None'
        self.Img3='None'
        self.CentreMeanValue=0.0
        self.navi_toolbar1 = NavigationToolbar(self.MLCAlignWidget, self)
        self.Wedge1Layout.addWidget(self.navi_toolbar1)

        self.comboBox_cmap1.currentIndexChanged.connect(self.updateCMap1)

    def updateCMap1(self):
        self.cmapType1=str(self.comboBox_cmap1.currentText())
        self.MLCAlignWidget.axes.imshow(self.Img3,cmap=self.cmapType1)
        self.MLCAlignWidget.draw()





if __name__ == "__main__":
    app =QtWidgets.QApplication(sys.argv)
    dlg = MLCAlignWidget()
    dlg.show()
    sys.exit(app.exec_())
