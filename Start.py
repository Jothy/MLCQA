import sys
import os.path,time
from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from MainWindow import Ui_MainWindow


import Script_WedgeWidget as WedgeDlg
import Script_ComplexABWidget as ComplexDlg
import Script_PyramidWidget as PyramidDlg
import Script_PFWidget as PFDlg
import Script_MLCAlign as MLCAlignDlg
import Script_ContStripesWidget as ContStripesDlg

import DCMReader
import numpy as np
from skimage.filters import sobel
from pylinac.picketfence import PicketFence


import pylab as pl
from datetime import date

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from skimage.measure import structural_similarity as ssim

#To bundle dlls into to exe with Pyinstaller
import ctypes

if getattr(sys, 'frozen', False):
  # Override dll search path.
  ctypes.windll.kernel32.SetDllDirectoryW('C:/Anaconda3/Library/bin/')
  # Init code to load external dll
  ctypes.CDLL('mkl_def.dll')
  # Restore dll search path.
  ctypes.windll.kernel32.SetDllDirectoryW(sys._MEIPASS)

class StartQT(  QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Connect signal slots
        self.ui.pushButtonMLCQAMonthly.clicked.connect(self.AutoReportMonthlyMLCQA)

        self.CurrentImages=[]
        self.Mode='Auto'
        self.Iso=[512,384]


    def SaveWidgetScreenShot(self, Widget, filename):
        pixelMap =Qt.QPixmap(Widget.size())
        Widget.render(pixelMap,Qt.QPoint(),Qt.QRegion())
        pixelMap.save(filename, quality=100)

    def AnalyseWedges(self, title):
        if self.Mode == "Manual":
            files =QtWidgets.QFileDialog(self)
            files.setWindowTitle(title)
            if title == 'XWedges':
                self.CurrentImages = files.getOpenFileNames(self, caption='X-Wedges')
            else:
                self.CurrentImages = files.getOpenFileNames(self, caption='Y-Wedges')
        WedgeDlg1 = WedgeDlg.WedgeWidget(self)
        WedgeDlg1.setWindowTitle(title)

        yWedge1 = DCMReader.ReadDCMFile(str(self.CurrentImages[0]))
        WedgeDlg1.Img1 = yWedge1
        WedgeDlg1.Wedge1.axes.imshow(WedgeDlg1.Img1, cmap='gray')
        if self.WedgeType == 'X':
            WedgeDlg1.Wedge1.axes.set_title('Wedge1 -X')
        else:
            WedgeDlg1.Wedge1.axes.set_title('Wedge1 -Y')
        #WedgeDlg1.Wedge1.axes.hold(True)

        EPIDType = np.shape(yWedge1)
        if EPIDType[0] == 768:
            WedgeDlg1.Wedge1.axes.plot(self.Iso[0], self.Iso[1], 'y+', markersize=20)
        else:
            WedgeDlg1.Wedge1.axes.plot(256, 192, 'y+', markersize=20)

        WedgeDlg1.Wedge1.axes.set_xlabel('Pixel No. A-B')
        WedgeDlg1.Wedge1.axes.set_ylabel('Pixel No. T-G')
        if self.Mode == "Manual":
            WedgeDlg1.Wedge1.draw()

        yWedge2 = DCMReader.ReadDCMFile(str(self.CurrentImages[1]))
        WedgeDlg1.Img2 = yWedge2
        WedgeDlg1.Wedge2.axes.imshow(WedgeDlg1.Img2, cmap='gray')
        if self.WedgeType == 'X':
            WedgeDlg1.Wedge2.axes.set_title('Wedge2 -x')
        else:
            WedgeDlg1.Wedge2.axes.set_title('Wedge2 -y')
        #WedgeDlg1.Wedge2.axes.hold(True)
        if EPIDType[0] == 768:
            WedgeDlg1.Wedge2.axes.plot(self.Iso[0], self.Iso[1], 'y+', markersize=20)
        else:
            WedgeDlg1.Wedge2.axes.plot(256, 192, 'y+', markersize=20)

        WedgeDlg1.Wedge2.axes.set_xlabel('Pixel No. A-B')
        WedgeDlg1.Wedge2.axes.set_ylabel('Pixel No. T-G')
        if self.Mode == "Manual":
            WedgeDlg1.Wedge2.draw()

        combiWedges = yWedge1 + yWedge2
        WedgeDlg1.Img3 = combiWedges
        WedgeDlg1.CombinedWedges.axes.imshow(WedgeDlg1.Img3, cmap='gray')
        if self.WedgeType == 'X':
            WedgeDlg1.CombinedWedges.axes.set_title('Combined Wedges-X')
        else:
            WedgeDlg1.CombinedWedges.axes.set_title('Combined Wedges-Y')
        #WedgeDlg1.CombinedWedges.axes.hold(True)
        if EPIDType[0] == 768:
            WedgeDlg1.CombinedWedges.axes.plot(self.Iso[0], self.Iso[1], 'y+', markersize=20)
        else:
            WedgeDlg1.CombinedWedges.axes.plot(256, 192, 'y+', markersize=20)

        # WedgeDlg1.CombinedWedges.axes.set_xlim(0,1024)
        # WedgeDlg1.CombinedWedges.axes.set_ylim(0,768)
        WedgeDlg1.CombinedWedges.axes.set_xlabel('Pixel No. A-B')
        WedgeDlg1.CombinedWedges.axes.set_ylabel('Pixel No. T-G')

        if self.Mode == "Manual":
            WedgeDlg1.CombinedWedges.draw()

        WedgeDlg1.plotProfiles(self.WedgeType)
        # print(self.WedgeType,"WedgeType")
        WedgeDlg1.exec()
        WedgeDlg1.close()

        if self.Mode == "Manual":
            WedgeDlg1.exec_()
        if self.WedgeType == 'X':
            self.SaveWidgetScreenShot(WedgeDlg1, 'XWedges.jpg')
        if self.WedgeType == 'Y':
            self.SaveWidgetScreenShot(WedgeDlg1, 'YWedges.jpg')

    def AnalyseXWedges(self):
        self.WedgeType = 'X'
        self.AnalyseWedges('XWedges')

    def AnalyseYWedges(self):
        self.WedgeType = 'Y'
        self.AnalyseWedges('YWedges')

    def AnalysePicketFence0(self):
        if self.Mode == "Manual":
            files =QtWidgets.QFileDialog(self)
            files.setWindowTitle('Picket Fence 0')
            self.CurrentImages = files.getOpenFileNames(self, caption='Continuous Stripes (1)')

        ContStripesDlg1 = ContStripesDlg.ContStripesWidget(self)
        # ContStripesDlg1.Img=DCMReader.ReadDCMFile(str(self.CurrentImages[0]))

        mypf = PicketFence(str(self.CurrentImages[0]))

        mypf.image.check_inversion()
        mypf.analyze(tolerance=0.5, action_tolerance=0.3, hdmlc=False)
        mypf.save_analyzed_image('PicketFence0', gaurd_rails=True, mlc_peaks=True, overlay=True,
                                 leaf_error_subplot=True)
        # print(mypf.num_pickets,'No. of pickets found')
        # print(mypf.return_results())
        # mypf.plot_analyzed_image()

        AnalyzedImage = pl.imread('PicketFence0.png')
        ContStripesDlg1.Stripes.axes.imshow(AnalyzedImage)
        ContStripesDlg1.ResultsLabel.setText(mypf.return_results())
        # mypf.plot_analyzed_image(ContStripesDlg1.Stripes)
        numPickets = str(mypf.num_pickets)
        ContStripesDlg1.Stripes.axes.set_title("No. of pickets found: " + numPickets + "Gantry=0")
        ContStripesDlg1.Stripes.axes.text(5, 25, "Tol=0.5mm,Act_Tol=0.3mm", color='g')
        ContStripesDlg1.Stripes.axes.text(5, 60, "Warning:Picket & leaf indexing starts with 0", color='r')

        ContStripesDlg1.Stripes.axes.arrow(25, 550, 50, 0, head_width=10, head_length=25, fc='b', ec='b')
        ContStripesDlg1.Stripes.axes.arrow(25, 550, 0, -50, head_width=10, head_length=25, fc='b', ec='b')
        ContStripesDlg1.Stripes.axes.text(35, 570, "Count", color='gray')
        ContStripesDlg1.Stripes.axes.text(5, 515, "Count", color='gray', rotation=90)

        ContStripesDlg1.Stripes.axes.set_xlabel("Pixel No. G-T")
        ContStripesDlg1.Stripes.axes.set_ylabel("Pixel No. A-B")
        ContStripesDlg1.exec_()

        self.SaveWidgetScreenShot(ContStripesDlg1, 'PicketFence0.jpg')
        ContStripesDlg1.close()

        if self.Mode == "Manual":
            ContStripesDlg1.Stripes.draw()
            ContStripesDlg1.exec_()
            QtWidgets.QApplication.processEvents()

    def AnalysePicketFence270(self):
        if self.Mode == "Manual":
            files =QtWidgets.QFileDialog(self)
            files.setWindowTitle('Picket Fence 270')
            self.CurrentImages = files.getOpenFileNames(self, caption='Continuous Stripes (1)')

        ContStripesDlg1 = ContStripesDlg.ContStripesWidget(self)
        # ContStripesDlg1.Img=DCMReader.ReadDCMFile(str(self.CurrentImages[0]))

        mypf = PicketFence(str(self.CurrentImages[0]))

        mypf.image.check_inversion()
        mypf.analyze(tolerance=0.5, action_tolerance=0.3, hdmlc=False)
        mypf.save_analyzed_image('PicketFence270', gaurd_rails=True, mlc_peaks=True, overlay=True,
                                 leaf_error_subplot=True)
        # print(mypf.num_pickets,'No. of pickets found')
        # print(mypf.return_results())
        # mypf.plot_analyzed_image()


        AnalyzedImage = pl.imread('PicketFence270.png')
        ContStripesDlg1.Stripes.axes.imshow(AnalyzedImage)
        ContStripesDlg1.ResultsLabel.setText(mypf.return_results())
        # mypf.plot_analyzed_image(ContStripesDlg1.Stripes)
        numPickets = str(mypf.num_pickets)
        ContStripesDlg1.Stripes.axes.set_title("No. of pickets found: " + numPickets + "Gantry=270")
        ContStripesDlg1.Stripes.axes.text(5, 25, "Tol=0.5mm,Act_Tol=0.3mm", color='g')
        ContStripesDlg1.Stripes.axes.text(5, 60, "Warning:Picket & leaf indexing starts with 0", color='r')

        ContStripesDlg1.Stripes.axes.arrow(25, 550, 50, 0, head_width=10, head_length=25, fc='b', ec='b')
        ContStripesDlg1.Stripes.axes.arrow(25, 550, 0, -50, head_width=10, head_length=25, fc='b', ec='b')
        ContStripesDlg1.Stripes.axes.text(35, 570, "Count", color='gray')
        ContStripesDlg1.Stripes.axes.text(5, 515, "Count", color='gray', rotation=90)

        ContStripesDlg1.Stripes.axes.set_xlabel("Pixel No. G-T")
        ContStripesDlg1.Stripes.axes.set_ylabel("Pixel No. A-B")
        ContStripesDlg1.exec_()
        self.SaveWidgetScreenShot(ContStripesDlg1, 'PicketFence270.jpg')


    def AnalysePicketFence90(self):
        if self.Mode == "Manual":
            files =QtWidgets.QFileDialog(self)
            files.setWindowTitle('Picket Fence 90')
            self.CurrentImages = files.getOpenFileNames(self, caption='Continuous Stripes (1)')

        ContStripesDlg1 = ContStripesDlg.ContStripesWidget(self)
        # ContStripesDlg1.Img=DCMReader.ReadDCMFile(str(self.CurrentImages[0]))

        mypf = PicketFence(str(self.CurrentImages[0]))

        mypf.image.check_inversion()
        mypf.analyze(tolerance=0.5, action_tolerance=0.3, hdmlc=False)
        mypf.save_analyzed_image('PicketFence90', gaurd_rails=True, mlc_peaks=True, overlay=True,
                                 leaf_error_subplot=True)
        # print(mypf.num_pickets,'No. of pickets found')
        # print(mypf.return_results())
        # mypf.plot_analyzed_image()


        AnalyzedImage = pl.imread('PicketFence90.png')
        ContStripesDlg1.Stripes.axes.imshow(AnalyzedImage)
        ContStripesDlg1.ResultsLabel.setText(mypf.return_results())
        # mypf.plot_analyzed_image(ContStripesDlg1.Stripes)
        numPickets = str(mypf.num_pickets)
        ContStripesDlg1.Stripes.axes.set_title("No. of pickets found: " + numPickets + "Gantry=90")
        ContStripesDlg1.Stripes.axes.text(5, 25, "Tol=0.5mm,Act_Tol=0.3mm", color='g')
        ContStripesDlg1.Stripes.axes.text(5, 60, "Warning:Picket & leaf indexing starts with 0", color='r')

        ContStripesDlg1.Stripes.axes.arrow(25, 550, 50, 0, head_width=10, head_length=25, fc='b', ec='b')
        ContStripesDlg1.Stripes.axes.arrow(25, 550, 0, -50, head_width=10, head_length=25, fc='b', ec='b')
        ContStripesDlg1.Stripes.axes.text(35, 570, "Count", color='gray')
        ContStripesDlg1.Stripes.axes.text(5, 515, "Count", color='gray', rotation=90)

        ContStripesDlg1.Stripes.axes.set_xlabel("Pixel No. G-T")
        ContStripesDlg1.Stripes.axes.set_ylabel("Pixel No. A-B")

        ContStripesDlg1.exec_()
        self.SaveWidgetScreenShot(ContStripesDlg1, 'PicketFence90.jpg')
        ContStripesDlg1.close()

        if self.Mode == "Manual":
            ContStripesDlg1.Stripes.draw()
            ContStripesDlg1.exec_()

    def AnalyseMLCAlign(self):
        files =QtWidgets.QFileDialog(self)
        files.setWindowTitle('MLC Alignment')
        if self.Mode == "Manual":
            self.CurrentImages = files.getOpenFileNames(self, caption='MLC ALignment (2)')

        MLCAlignDlg1 = MLCAlignDlg.MLCAlignWidget(self)

        MLC1 = DCMReader.ReadDCMFile(str(self.CurrentImages[0]))
        MLCAlignDlg1.Img1 = MLC1

        MLC2 = DCMReader.ReadDCMFile(str(self.CurrentImages[1]))
        MLCAlignDlg1.Img2 = MLC2

        MLCAlignDlg1.Img3 = MLCAlignDlg1.Img1 + MLCAlignDlg1.Img2
        EPIDType = (np.shape(MLC1))

        MLCAlignDlg1.MLCAlignWidget.axes.imshow(MLCAlignDlg1.Img3, cmap='cool')
        MLCAlignDlg1.MLCAlignWidget.axes.set_title('MLC Alignment')
        #MLCAlignDlg1.MLCAlignWidget.axes.hold(True)
        # 1mm x-guard lines
        xLine1 = np.linspace(0, EPIDType[1], 50)
        if EPIDType[0] == 384:
            spacing = 0.784
        else:
            spacing = 0.397
        xLine2 = np.ones(50) * (EPIDType[0] / 2.0) - (0.5 / spacing)  # 0.5 mm away from centreline
        MLCAlignDlg1.MLCAlignWidget.axes.plot(xLine1, xLine2, color='y', linewidth=1)
        xLine3 = np.linspace(0, EPIDType[1], 50)
        xLine4 = np.ones(50) * (EPIDType[0] / 2.0) + (0.5 / spacing)  # 0.5 mm away from centreline
        MLCAlignDlg1.MLCAlignWidget.axes.plot(xLine3, xLine4, color='y', linewidth=1)

        # 1mm y-guard lines
        yLine1 = np.linspace(0, EPIDType[0], 50)
        yLine2 = np.ones(50) * (EPIDType[1] / 2.0) - (0.5 / spacing)  # 0.5 mm away from centreline
        MLCAlignDlg1.MLCAlignWidget.axes.plot(yLine2, yLine1, color='y', linewidth=1)
        yLine3 = np.linspace(0, EPIDType[0], 50)
        yLine4 = np.ones(50) * (EPIDType[1] / 2.0) + (0.5 / spacing)  # 0.5 mm away from centreline
        MLCAlignDlg1.MLCAlignWidget.axes.plot(yLine4, yLine3, color='y', linewidth=1)

        # MLCAlignDlg1.MLCAlignWidget.axes.plot(self.Iso[0],self.Iso[1],'y+',markersize=20)
        MLCAlignDlg1.MLCAlignWidget.axes.set_xlim(0, EPIDType[1])
        MLCAlignDlg1.MLCAlignWidget.axes.set_ylim(0, EPIDType[0])
        MLCAlignDlg1.MLCAlignWidget.axes.set_xlabel('Pixel No. A-B', fontsize=8)
        MLCAlignDlg1.MLCAlignWidget.axes.set_ylabel('Pixel No. T-G', fontsize=8)
        MLCAlignDlg1.MLCAlignWidget.draw()
        self.SaveWidgetScreenShot(MLCAlignDlg1.MLCAlignWidget, 'MLCAlignment.jpg')
        MLCAlignDlg1.exec_()

        if self.Mode == "Manual":
            MLCAlignDlg1.show()


    def AutoReportMonthlyMLCQA(self):
        self.Mode = "Auto"
        dirPath = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory","\\\\NAS-8TB-RADONC\\ARIAdata\\MVimages\\"))
        files = os.listdir(dirPath)
        files = sorted(files)

        for x in range(0, np.size(files), 1):
            files[x] = dirPath + '\\' + files[x]
        if (np.size(files) != 9):
            errorMsg = QtWidgets.QErrorMessage(self)
            errorMsg.setWindowTitle("Error")
            errorMsg.showMessage("No. of files must be 9 for monthly QA", "Error")
            errorMsg.exec_()
        else:
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            # MLC Alignment
            self.CurrentImages.append(files[0])
            self.CurrentImages.append(files[1])
            self.AnalyseMLCAlign()
            self.CurrentImages.clear()

            # Picket Fence- Gantry =0
            self.CurrentImages.append(files[2])
            self.AnalysePicketFence0()
            self.CurrentImages.clear()

            # Picket Fence- Gantry =270
            self.CurrentImages.append(files[3])
            self.AnalysePicketFence270()
            self.CurrentImages.clear()

            # Picket Fence- Gantry =90
            self.CurrentImages.append(files[4])
            self.AnalysePicketFence90()
            self.CurrentImages.clear()

            # X-Wedges
            self.WedgeType = 'X'
            self.CurrentImages.append(files[5])
            self.CurrentImages.append(files[6])
            self.AnalyseWedges("X")
            self.CurrentImages.clear()

            # Y-Wedges
            self.WedgeType = 'Y'
            self.CurrentImages.append(files[7])
            self.CurrentImages.append(files[8])
            self.AnalyseWedges("Y")
            self.CurrentImages.clear()

            # Restore normal cursor
            QtWidgets.QApplication.restoreOverrideCursor()

            # Create a PDF report
            self.CreatePDFReportMLCMonthlyQA()

            # Revert back to manual mode
            self.Mode = "Manual"
            os.startfile(self.reportStr)


    def CreatePDFReportMLCMonthlyQA(self):
        mcID =QtWidgets.QInputDialog.getText(self, "Enter M/C ID", "M/C ID:", 0)
        #mcID = QtGui.QComboBox(self,"M/C ID:")
        msrBy =QtWidgets.QInputDialog.getText(self, "Initials", "Measured by:", 0)
        if mcID[1] == True and msrBy[1] == True:
            # Setting up header & preparing page
            today = date.today()
            day = str(today.day)
            month = str(today.month)
            year = str(today.year)
            dateStr = day + '_' + month + '_' + year
            mcIDStr = "MC ID:" + mcID[0]
            # self.reportStr = "D:\\MLC QA\\" + str(mcID[0]) + "\\MLCQA" + "_" + dateStr + '.pdf'
            #self.reportStr = "D:\\" + "Projects\\"+"RTQA\\"+ "CurrentReport" + '.pdf'
            self.reportStr="\\\\NAS-8TB-RADONC\\ARIAdata\\MLCQA Reports"+"\\"+str(mcID[0])+"\\"+dateStr + '.pdf'
            c = canvas.Canvas(self.reportStr, pagesize=A4)
            c.drawImage('Logo.png', 350, 775, 8 * cm, 1.75 * cm)
            text1 = "MLC QA Report:" + dateStr
            c.drawString(100, 800, text1)
            c.drawString(100, 750, mcIDStr)

            # MLC Bank Alignment
            c.line(50, 700, 580, 700)
            c.drawString(250, 675, "MLC Bank Alignment")
            c.drawImage('MLCAlignment.jpg', 100, 150, 15 * cm, 18 * cm, preserveAspectRatio=True)
            text2 = 'Measured by:    ' + str(msrBy[0])
            text3 = 'Checked by:_______________'
            c.drawString(100, 80, text2)
            c.drawString(100, 50, text3)
            c.line(50, 125, 580, 125)

            # Picket fence#Gantry=0
            c.showPage()  # Move to next page
            c.line(50, 700, 580, 700)
            c.drawString(250, 675, "Picket Fence Gantry=0")
            c.drawImage('PicketFence0.jpg', 100, 150, 13 * cm, 18 * cm, preserveAspectRatio=True)
            text2 = 'Measured by:    ' + str(msrBy[0])
            text3 = 'Checked by:_______________'
            c.drawString(100, 80, text2)
            c.drawString(100, 50, text3)
            c.line(50, 125, 580, 125)

            # Picket fence#Gantry=270
            c.showPage()  # Move to next page
            c.line(50, 700, 580, 700)
            c.drawString(250, 675, "Picket Fence Gantry=270")
            c.drawImage('PicketFence270.jpg', 100, 150, 13 * cm, 18 * cm, preserveAspectRatio=True)
            text2 = 'Measured by:    ' + str(msrBy[0])
            text3 = 'Checked by:_______________'
            c.drawString(100, 80, text2)
            c.drawString(100, 50, text3)
            c.line(50, 125, 580, 125)

            # Picket fence#Gantry=90
            c.showPage()  # Move to next page
            c.line(50, 700, 580, 700)
            c.drawString(250, 675, "Picket Fence Gantry=90")
            c.drawImage('PicketFence90.jpg', 100, 150, 13 * cm, 18 * cm, preserveAspectRatio=True)
            text2 = 'Measured by:    ' + str(msrBy[0])
            text3 = 'Checked by:_______________'
            c.drawString(100, 80, text2)
            c.drawString(100, 50, text3)
            c.line(50, 125, 580, 125)

            # X-Wedges
            c.showPage()  # Move to next page
            c.line(50, 700, 580, 700)
            c.drawString(270, 675, "XWedges")
            c.drawImage('XWedges.jpg', 100, 150, 15 * cm, 18 * cm, preserveAspectRatio=True)
            text2 = 'Measured by:    ' + str(msrBy[0])
            text3 = 'Checked by:_______________'
            c.drawString(100, 80, text2)
            c.drawString(100, 50, text3)
            c.line(50, 125, 580, 125)

            # Y-Wedges
            c.showPage()  # Move to next page
            c.line(50, 700, 580, 700)
            c.drawString(270, 675, "YWedges")
            c.drawImage('YWedges.jpg', 100, 150, 15 * cm, 18 * cm, preserveAspectRatio=True)
            text2 = 'Measured by:    ' + str(msrBy[0])
            text3 = 'Checked by:_______________'
            c.drawString(100, 80, text2)
            c.drawString(100, 50, text3)
            c.line(50, 125, 580, 125)

            # Save the PDF to database -"D:\MLC QA\LA ID" LA ID=LA1/LA2/LA3/LA4
            c.save()
            os.startfile(self.reportStr)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = StartQT()
    myapp.show()
    myapp.setWindowTitle('RT QA')
    sys.exit(app.exec_())

