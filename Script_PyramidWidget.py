import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from Pyramids import Ui_Form

from skimage.filters import sobel


from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar


class PyramidWidget(QtWidgets.QDialog,Ui_Form):
    def __init__(self,parent=None):
        super(PyramidWidget,self).__init__(parent)
        self.setupUi(self)
        self.Img1='None'
        self.cmapType1='gray'
        self.Img2='None'
        self.cmapType2='gray'
        self.navi_toolbar1 = NavigationToolbar(self.pyramid1,self)
        self.verticalLayout.addWidget(self.navi_toolbar1)
        self.navi_toolbar2 = NavigationToolbar(self.pyramid2,self)
        self.verticalLayout_2.addWidget(self.navi_toolbar2)

        self.cmap1.currentIndexChanged.connect(self.updateCMap1)
        self.cmap2.currentIndexChanged.connect(self.updateCMap2)


    def updateCMap1(self):
        #self.pyramid1.axes.clear()
        self.cmapType1=str(self.cmap1.currentText())
        self.pyramid1.axes.imshow(self.Img1,cmap=self.cmapType1,alpha=0.5)

        edge_sobel = sobel(self.Img1)
        self.pyramid1.axes.hold(True)
        self.pyramid1.axes.imshow(edge_sobel,cmap='gray',alpha=0.5)
        self.pyramid1.axes.hold(True)
        self.pyramid1.axes.set_xlabel('Pixel No. A-B')
        self.pyramid1.axes.set_ylabel('Pixel No. T-G')
        self.pyramid1.draw()

    def updateCMap2(self):
        #self.pyramid2.axes.clear()
        self.cmapType2=str(self.cmap2.currentText())
        self.pyramid2.axes.imshow(self.Img2,cmap=self.cmapType2,alpha=0.5)

        edge_sobel = sobel(self.Img2)
        self.pyramid2.axes.hold(True)
        self.pyramid2.axes.imshow(edge_sobel,cmap='gray',alpha=0.5)
        self.pyramid2.axes.hold(True)
        self.pyramid2.axes.set_xlabel('Pixel No. A-B')
        self.pyramid2.axes.set_ylabel('Pixel No. T-G')
        self.pyramid2.draw()


if __name__ == "__main__":
    app =QtWidgets.QApplication(sys.argv)
    dlg = PyramidWidget()
    dlg.show()
    sys.exit(app.exec_())
