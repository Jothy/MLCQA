import dicom as dcm
import numpy as np
import matplotlib.pyplot as plt
from dicom.dataset import Dataset, FileDataset
import dicom.UID
import datetime, time

from skimage.filters import sobel



f1='H:\\MLC QA\\Imgs\\20150814_MLCQA\\ContStripes.dcm'
##mypf = PicketFence(f1)
##mypf.analyze(tolerance=0.15, action_tolerance=0.03)
##print(mypf.return_results())
##mypf.plot_analyzed_image()


def ReadDCMFile(fp):
    Img=dcm.read_file(fp)
    Slope=Img.RescaleSlope
    Intercept=Img.RescaleIntercept
    #print Slope,Intercept
    #convert raw values to actual values
    #V=(slope*rawValue)+intercept
    Img=(Img.pixel_array*Slope)+Intercept
    return Img


def GetNumFrames(fp):
    Data=dcm.read_file(fp)
    Descrp=Data.RTImageDescription
    FrameStr=Descrp.split(sep='\r\n')
    Frames=FrameStr[2].split(sep='Averaged Frames')[1]
    return float(Frames)




def WriteDCMFile(pixel_array,filename):
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = 'RT Image Storage'
    file_meta.MediaStorageSOPInstanceUID = '1.3.6.1.4.1.9590.100.1.1.111165684411017669021768385720736873780'
    file_meta.ImplementationClassUID = '1.3.6.1.4.1.9590.100.1.0.100.4.0'
    ds = FileDataset(filename, {},file_meta = file_meta,preamble="\0"*128)
    ds.Modality = 'RTIMAGE'
    ds.ContentDate = str(datetime.date.today()).replace('-','')
    ds.ContentTime = str(time.time()) #milliseconds since the epoch
    ds.StudyInstanceUID =  '1.3.6.1.4.1.9590.100.1.1.124313977412360175234271287472804872093'
    ds.SeriesInstanceUID = '1.3.6.1.4.1.9590.100.1.1.369231118011061003403421859172643143649'
    ds.SOPInstanceUID =    '1.3.6.1.4.1.9590.100.1.1.111165684411017669021768385720736873780'
    ds.SOPClassUID = 'RT Image Storage'
    ds.SecondaryCaptureDeviceManufacturer = 'Varian Medical Systems'

    ## These are the necessary imaging components of the FileDataset object.
    ds.SamplesPerPixel = 1
    ds.ImagePlanePixelSpacing=[0.392,0.392]
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelRepresentation = 0
    ds.HighBit = 15
    ds.BitsStored = 16
    ds.BitsAllocated = 16
    # ds.SmallestImagePixelValue = '\\x00\\x00'
    # ds.LargestImagePixelValue = '\\xff\\xff'
    ds.Columns =1024# pixel_array.shape[0]
    ds.Rows =764# pixel_array.shape[1]
    ds.RescaleSlope=1.0
    ds.RescaleIntercept=1.0
    # if type(pixel_array) != np.uint16:
    #     pixel_array =np.uint16(pixel_array)
    ds.PixelData = pixel_array
    ds.save_as(filename,write_like_original=True)
    return




