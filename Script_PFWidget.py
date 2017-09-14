import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PicketFence import Ui_Form


from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar


class PFWidget(QtWidgets.QDialog,Ui_Form):
    def __init__(self,parent=None):
        super(PFWidget,self).__init__(parent)
        self.setupUi(self)
        self.Img1='None'
        self.cmapType1='gray'
        self.Img2='None'
        self.cmapType2='gray'
        self.Img3='None'
        self.cmapType3='gray'
        self.ImgCombi='None'
        self.cmapTypeCombi='gray'



if __name__ == "__main__":
    app =QtWidgets.QApplication(sys.argv)
    dlg = PFWidget()
    dlg.show()
    sys.exit(app.exec_())
