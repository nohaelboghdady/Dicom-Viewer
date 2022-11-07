import sys
import pydicom as dicom # For reading dicom image
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
import matplotlib 
matplotlib.use('Qt5Agg')
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import os 
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QPointF



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

    def Graphic_Scene(self,fig_width,fig_height,view,bool=True):
        '''Setting up a canvas to view an image in its graphics view'''
        scene= QGraphicsScene()
        figure = Figure(figsize=(fig_width/90, fig_height/90),dpi = 90)
        canvas = FigureCanvas(figure )
       
        axes = figure .add_subplot()
        scene.addWidget(canvas)
        self.moveObject = MovingObject(50, 50, 5)
        scene.addItem(self.moveObject)
        #scene.addWidget(Cursor(self.axes, horizOn= True, vertOn= True, color="green"))
        view.setScene(scene)
        if bool ==True:
            figure .subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
            axes.get_xaxis().set_visible(False)
            axes.get_yaxis().set_visible(False)
        else:
            axes.get_xaxis().set_visible(True)
            axes.get_yaxis().set_visible(True)
        return figure, axes
      
        


    def onclick(self, event):
        print("in on click")
        if (self.axis_Axial_Plane):
            if event.inaxes == self.axis_Axial_Plane:
                x = event.xdata
                y = event.ydata
                print(x , y)
                
                xlim0, xlim1 = self.axis_Axial_Plane.get_xlim()
                if x <= xlim0+(xlim1-xlim0)*self.clicklim:
                    self.horizontal_line_Axial.set_ydata(y)
                    self.text.set_text(str(y))
                    self.text.set_position((xlim0, y))
                    self.figure_Axial_Plane.canvas.draw()
        if (self.axis_Sagittal_Plane):
            if event.inaxes == self.axis_Sagittal_Plane:
                x = event.xdata
                y = event.ydata
                print(x , y)
                
                xlim0, xlim1 = self.axis_Sagittal_Plane.get_xlim()
                if x <= xlim0+(xlim1-xlim0)*self.clicklim:
                    self.horizontal_line_Sagittal.set_ydata(y)
                    self.text.set_text(str(y))
                    self.text.set_position((xlim0, y))
                    self.figure_Sagittal_Plane.canvas.draw()           

        if (self.axis_Coronal_Plane):
            if event.inaxes == self.axis_Coronal_Plane:
                x = event.xdata
                y = event.ydata
                print(x , y)
                
                xlim0, xlim1 = self.axis_Coronal_Plane.get_xlim()
                if x <= xlim0+(xlim1-xlim0)*self.clicklim:
                    self.horizontal_line_Coronal.set_ydata(y)
                    self.text.set_text(str(y))
                    self.text.set_position((xlim0, y))
                    self.figure_Coronal_Plane.canvas.draw()              
                    

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


        self.viewing_planes(self.Axial_Plane)
        self.viewing_planes(self.Sagittal_Plane)
        self.viewing_planes(self.Coronal_Plane)


    def viewing_planes(self, plane):    
       self.figure_Plane, self.axis_Plane = self.Graphic_Scene(201, 170, plane)
       if (plane == self.Axial_Plane):
            self.axis_Plane.imshow(self.volume3d[:,:,0], cmap="gray") # first slice in z
       if (plane == self.Coronal_Plane):
            self.axis_Plane.imshow(np.rot90(self.volume3d[256,:,:]), cmap="gray")
       if (plane == self.Sagittal_Plane):   
            self.axis_Plane.imshow(np.rot90(self.volume3d[:,256,:]), cmap="gray") 

        

        

class MovingObject(QLine):
    def __init__(self, x, y, r):
        super().__init__(0, 0, r, r)
        self.setPos(x, y)
        self.setBrush(Qt.blue)
        self.setAcceptHoverEvents(True)

    # mouse hover event
    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    # mouse click event
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))




if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1" 
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Dicom_Viewer_App()
    window.show()
    app.exec_()        