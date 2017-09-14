import sys
import os
from PyQt4.QtCore import*
from PyQt4.QtGui import*
from MPLWidget import Ui_Form


from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar


class MPLWidget(QDialog,Ui_Form):
    def __init__(self,parent=None):
        super(MPLWidget,self).__init__(parent)
        self.setupUi(self)
        self.navi_toolbar = NavigationToolbar(self.mplwidget, self)
        self.gridLayout.addWidget(self.navi_toolbar)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = MPLWidget()
    dlg.show()
    sys.exit(app.exec_())
