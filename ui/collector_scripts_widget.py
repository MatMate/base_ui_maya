#### PySide2
from PySide2.QtCore import Qt 
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTabWidget)

import logging
LEVEL = logging.DEBUG
_logger = logging.getLogger(__name__)
_logger.setLevel(LEVEL)

### Widgets


try:
    import ui.ui_tools.qt_widgets_custom as qt_widgets_custom
except:
    import base_ui_maya.ui.ui_tools.qt_widgets_custom as qt_widgets_custom



###
#   UI
######
class CustomQLabel(QLabel):

    TEXT = "still work in progress"

    def __init__(self):
        super(CustomQLabel, self).__init__()
        
        qt_widgets_custom.set_style_label(label = self, text = "Matteo RIG Utils v 1.0.0",
                         color =  [109,0,0], fontFam = "Verdana", fontSi = 9, fontBold = True)
        self.setAlignment(Qt.AlignCenter)
        self.setToolTip(self.TEXT)


class CollectorScripsWidget(QWidget): #Python2 QtGui.QDialog

    def __init__(self):
        super(CollectorScripsWidget, self).__init__()

    
        #self.setMinimumWidth(280)

        self.main_vert_lyt = QVBoxLayout()
        self.main_vert_lyt.setContentsMargins(0,0,0,0)
        self.main_vert_lyt.setSpacing(2)

        #####
        #   addToLayout
        #####

        ########
        #   Toll Box
        self.tab = QTabWidget()
        #self.tab.setFixedHeight(200)



        self.main_vert_lyt.addWidget(self.tab)
        #
        ############

        #name author
        self.main_vert_lyt.addWidget(self.line_frame())
        self.main_vert_lyt.addSpacing(10)
        self.main_vert_lyt.addWidget(CustomQLabel())
        #############

        self.make_connection()


        self.setWindowTitle("RIG Helper by MatMate")
        self.setLayout(self.main_vert_lyt)

        
    
    ################
    #   Init Widgets
    ################
    
    
    def line_frame(self):        
        sep = qt_widgets_custom.QLineCustom(color = None)
        return sep

    def make_connection(self):
        pass
    
    #######
    #Methods UI
    ########
    def create_script_jobs(self):
        #self.rot_wid.create_script_jobs()
        pass


    def get_script_jobs(self):
        #return self.rot_wid.get_script_jobs()
        pass
    
    def set_script_jobs(self, ls = []):
        #self.rot_wid.set_script_jobs(ls)
        pass