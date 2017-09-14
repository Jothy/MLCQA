import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from ContStripes import Ui_Form


from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar


class ContStripesWidget(QtWidgets.QDialog,Ui_Form):
    def __init__(self,parent=None):
        super(ContStripesWidget,self).__init__(parent)
        self.setupUi(self)
        self.Img='None'
        self.cmapType='gray'
        self.navi_toolbar1 = NavigationToolbar(self.Stripes,self)
        self.verticalLayout.addWidget(self.navi_toolbar1)

        self.cmap.currentIndexChanged.connect(self.updateCMap)

    def updateCMap(self):
        #self.Stripes.axes.clear()
        self.cmapType=str(self.cmap.currentText())
        self.Stripes.axes.imshow(self.Img,cmap=self.cmapType)
        self.Stripes.draw()





if __name__ == "__main__":
    app =QtWidgets.QApplication(sys.argv)
    dlg = ContStripesWidget()
    dlg.show()
    sys.exit(app.exec_())
