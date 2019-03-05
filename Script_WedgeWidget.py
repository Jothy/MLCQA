import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from Wedges import Ui_Form

import numpy as np


from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar


class WedgeWidget(QtWidgets.QDialog,Ui_Form):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.cmapType1='gray'
        self.cmapType2='gray'
        self.cmapType3='gray'
        self.Img1='None'
        self.Img2='None'
        self.Img3='None'
        self.CentreMeanValue=0.0
        self.navi_toolbar1 = NavigationToolbar(self.Wedge1, self)
        self.navi_toolbar2 = NavigationToolbar(self.Wedge2, self)
        self.navi_toolbar3 = NavigationToolbar(self.CombinedWedges, self)
        self.Wedge1Layout.addWidget(self.navi_toolbar1)
        self.Wedge2Layout.addWidget(self.navi_toolbar2)
        self.CombiLayout.addWidget(self.navi_toolbar3)

        self.comboBox_cmap1.currentIndexChanged.connect(self.updateCMap1)
        self.comboBox_cmap2.currentIndexChanged.connect(self.updateCMap2)
        self.comboBox_cmap3.currentIndexChanged.connect(self.updateCMap3)


    def updateCMap1(self):
        self.cmapType1=str(self.comboBox_cmap1.currentText())
        self.Wedge1.axes.imshow(self.Img1,cmap=self.cmapType1)
        self.Wedge1.draw()


    def updateCMap2(self):
            self.cmapType2=str(self.comboBox_cmap2.currentText())
            self.Wedge2.axes.imshow(self.Img2,cmap=self.cmapType2)
            self.Wedge2.draw()


    def CalcCentreMean(self,Img):
        shape=np.shape(Img)
        CentreMean=list()
        if shape[0]==768:#as1000
            c1=Img[383,512+2]
            c2=Img[383,512+2]
            c3=Img[384,512+2]
            c4=Img[385,512+2]
            c5=Img[383,511+2]
            c6=Img[384,511+2]
            c7=Img[385,511+2]
            c8=Img[383,513+2]
            c9=Img[384,513+2]
        else:
            c1=Img[188,256+2]
            c2=Img[189,256+2]
            c3=Img[190,256+2]
            c4=Img[191,256+2]
            c5=Img[192,256+2]
            c6=Img[192,256+2]
            c7=Img[193,256+2]
            c8=Img[194,256+2]
            c9=Img[195,256+2]

        CentreMean.append(c1),CentreMean.append(c2),CentreMean.append(c3)
        CentreMean.append(c4),CentreMean.append(c5),CentreMean.append(c6)
        CentreMean.append(c7),CentreMean.append(c8),CentreMean.append(c9)
        self.CentreMeanValue=np.mean(CentreMean)*-1.0
        #print(self.CentreMeanValue,'Mean')


    def updateCMap3(self):
            self.cmapType3=str(self.comboBox_cmap3.currentText())
            self.CombinedWedges.axes.imshow(self.Img3,cmap=self.cmapType3)
            self.CombinedWedges.draw()

    def plotProfiles(self,WedgeType):
        #Tolerance lines are +/-2%; not sure is this appropriate?
        self.CalcCentreMean(self.Img3)
        EPIDType=np.shape(self.Img3)
        if WedgeType=='X':
            if EPIDType[0]==768:
                xProfile1=self.Img1[384,:]*-1.0
                self.profiler.axes.plot(xProfile1,'g')
                self.profiler.axes.set_xlim(0,1024)
                #self.profiler.axes.hold(True)
                xProfile2=self.Img2[384,:]*-1.0
                self.profiler.axes.plot(xProfile2,'r')
                #self.profiler.axes.hold(True)
                xProfileCombined=self.Img3[384,:]*-1.0
                self.profiler.axes.plot(xProfileCombined,'b')
                #self.profiler.axes.hold(True)

                xValues=np.linspace(0,1024,1024)
                yValuesUP=np.ones([1024])*(self.CentreMeanValue+self.CentreMeanValue*0.02)
                yValuesLOW=np.ones([1024])*(self.CentreMeanValue-self.CentreMeanValue*0.02)
            else:
                xProfile1=self.Img1[192,:]*-1.0
                self.profiler.axes.plot(xProfile1,'g')
                self.profiler.axes.set_xlim(0,512)
                #self.profiler.axes.hold(True)
                xProfile2=self.Img2[192,:]*-1.0
                self.profiler.axes.plot(xProfile2,'r')
                #self.profiler.axes.hold(True)
                xProfileCombined=self.Img3[192,:]*-1.0
                self.profiler.axes.plot(xProfileCombined,'b')
                self.profiler.axes.hold(True)

                xValues=np.linspace(0,512,512)
                yValuesUP=np.ones([512])*(self.CentreMeanValue+self.CentreMeanValue*0.02)
                yValuesLOW=np.ones([512])*(self.CentreMeanValue-self.CentreMeanValue*0.02)



        else:#plot Y wedge
            if EPIDType[0]==768:
                yProfile1=self.Img1[:,512]*-1.0
                self.profiler.axes.plot(yProfile1,'g')
                self.profiler.axes.set_xlim(0,768)
                #self.profiler.axes.hold(True)
                yProfile2=self.Img2[:,512]*-1.0
                self.profiler.axes.plot(yProfile2,'r')
                #self.profiler.axes.hold(True)
                yProfileCombined=self.Img3[:,512]*-1.0
                self.profiler.axes.plot(yProfileCombined,'b')
                #self.profiler.axes.hold(True)

                xValues=np.linspace(0,768,768)
                yValuesUP=np.ones([768])*(self.CentreMeanValue+self.CentreMeanValue*0.02)
                yValuesLOW=np.ones([768])*(self.CentreMeanValue-self.CentreMeanValue*0.02)
            else:
                yProfile1=self.Img1[:,256]*-1.0
                self.profiler.axes.plot(yProfile1,'g')
                self.profiler.axes.set_xlim(0,384)
                #self.profiler.axes.hold(True)
                yProfile2=self.Img2[:,256]*-1.0
                self.profiler.axes.plot(yProfile2,'r')
                #self.profiler.axes.hold(True)
                yProfileCombined=self.Img3[:,256]*-1.0
                self.profiler.axes.plot(yProfileCombined,'b')
                self.profiler.axes.hold(True)

                xValues=np.linspace(0,384,384)
                yValuesUP=np.ones([384])*(self.CentreMeanValue+self.CentreMeanValue*0.02)
                yValuesLOW=np.ones([384])*(self.CentreMeanValue-self.CentreMeanValue*0.02)



        self.profiler.axes.plot(xValues,yValuesUP,'gray')
        #self.profiler.axes.hold(True)
        self.profiler.axes.plot(xValues,yValuesLOW,'gray')
        self.profiler.axes.set_xlabel('Pixel No.')
        self.profiler.axes.set_ylabel('Arbitrary Units')

        self.profiler.axes.legend(['Wedge1','Wedge2','Combined Wedges'],fontsize=6,loc=4)
        self.profiler.draw()







if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dlg = WedgeWidget()
    dlg.show()
    sys.exit(app.exec_())
