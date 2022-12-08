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


# AUTO-Connect with ui file
ui,_ = loadUiType(os.path.join(os.path.dirname(__file__),'first_gui.ui'))

class Dicom_Viewer_App(QMainWindow , ui):
    def __init__(self , parent=None):
        super(Dicom_Viewer_App , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        # Global variables
        self.data_set_path=""
        self.volume3d=""
        self.flag = 0
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QtCore.Qt.white)
        painter.drawLine(0, 0, 200, 200)
        self.sliders_list = [self.AxialHorizontalSlider,
                            self.SagittalHorizontalSlider,
                            self.CoronalHorizontalSlider,
                            self.AxialVerticalSlider,
                            self.SagittalVerticalSlider,
                            self.CoronalVerticalSlider]
        self.handle_buttons()
        
        
        
        self.set_sliders()
        self.obliqueLineSlider.valueChanged.connect(self.viewing_planes)
        self.obliqueLineSlopeSlider.valueChanged.connect(self.viewing_planes)
        self.startPoint = [0,0]
        self.obliqueLine_slope = 1
            
        self.axialSlice = 117
        self.sagittalSlice = 256
        self.coronalSlice = 256

        for i, slider in enumerate(self.sliders_list):
          if i ==0:
            #slider.setValue(self.sagittalSlice)
            slider.valueChanged.connect(self.Axial_H_changed)
          if i ==3:
            #slider.setValue(-self.coronalSlice)
            slider.valueChanged.connect(self.Axial_V_changed)
          if i ==1:
          #  slider.setValue(self.axialSlice)
            slider.valueChanged.connect(self.Sagittal_H_changed)
          if i ==4:  
           # slider.setValue(-self.coronalSlice)
            slider.valueChanged.connect(self.Sagittal_V_changed)
          if i ==2:  
            #slider.setValue(self.axialSlice)
            slider.valueChanged.connect(self.Coronal_H_changed)
          if i ==5:  
            #slider.setValue(-self.sagittalSlice)
            slider.valueChanged.connect(self.Coronal_V_changed)
       


           
    def set_sliders(self):
        self.obliqueLineSlopeSlider.setValue(0)
        self.obliqueLineSlopeSlider.setMinimum(-512)
        self.obliqueLineSlopeSlider.setMaximum(512)
        self.obliqueLineSlopeSlider.setTickInterval(1)

        self.obliqueLineSlider.setValue(0)
        self.obliqueLineSlider.setMinimum(-512)
        self.obliqueLineSlider.setMaximum(512)
        self.obliqueLineSlider.setTickInterval(1)
        
    def Axial_H_changed(self):
        self.sagittalSlice = self.AxialHorizontalSlider.value()
        self.viewing_planes()
        

    def Axial_V_changed(self):
        self.coronalSlice = -self.AxialVerticalSlider.value()
        self.viewing_planes()

    def Sagittal_H_changed(self):
        self.axialSlice = self.SagittalHorizontalSlider.value()
        self.viewing_planes()

    def Sagittal_V_changed(self):
        self.coronalSlice = -self.SagittalVerticalSlider.value()
        self.viewing_planes()

    def Coronal_H_changed(self):
        self.axialSlice = self.CoronalHorizontalSlider.value()
        self.viewing_planes()

    def Coronal_V_changed(self):
        self.sagittalSlice = -self.CoronalVerticalSlider.value()
        self.viewing_planes()

    def Graphic_Scene(self,fig_width,fig_height,view,bool=True):
        '''Setting up a canvas to view an image in its graphics view'''
        scene= QGraphicsScene()
        figure = Figure(figsize=(fig_width/90, fig_height/90),dpi = 90)
        canvas = FigureCanvas(figure)
        axes = figure.add_subplot()
        scene.addWidget(canvas)
        # scene.addWidget(self.dial)
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
        '''Connect Browse Button with brosw_dicom_folder function'''
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
        '''Convert dicom image to 3d volume'''
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

        self.set_sliders_limits(self.sliders_list )
        # viewing planes
        self.viewing_planes()


    def set_sliders_limits(self, sliders):
        '''Declaring sliders limitations'''
        for i, slider in enumerate(sliders):
            # slider.setValue()
            if i > 2 :
                if i == 3:
                    slider.setMinimum(-self.volume3d.shape[1]+2)
                    slider.setMaximum(0)
                    slider.setTickInterval(1)
                    slider.setValue(-self.volume3d.shape[1]//2)
                else:
                    slider.setMinimum(-self.volume3d.shape[1]+2)
                    slider.setMaximum(0)
                    slider.setTickInterval(1)
                    slider.setValue(-self.volume3d.shape[1]//2)
            if i == 0:
                slider.setMinimum(0)
                slider.setMaximum(self.volume3d.shape[0]-2)
                slider.setTickInterval(1)
                slider.setValue(self.volume3d.shape[0]//2)
            if (i ==1 or i ==2):
                slider.setMinimum(0)
                slider.setTickInterval(1)
                slider.setMaximum(self.volume3d.shape[2]-2)
                slider.setValue(self.volume3d.shape[2]//2)


    def onclick(self,event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
            ('double' if event.dblclick else 'single', event.button,
            event.x, event.y, event.xdata, event.ydata))
        
        self.obliqueLine.set_visible(False)
        self.obliqueLine_slope = ((event.ydata- self.startPoint[1])/(event.xdata- self.startPoint[0]))
        print(event.xdata/event.ydata)
        print(abs(self.obliqueLine_slope))
        self.obliqueLine = self.axial_axis.axline(self.startPoint,slope=abs(self.obliqueLine_slope))
        self.obliqueLine.set_visible(True)
        self.axial_figure.canvas.draw_idle()
        self.axial_figure.canvas.flush_events()
        #self.viewing_planes()


    def viewing_planes(self):
        '''Creating the plains figures and axes and plotting slices on them'''

        # Initialize figure and axis for every plane
        self.axial_figure, self.axial_axis = self.Graphic_Scene(210, 170, self.Axial_Plane)
        self.sagittal_figure, self.sagittal_axis = self.Graphic_Scene(210, 170, self.Sagittal_Plane)
        self.coronal_figure, self.coronal_axis = self.Graphic_Scene(210, 170, self.Coronal_Plane)

        # Plot a slice on every plane
        self.axial_axis.imshow((self.volume3d[:,:,self.axialSlice]), cmap="gray")
        self.sagittal_axis.imshow((self.volume3d[:,self.sagittalSlice,:]), cmap="gray")
        self.coronal_axis.imshow((self.volume3d[self.coronalSlice,:,:]), cmap="gray")

        if self.obliqueLineSlopeSlider.value() > 0:
            self.obliqueLine_slope = ((512-self.obliqueLineSlopeSlider.value()- self.startPoint[1])/(512- self.startPoint[0]))
        elif self.obliqueLineSlopeSlider.value() < 0:
            self.obliqueLine_slope = ((512- self.startPoint[1])/(512+self.obliqueLineSlopeSlider.value()-self.startPoint[1]))

        if self.obliqueLineSlider.value() > 0:
            self.startPoint = [self.obliqueLineSlider.value(), 0]
        else:
            self.startPoint = [0, -self.obliqueLineSlider.value()]


        self.obliqueLine = self.axial_axis.axline(self.startPoint,slope=self.obliqueLine_slope)
        self.obliqueLine.set_visible(True)
        self.axial_axis.axhline(y = -self.AxialVerticalSlider.value(), color = 'b', label = 'axvline - full height')
        self.axial_axis.axvline(x = self.AxialHorizontalSlider.value(), color = 'b', label = 'axvline - full height')
        self.sagittal_axis.axhline(y = -self.SagittalVerticalSlider.value(), color = 'b', label = 'axvline - full height')
        self.sagittal_axis.axvline(x = self.SagittalHorizontalSlider.value(), color = 'b', label = 'axvline - full height')
        self.coronal_axis.axhline(y = -self.CoronalVerticalSlider.value(), color = 'b', label = 'axvline - full height')
        self.coronal_axis.axvline(x = self.CoronalHorizontalSlider.value(), color = 'b', label = 'axvline - full height') 

        self.axial_figure.canvas.mpl_connect('button_press_event', self.onclick)

        self.show()



if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Dicom_Viewer_App()
    window.show()
    app.exec_()