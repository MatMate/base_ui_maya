#### PySide2
from PySide2.QtCore import Qt 
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QPushButton, QLineEdit)

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
        self.main_vert_lyt.addLayout(self.test_lyt())

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

    def test_lyt(self):
        """
            preview widgets
        """
        test_h_lyt = QHBoxLayout()

        self.test_li_ed = QLineEdit()
        self.test_li_ed.setPlaceholderText("Type something...")
        test_h_lyt.addWidget(self.test_li_ed)
        test_h_lyt.addSpacing(10)

        test_h_lyt.addStretch()
        self.test_btn = QPushButton("Press to print!")
        self.setToolTip("Press to print text from the left!")
        test_h_lyt.addWidget(self.test_btn)


        return test_h_lyt
    
    
    def line_frame(self):        
        sep = qt_widgets_custom.QLineCustom(color = None)
        return sep

    def make_connection(self):
        

        self.test_li_ed.textChanged.connect(self.test_li_ed_com)
        self.test_btn.pressed.connect(self.test_btn_com)
    
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

    ################
    #
    ###########

    def test_li_ed_com(self, text = ""):
        """
        """
        print(f"Text changed to: {text}")

    def test_btn_com(self):
        """
        
        """

        print(f"TEXT TO PRINT: \n{self.test_li_ed.text()}")