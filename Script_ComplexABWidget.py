import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from ComplexAB import Ui_Form

from skimage.filters import sobel


from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar


class ComplexABWidget(QtWidgets.QDialog,Ui_Form):
    def __init__(self,parent=None):
        super(ComplexABWidget,self).__init__(parent)
        self.setupUi(self)
        self.Img1='None'
        self.cmapType1='gray'
        self.navi_toolbar1 = NavigationToolbar(self.mplwidget,self)
        self.verticalLayout.addWidget(self.navi_toolbar1)

        self.cmap.currentIndexChanged.connect(self.updateCMap)

    def updateCMap(self):
        self.mplwidget.axes.clear()
        self.cmapType=str(self.cmap.currentText())
        self.mplwidget.axes.imshow(self.Img1,cmap=self.cmapType,alpha=0.5)

        edge_sobel = sobel(self.Img1)
        self.mplwidget.axes.hold(True)
        self.mplwidget.axes.imshow(edge_sobel,cmap='gray',alpha=0.5)
        self.mplwidget.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dlg = ComplexABWidget()
    dlg.show()
    sys.exit(app.exec_())
