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
import pyqtgraph as pg
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

        # self.Axial_Plane = pg.InfiniteLine(angle=135, movable=True, pen='g')
        self.sliders_list = [self.AxialHorizontalSlider,
                            self.SagittalHorizontalSlider,
                            self.CoronalHorizontalSlider,
                            self.AxialVerticalSlider,
                            self.SagittalVerticalSlider,
                            self.CoronalVerticalSlider]
       

        self.handle_buttons()


        # self.AxialHorizontalSlider.valueChanged.connect(self.AxialHorizontalSliderChange)

        for i, slider in enumerate(self.sliders_list):
          if i ==0:
            slider.valueChanged.connect(self.Axial_H_changed)
          if i ==3:
            slider.valueChanged.connect(self.Axial_V_changed)
          if i ==1:
            slider.valueChanged.connect(self.Sagittal_H_changed)
          if i ==4:
            slider.valueChanged.connect(self.Sagittal_V_changed)
          if i ==2:
             slider.valueChanged.connect(self.Coronal_H_changed)
          if i ==5:
             slider.valueChanged.connect(self.Coronal_V_changed)





        self.current_A_H_value = 0
        self.current_A_V_value = 0
        self.current_S_H_value = 0
        self.current_S_V_value = 0
        self.current_C_H_value = 0
        self.current_C_V_value = 0

        # for slider in self.sliders_list:
        #     slider.valueChanged.connect(self.value_changed)
        #     slider.valueChanged.connect(self.viewing_planes)



    def Axial_H_changed(self):
        # self.flag=1
        self.axial_figure, self.axial_axis = self.Graphic_Scene(210, 170, self.Axial_Plane)
        self.sagittal_figure, self.sagittal_axis = self.Graphic_Scene(210, 170, self.Sagittal_Plane)
        self.coronal_figure, self.coronal_axis = self.Graphic_Scene(210, 170, self.Coronal_Plane)
        self.obliqueLine = self.axial_axis.axline([0,0],slope=1)
        self.obliqueLine.set_visible(True)
        self.current_A_H_value = self.AxialHorizontalSlider.value()
        self.coronal_axis.imshow((self.volume3d[256,:,:]), cmap="gray")
        self.axial_axis.imshow((self.volume3d[:,:,0]), cmap="gray")
        self.sagittal_axis.imshow((self.volume3d[:,self.current_A_H_value,:]), cmap="gray")
        self.axial_axis.axhline(y = self.current_A_V_value, color = 'b', label = 'axvline - full height')
        self.axial_axis.axvline(x = self.current_A_H_value, color = 'b', label = 'axvline - full height')
        self.show()

    def Axial_V_changed(self):
        # self.flag=1
        self.axial_figure, self.axial_axis = self.Graphic_Scene(210, 170, self.Axial_Plane)
        self.sagittal_figure, self.sagittal_axis = self.Graphic_Scene(210, 170, self.Sagittal_Plane)
        self.coronal_figure, self.coronal_axis = self.Graphic_Scene(210, 170, self.Coronal_Plane)
        self.obliqueLine = self.axial_axis.axline([0,0],slope=1)
        self.obliqueLine.set_visible(True)
        self.current_A_V_value = self.AxialVerticalSlider.value()
        self.sagittal_axis.imshow((self.volume3d[:,256,:]), cmap="gray")
        self.axial_axis.imshow((self.volume3d[:,:,0]), cmap="gray")
        self.coronal_axis.imshow((self.volume3d[self.current_A_V_value,:,:]), cmap="gray")
        self.axial_axis.axhline(y = -self.current_A_V_value, color = 'b', label = 'axvline - full height')
        self.axial_axis.axvline(x = self.current_A_H_value, color = 'b', label = 'axvline - full height')
        self.show()
    def Sagittal_H_changed(self):
        # self.flag=1
        self.axial_figure, self.axial_axis = self.Graphic_Scene(210, 170, self.Axial_Plane)
        self.sagittal_figure, self.sagittal_axis = self.Graphic_Scene(210, 170, self.Sagittal_Plane)
        self.coronal_figure, self.coronal_axis = self.Graphic_Scene(210, 170, self.Coronal_Plane)
        self.obliqueLine = self.axial_axis.axline([0,0],slope=1)
        self.obliqueLine.set_visible(True)
        self.current_S_H_value = self.SagittalHorizontalSlider.value()
        self.axial_axis.imshow((self.volume3d[:,:,self.current_S_H_value]), cmap="gray")
        self.sagittal_axis.imshow((self.volume3d[:,256,:]), cmap="gray")
        self.coronal_axis.imshow((self.volume3d[256,:,:]), cmap="gray")
        self.sagittal_axis.axhline(y = -self.current_S_V_value, color = 'b', label = 'axvline - full height')
        self.sagittal_axis.axvline(x = self.current_S_H_value, color = 'b', label = 'axvline - full height')
        self.show()

    def Sagittal_V_changed(self):
        # self.flag=1
        self.axial_figure, self.axial_axis = self.Graphic_Scene(210, 170, self.Axial_Plane)
        self.sagittal_figure, self.sagittal_axis = self.Graphic_Scene(210, 170, self.Sagittal_Plane)
        self.coronal_figure, self.coronal_axis = self.Graphic_Scene(210, 170, self.Coronal_Plane)
        self.obliqueLine = self.axial_axis.axline([0,0],slope=1)
        self.obliqueLine.set_visible(True)
        self.current_S_V_value = self.SagittalVerticalSlider.value()

        self.axial_axis.imshow((self.volume3d[:,:,0]), cmap="gray")
        self.sagittal_axis.imshow((self.volume3d[:,256,:]), cmap="gray")
        self.coronal_axis.imshow((self.volume3d[self.current_S_V_value,:,:]), cmap="gray")

        self.sagittal_axis.axhline(y = -self.current_S_V_value, color = 'b', label = 'axvline - full height')
        self.sagittal_axis.axvline(x = self.current_S_H_value, color = 'b', label = 'axvline - full height')
        self.show()

    def Coronal_H_changed(self):
          # self.flag=1
        self.axial_figure, self.axial_axis = self.Graphic_Scene(210, 170, self.Axial_Plane)
        self.sagittal_figure, self.sagittal_axis = self.Graphic_Scene(210, 170, self.Sagittal_Plane)
        self.coronal_figure, self.coronal_axis = self.Graphic_Scene(210, 170, self.Coronal_Plane)
        self.obliqueLine = self.axial_axis.axline([0,0],slope=1)
        self.obliqueLine.set_visible(True)
        self.current_C_H_value = self.CoronalHorizontalSlider.value()

        self.axial_axis.imshow((self.volume3d[:,:,self.current_C_H_value]), cmap="gray")
        self.sagittal_axis.imshow((self.volume3d[:,256,:]), cmap="gray")
        self.coronal_axis.imshow((self.volume3d[256,:,:]), cmap="gray")

        self.coronal_axis.axhline(y = -self.current_C_V_value, color = 'b', label = 'axvline - full height')
        self.coronal_axis.axvline(x = self.current_C_H_value, color = 'b', label = 'axvline - full height')
        self.show()

    def Coronal_V_changed(self):
          # self.flag=1
        self.axial_figure, self.axial_axis = self.Graphic_Scene(210, 170, self.Axial_Plane)
        self.sagittal_figure, self.sagittal_axis = self.Graphic_Scene(210, 170, self.Sagittal_Plane)
        self.coronal_figure, self.coronal_axis = self.Graphic_Scene(210, 170, self.Coronal_Plane)

        self.obliqueLine = self.axial_axis.axline([0,0],slope=1)
        self.obliqueLine.set_visible(True)

        self.current_C_V_value = self.CoronalVerticalSlider.value()

        self.axial_axis.imshow((self.volume3d[:,:,0]), cmap="gray")
        self.sagittal_axis.imshow((self.volume3d[:,self.current_C_V_value,:]), cmap="gray")
        self.coronal_axis.imshow((self.volume3d[256,:,:]), cmap="gray")

        self.coronal_axis.axhline(y = -self.current_C_V_value, color = 'b', label = 'axvline - full height')
        self.coronal_axis.axvline(x = self.current_C_H_value, color = 'b', label = 'axvline - full height')
        self.show()

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

        self.set_sliders_limits(self.sliders_list)
        # viewing planes
        self.viewing_planes()


    def set_sliders_limits(self, sliders):
        '''Declaring sliders limitations'''

        for i, slider in enumerate(sliders):
            if i > 2 :
                if i == 3:
                    slider.setValue(-self.volume3d.shape[1]//2)
                    slider.setMinimum(-self.volume3d.shape[1])
                    slider.setMaximum(0)
                    slider.setTickInterval(1)
                else:
                    slider.setValue(-self.volume3d.shape[1]//2)
                    slider.setMinimum(-self.volume3d.shape[1])
                    slider.setMaximum(0)
                    slider.setTickInterval(1)
            if i == 0:
                slider.setValue(self.volume3d.shape[1]//2)
                slider.setMinimum(0)
                slider.setMaximum(self.volume3d.shape[1])
                slider.setTickInterval(1)
            if (i ==1 or i ==2):
                slider.setValue(self.volume3d.shape[2]//2)
                slider.setMinimum(0)
                slider.setTickInterval(1)
                slider.setMaximum(self.volume3d.shape[2])




    def viewing_planes(self):
        '''Creating the plains figures and axes and plotting slices on them'''

        # Initialize figure and axis for every plane
        self.axial_figure, self.axial_axis = self.Graphic_Scene(210, 170, self.Axial_Plane)
        self.sagittal_figure, self.sagittal_axis = self.Graphic_Scene(210, 170, self.Sagittal_Plane)
        self.coronal_figure, self.coronal_axis = self.Graphic_Scene(210, 170, self.Coronal_Plane)


        # Plot a slice on every plane
        self.axial_axis.imshow((self.volume3d[:,:,0]), cmap="gray")
        self.sagittal_axis.imshow((self.volume3d[:,256,:]), cmap="gray")
        self.coronal_axis.imshow((self.volume3d[256,:,:]), cmap="gray")

        self.obliqueLine = self.axial_axis.axline([0,0],slope=1)
        self.obliqueLine.set_visible(True)

        self.axial_axis.axhline(y = 256, color = 'b', label = 'axvline - full height')
        self.axial_axis.axvline(x = 256, color = 'b', label = 'axvline - full height')
        self.sagittal_axis.axhline(y = 256, color = 'b', label = 'axvline - full height')
        self.sagittal_axis.axvline(x = 117, color = 'b', label = 'axvline - full height')
        self.coronal_axis.axhline(y = 256, color = 'b', label = 'axvline - full height')
        self.coronal_axis.axvline(x = 117, color = 'b', label = 'axvline - full height')
        self.show()
        self.axial_figure.canvas.mpl_connect('button_press_event', self.onclick)
        # Calling OnsliderChange function to change line position
        # if (self.flag ==1):
        #     self.OnSlidersChange(self.AxialHorizontalSlider,self.axial_axis,False)
        #     self.OnSlidersChange(self.AxialVerticalSlider,self.axial_axis,True)
        #     self.OnSlidersChange(self.SagittalHorizontalSlider,self.sagittal_axis,False)
        #     self.OnSlidersChange(self.SagittalVerticalSlider,self.sagittal_axis,True)
        #     self.OnSlidersChange(self.CoronalHorizontalSlider,self.coronal_axis,False)
        #     self.OnSlidersChange(self.CoronalVerticalSlider,self.coronal_axis,True)


    def onclick(self,event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
            ('double' if event.dblclick else 'single', event.button,
            event.x, event.y, event.xdata, event.ydata))
        
        self.obliqueLine.set_visible(False)
        self.obliqueLine_slope = (event.ydata/event.xdata)
        print(event.xdata/event.ydata)
        print(abs(self.obliqueLine_slope))
        self.obliqueLine = self.axial_axis.axline([0,0],slope=abs(self.obliqueLine_slope))
        self.obliqueLine.set_visible(True)
        self.axial_figure.canvas.draw_idle()
        self.axial_figure.canvas.flush_events()
        






if __name__ == '__main__':
    # os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Dicom_Viewer_App()
    window.show()
    sys.exit(app.exec_())