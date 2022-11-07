import sys
import pydicom as dicom # For reading dicom image
import numpy as np
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib 
matplotlib.use('Qt5Agg')
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import os 



ui,_ = loadUiType(os.path.join(os.path.dirname(__file__),'first_gui.ui'))

class Dicom_Viewer_App(QMainWindow , ui):
    def __init__(self , parent=None):
        super(Dicom_Viewer_App , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        # Global variables
        self.data_set_path=""
        self.volume3d=""
        self.handle_buttons()
        self.AxialHorizontalSlider.valueChanged.connect(self.viewing_planes)
        self.AxialVerticalSlider.valueChanged.connect(self.viewing_planes)
        self.SagittalHorizontalSlider.valueChanged.connect(self.viewing_planes)
        self.SagittalVerticalSlider.valueChanged.connect(self.viewing_planes)
        self.CoronalHorizontalSlider.valueChanged.connect(self.viewing_planes)
        self.CoronalVerticalSlider.valueChanged.connect(self.viewing_planes)
        
        


    def Graphic_Scene(self,fig_width,fig_height,view,bool=True):
        '''Setting up a canvas to view an image in its graphics view'''
        scene= QGraphicsScene()
        figure = Figure(figsize=(fig_width/90, fig_height/90),dpi = 90)
        canvas = FigureCanvas(figure)
        axes = figure.add_subplot()
        scene.addWidget(canvas)
        view.setScene(scene)
        if bool ==True:
            figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
            axes.get_xaxis().set_visible(False)
            axes.get_yaxis().set_visible(False)
        else:
            axes.get_xaxis().set_visible(True)
            axes.get_yaxis().set_visible(True)
        self.show()
        return figure,axes
      

    def handle_buttons(self):
        self.Browse_Button.clicked.connect(self.browse_dicom_folder)

    def browse_dicom_folder(self):    
        '''Browse to get Dicom Folder'''
        #Getting folder path
        self.data_set_path = QFileDialog.getExistingDirectory(self,"Select Dicom Folder",directory='.')
        if (self.data_set_path == ""):
            return
        else:
           self.build_3d_volume()

    def build_3d_volume(self):
        head_images = os.listdir(self.data_set_path)

        # Getting the images slices
        # Reading Dicom images/slices
        slices = [dicom.read_file(self.data_set_path + '/' + s, force= True) for s in head_images]


        # Initializing the 3-D mattrix
        img_shape = list(slices[0].pixel_array.shape)
        img_shape.append(len(slices))
        self.volume3d=np.zeros(img_shape)

        # Converting dicom image to 3D Mattrix
        for i,s in enumerate(slices):
            array2D=s.pixel_array
            self.volume3d[:,:,i]= array2D

        self.set_sliders_limits([self.AxialHorizontalSlider, self.SagittalHorizontalSlider, self.CoronalHorizontalSlider, self.AxialVerticalSlider, self.SagittalVerticalSlider, self.CoronalVerticalSlider])

        # viewing plane
        self.viewing_planes()
        # self.viewing_planes(self.Coronal_Plane)
        # self.viewing_planes(self.Sagittal_Plane)

    def set_sliders_limits(self, sliders):
        for i, slider in enumerate(sliders):
            slider.setValue(0)
            slider.setTickInterval(1)
            if i > 2 :
                slider.setMaximum(0)
                if i == 3:
                    slider.setMinimum(-self.volume3d.shape[1])
                else:
                    slider.setMinimum(-self.volume3d.shape[2])
            else:
                slider.setMinimum(0)
                slider.setMaximum(self.volume3d.shape[0])

        # self.AxialHorizontalSlider.setMinimum(0)
        # self.AxialHorizontalSlider.setMaximum(self.volume3d.shape[0])
        # self.AxialHorizontalSlider.setValue(0)
        # self.AxialHorizontalSlider.setTickInterval(1)

        # self.AxialVerticalSlider.setMinimum(-self.volume3d.shape[1])
        # self.AxialVerticalSlider.setMaximum(0)
        # self.AxialVerticalSlider.setValue(0)
        # self.AxialVerticalSlider.setTickInterval(1)

        # self.SagittalHorizontalSlider.setMinimum(0)
        # self.SagittalHorizontalSlider.setMaximum(self.volume3d.shape[0])
        # self.SagittalHorizontalSlider.setValue(0)
        # self.SagittalHorizontalSlider.setTickInterval(1)

        # self.SagittalVerticalSlider.setMinimum(-self.volume3d.shape[2])
        # self.SagittalVerticalSlider.setMaximum(0)
        # self.SagittalVerticalSlider.setValue(0)
        # self.SagittalVerticalSlider.setTickInterval(1)

        # self.CoronalHorizontalSlider.setMinimum(0)
        # self.CoronalHorizontalSlider.setMaximum(self.volume3d.shape[0])
        # self.CoronalHorizontalSlider.setValue(0)
        # self.CoronalHorizontalSlider.setTickInterval(1)

        # self.CoronalVerticalSlider.setMinimum(-self.volume3d.shape[2])
        # self.CoronalVerticalSlider.setMaximum(0)
        # self.CoronalVerticalSlider.setValue(0)
        # self.CoronalVerticalSlider.setTickInterval(1)

    def viewing_planes(self):    
        self.axial_figure, self.axial_axis = self.Graphic_Scene(201, 170, self.Axial_Plane)
        self.sagittal_figure, self.sagittal_axis = self.Graphic_Scene(201, 170, self.Sagittal_Plane)
        self.coronal_figure, self.coronal_axis = self.Graphic_Scene(201, 170, self.Coronal_Plane)

        self.axial_axis.imshow(self.volume3d[:,:,0], cmap="gray") # first slice in z
        self.sagittal_axis.imshow(np.rot90(self.volume3d[:,256,:]), cmap="gray") 
        self.coronal_axis.imshow(np.rot90(self.volume3d[256,:,:]), cmap="gray")
         
        # self.axial_axis.axvline(x = 50, color = 'b', label = 'axvline - full height')
        # self.show()
        #self.draw()
        self.OnSlidersChange(self.AxialHorizontalSlider,self.axial_axis,False)
        self.OnSlidersChange(self.AxialVerticalSlider,self.axial_axis,True)
        self.OnSlidersChange(self.SagittalHorizontalSlider,self.sagittal_axis,False)
        self.OnSlidersChange(self.SagittalVerticalSlider,self.sagittal_axis,True)
        self.OnSlidersChange(self.CoronalHorizontalSlider,self.coronal_axis,False)
        self.OnSlidersChange(self.CoronalVerticalSlider,self.coronal_axis,True)
        #self.AxialHorizontalSlider_changed()
        #self.AxialVerticalSlider_changed()
        # self.SagittalHorizontalSlider_changed()
        # self.SagittalVerticalSlider_changed()
        # self.CoronalHorizontalSlider_changed()
        # self.CoronalVerticalSlider_changed()

        
            
    def OnSlidersChange(self, slider, axes, isVertical):
        my_value = slider.value()
        if isVertical:
            axes.axhline(y = -my_value, color = 'b', label = 'axvline - full height')
        else:
            axes.axvline(x = my_value, color = 'b', label = 'axvline - full height')
        self.show()
        print(my_value)

    # def AxialHorizontalSlider_changed(self):
    #     my_value = self.AxialHorizontalSlider.value()
    #     self.axial_axis.axvline(x = my_value, color = 'b', label = 'axvline - full height')
    #     self.show()
    #     print(my_value)

    # def AxialVerticalSlider_changed(self):
    #     my_value = self.AxialVerticalSlider.value()
    #     self.axial_axis.axhline(y = -my_value, color = 'b', label = 'axvline - full height')
    #     self.show()
    #     print(my_value)

    # def SagittalHorizontalSlider_changed(self):
    #     my_value = self.SagittalHorizontalSlider.value()
    #     self.sagittal_axis.axvline(x = my_value, color = 'b', label = 'axvline - full height')
    #     self.show()
    #     print(my_value)

    # def SagittalVerticalSlider_changed(self):
    #     my_value = self.SagittalVerticalSlider.value()
    #     self.sagittal_axis.axhline(y = -my_value, color = 'b', label = 'axvline - full height')
    #     self.show()
    #     print(my_value)
        
    # def CoronalHorizontalSlider_changed(self):
    #     my_value = self.CoronalHorizontalSlider.value()
    #     self.coronal_axis.axvline(x = my_value, color = 'b', label = 'axvline - full height')
    #     self.show()
    #     print(my_value)

    # def CoronalVerticalSlider_changed(self):
    #     my_value = self.CoronalVerticalSlider.value()
    #     self.coronal_axis.axhline(y = -my_value, color = 'b', label = 'axvline - full height')
    #     self.show()
    #     print(my_value)
    

        



if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1" 
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Dicom_Viewer_App()
    window.show()
    app.exec_()        