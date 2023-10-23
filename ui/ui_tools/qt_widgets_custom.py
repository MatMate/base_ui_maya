"""idgets_custom.
Qt Library widget



"""
import maya.cmds as mc
import functools
from PySide2.QtCore import QRegExp, Qt
from PySide2.QtGui import QRegExpValidator, QFont, QIcon, QPixmap, QImage, QMouseEvent
#from PySide2.QtUiTools import *
from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton, QFrame, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy


######################
##  Joints
######################
class AdvanceSelectionJoints(QWidget):

    def __init__(self, 
                 text = "", 
                 parent_ui = None, 
                 icon_path = "kinConnect.png", 
                 color = None, 
                 messagge = "Required", 
                 logger = None,
                 **kwargs):
        """     
        Structure label, line edit, push btn 
        
        button ICON: nurbsCurve.svg, kinConnect.png
        
        """
        super(AdvanceSelectionJoints, self).__init__(**kwargs)
    
        self.text = text
        self.parent_ui = parent_ui
        self.status = False
        self.icon_path = icon_path
        self.color = color
        self.messagge = messagge
        self.logger = logger
        # info
        self.setToolTip(self.messagge)

        self.h_lyt = QHBoxLayout()
        self.h_lyt.setContentsMargins(0,0,0,0)
        self.setLayout(self.h_lyt)

        self.build_lyt()
        self.make_connection()
    
    def build_lyt(self):

        self.lab = QLabel()
        self.lab.setMinimumWidth(75)
        set_style_label(label = self.lab, text = self.text,
                         color = self.color, fontFam = "Verdana", fontSi = 7, fontBold = False)

        self.h_lyt.addWidget(self.lab)
        self.h_lyt.addStretch()

        self.li_ed = QLineEdit()
        self.li_ed.setPlaceholderText(self.messagge)
        self.h_lyt.addWidget(self.li_ed, Qt.AlignVCenter)

        #radio
        self.btn = QPushButton()
        self.btn.setFixedSize(18,18)
        self.btn.setIcon(QIcon(f":{self.icon_path}"))
        self.h_lyt.addWidget(self.btn)

    def make_connection(self):
        self.li_ed.textChanged.connect(functools.partial(self.check_li_ed_com, self.li_ed))
        self.btn.pressed.connect(functools.partial(self.ele_from_selection_btn_com, self.li_ed))

    
    def check_type(self, obj = "", obj_type = "joint"):
        """     check if """
        if mc.objExists(obj):
            return mc.objectType(obj) == obj_type
        else:
            return False



    ###########
    # JOINTS

    def ele_from_selection_btn_com(self, li_ed = QLineEdit):
        """ 
            set JNT from selection to given li_ed 
            press btn to set li_ed
        """
        selection = mc.ls(sl = True)
        if selection and mc.objectType(selection[0]) == "joint":
            li_ed.setText(str(selection[0]))
            self.logger.debug(f"JNT Name: {str(selection[0])}")
        else:
            self.logger.error(f"No joint Selected, from {selection}!")
            #self.parent_ui.messagge_error("No joint Selected, from {selection}!")

    def check_li_ed_com(self, li_ed = QLineEdit, text = ""):
        """ 
            set JNT from selection to given li_ed 
            set color and text li_ed
        """
        if self.check_type(obj = text, obj_type = "joint"):
            set_color_style(li_ed, color="green")
            self.status = True
        else:
            set_color_style(li_ed, color="red")
            self.status = False
            
    ##################
    # SET
    # 
    def set_enable(self, status = True):
        self.setEnabled(status)   
    
    def set_info(self, label = "", place_holder = ""):
        set_style_label(label = self.lab, text = label,
                         color = self.color, fontFam = "Verdana", fontSi = 7, fontBold = False)
        if place_holder != "":
            self.li_ed.setPlaceholderText(place_holder)
    ##################
    # GET
    
    def get_text(self):
        """     check if """
        return self.li_ed.text()
    
    def get_status(self):
        """     check if """
        return self.status
    
    def get_li_ed(self):
        """
        
        """
        return self.li_ed

    ##################
    # ERROR
    def error_selection(self):
        self.logger.error("No valid Joint selected!!")
        self.parent_ui.set_messagge_ui()


######################
##  Ankle
######################
class AdvanceSelectionAnkle(AdvanceSelectionJoints):

    def __init__(self, 
                 child = QLineEdit, 
                 gchild = QLineEdit, 
                 handle = QLineEdit, 
                 ctrl = QLineEdit, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.child = child
        self.gchild = gchild
        #handle
        self.handle = handle
        #ctrl
        self.ctrl = ctrl

    
    def check_li_ed_com(self, li_ed = QLineEdit, text = ""):
        """ 
            set JNT from selection to given li_ed 
            set color and text li_ed
        """
        if self.check_type(obj = text, obj_type = "joint"):
            set_color_style(li_ed, color="green")
            self.status = True
            self.set_children(text)
            self.set_handle(text)
        else:
            set_color_style(li_ed, color="red")
            self.status = False
    
    def set_children(self, text = ""):
        """
        set children
        
        """
        temp_child = mc.listRelatives(text, children = True)

        if temp_child:
            self.child.setText(temp_child[0])
            temp_gchild = mc.listRelatives(temp_child[0], children = True)
            self.logger.debug(f"child: {temp_gchild}")
            self.set_foot_ctrl(temp_child[0])
            if temp_gchild:
                self.gchild.setText(temp_gchild[0])
    
    def set_foot_ctrl(self, text = ""):
        """
        
        """
        try:
            ls_words = text.split("_")
            temp_prefix = ls_words[0]
            temp_suffix = ls_words[-1]

            pos_foot_ctrl = text.replace(("_" + temp_suffix),
                                        ("_CTRL"),
                                        1)
            if mc.objExists(pos_foot_ctrl):
                self.ctrl.setText(pos_foot_ctrl)
        except Exception as e :
            self.logger.error(f"No valid ctrl found! ERROR: {e}")
            self.ctrl.setText("")


    def set_handle(self, text = ""):
        """
        
        """
        try:
            ankle_ctrl = mc.listConnections("{}.offsetParentMatrix".format(text))[0]
            wd = mc.listConnections("{}.handlePath[0]".format(ankle_ctrl))[0]
            self.handle.setText(wd)
        except Exception as e :
            self.logger.error(f"No valid handle found! ERROR: {e}")
            self.handle.setText("")

######################
##  Controller
######################
class AdvanceSelectionController(AdvanceSelectionJoints):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def ele_from_selection_btn_com(self, li_ed=QLineEdit):
        """ 
            set CTRL from selection to given li_ed 
            press btn to set li_ed
        """
        selection = mc.ls(sl = True)
        if selection and mc.objExists(selection[0]+'Shape') and mc.objectType(selection[0]+'Shape') == "nurbsCurve":
            li_ed.setText(str(selection[0]))
            self.logger.debug(f"CTRL Name: {str(selection[0])}")
        else:
            self.logger.error(f"No Controller Selected, from {selection}!")
            #self.parent_ui.messagge_error("No Controller Selected, from {selection}!")
    
    def check_li_ed_com(self, li_ed=QLineEdit, text=""):
        """ 
            set CTRL from selection to given li_ed 
            set color and text li_ed
        """
        if text != "":
            if mc.objExists(text+'Shape') and mc.objectType(text+'Shape') == "nurbsCurve":
                set_color_style(widget = li_ed, color = "green")
                self.status = True
            else:
                set_color_style(widget = li_ed, color = "red")
                self.logger.error("No CTRL selected or Rename CTRL from standard name ex: nurbsCircle1")
                self.status = False
        else:
            set_color_style(widget = li_ed, color = None)


######################
##  Handle
######################
class AdvanceSelectionHandle(AdvanceSelectionJoints):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

    def ele_from_selection_btn_com(self, li_ed=QLineEdit):
        """ 
            set Handle from selection to given li_ed 
            press btn to set li_ed
        """
        selection = mc.ls(sl = True)
        if selection and mc.objExists(selection[0]) and mc.objectType(selection[0]) == "ikHandle":
            li_ed.setText(str(selection[0]))
            self.logger.debug(f"Handle Name: {str(selection[0])}")
        else:
            self.logger.error(f"No Controller Selected, from {selection}!")
            #self.parent_ui.messagge_error("No Controller Selected, from {selection}!")
    
    def check_li_ed_com(self, li_ed=QLineEdit, text=""):
        """ 
            set Handle from selection to given li_ed 
            set color and text li_ed
        """
        if text != "":
            if mc.objExists(text) and mc.objectType(text) == "ikHandle":
                set_color_style(widget = li_ed, color = "green")
                self.status = True
            else:
                set_color_style(widget = li_ed, color = "red")
                self.logger.error("No Valid Handle selected!")
                self.status = False
        else:
            set_color_style(widget = li_ed, color = None)
######
# Class Line
########
class QLineCustom(QFrame):
    def __init__(self, color = None, parent = None):
        super(QLineCustom, self).__init__(parent)

        self.color = color

        self.create_line()

    def create_line(self):
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        set_color_style(self, color_background = self.color)

class QScrollableWidget(QWidget):
    def __init__(self, title = "", title_color = "", height = 0, parent = None):
        super(QScrollableWidget, self).__init__(parent)

        self.title = title
        self.title_color = title_color
        self.fixed_height = height
        self.frame_visibility = False

        self.container_main_lyt = QVBoxLayout()
        self.container_main_lyt.setContentsMargins(2,1,2,1)
        self.container_main_lyt.setSpacing(0)

        #switch btn
        self.container_main_lyt.addLayout(self.switch_lyt())
        self.container_main_lyt.addWidget(self.frame_widget())

        self.setLayout(self.container_main_lyt)

        self.make_connection()
        self.set_fixed_size_text(50, 20)


    def line_frame(self, color = None):        
        sep = QLineCustom(color = color)
        return sep


    def switch_lyt(self):
        switch_hor_lyt = QHBoxLayout()
        switch_hor_lyt.setContentsMargins(0,0,0,0)
        switch_hor_lyt.setSpacing(0)

        self.switch_btn = QPushButton()
        set_color_style(self.switch_btn, color_background="transparent", border_enabled= True, border=0)#[70,70,70])
        self.switch_btn.setFixedSize(10,10)
        self.switch_btn.setIcon(QIcon(":arrowRight"))
        switch_hor_lyt.addWidget(self.switch_btn, Qt.AlignVCenter)
        switch_hor_lyt.addSpacing(10)

        self.switch_lab = QLabel()
        set_style_label(label = self.switch_lab, text = self.title,
                         color =  self.title_color, fontFam = "Verdana", fontSi = 7, fontBold = False)
        switch_hor_lyt.addWidget(self.switch_lab, Qt.AlignVCenter)

        return switch_hor_lyt

    def frame_widget(self):
        self.frame_custom = QFrame()
        self.frame_custom.setFrameShape(QFrame.StyledPanel)
        self.frame_custom.setFrameShadow(QFrame.Plain)
        self.frame_custom.lineWidth()
        self.frame_custom.setLineWidth(3)
        self.frame_custom.midLineWidth()
        self.frame_custom.setMidLineWidth(3)

        #self.frame_custom.setFixedHeight(self.fixed_height)
        self.frame_custom.setVisible(self.frame_visibility)

        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.frame_custom.setSizePolicy(size_policy)

        self.frame_v_lyt = QVBoxLayout(self.frame_custom)
        self.frame_v_lyt.setContentsMargins(2,2,2,2)
        self.frame_v_lyt.setSpacing(2)

        self.build_frame_lyt(self.frame_v_lyt)
        return self.frame_custom

    ######
    # Connections
    ####
    def make_connection(self):
        self.switch_lab.mousePressEvent = self.test_tt
        self.switch_btn.pressed.connect(self.switch_btn_com)


    def test_tt(self, event):
        if event:
            self.switch_btn_com()

    #####################
    # External Methods
    ###
    def build_frame_lyt(self, lyt = QVBoxLayout):
        """ create lyt Frame """
        pass

    def set_fixed_size_text(self, w, h):
        """     set width and height of text switch """
        self.switch_lab.setFixedHeight(h)
        self.switch_btn.setFixedSize(10, h)

    def get_frame_lyt(self):
        return self.frame_v_lyt




    #####################
    # BTN COM
    ###
    
    def switch_btn_com(self):
        self.frame_visibility = not self.frame_visibility
        if self.frame_visibility:
            self.switch_btn.setIcon(QIcon(":arrowDown.png"))
        else:
            self.switch_btn.setIcon(QIcon(":arrowRight.png"))
        
        self.frame_custom.setVisible(self.frame_visibility)






#####
#   Image editor
#####
def image_settings(widget = QLabel, path = "", dimension = []):
    """ set image to a label, with proper settings"""

    #widget.setPixmap(path) simple way no mod to image
    image = QImage(path)
    #set scaleble image
    if dimension:
        image = image.scaled(dimension[0], dimension[1], Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

    #pixmap
    pixmap = QPixmap()
    pixmap.convertFromImage(image)

    widget.setPixmap(pixmap)




def set_icon_widget(widget = QPushButton, path = "", info = ""):
    """ set icon, pass path and info for tool tip """
    
    widget.setIcon(QIcon(path)) # Absolute path for qt icon: ":fileOpen.png"
    if info != "":
        widget.setToolTip(info)


#########
#
###########

def mirror_image(self, ):
    """
    mirror image for 
    """

    img = QImage(f":{self.icon}")
    img = img.mirrored(True, False)
    pix = QPixmap()
    pix.convertFromImage(img)
    #self.forward_btn.setIcon(QIcon(pix))

def set_image_tool_tip(widget = None, user_text = "", image_path = ""):
    """
    mirror image for 
    """
    print("UPDATE 4")
    #image hover
    image_path = os.path.join(os.path.dirname(__file__), "jai.png")
    user_text = "TEST!"
    widget.setToolTip('<b>{0}</b><br><img src="{1}">'.format(user_text, image_path))
        

#####
#   LineEdit Builder
#####

def validator_lineEdit(lineEdit = QLineEdit, QRegExpText = ""):
    """ 
    ex: "[0-9]+.?[0-9]{,2}" 
    first part till symbols or letters: numbers
    second part, only one digit: symbols or letters
    third part: numbers
    
    ex: [\dA-Za-z][_\dA-Za-z]{1,}
    first digit: letters and numbers
    secondo digit: letters, numbers, and '_'
    
    """
    reg_ex = QRegExp(QRegExpText)
    input_validator = QRegExpValidator(reg_ex, lineEdit)
    lineEdit.setValidator(input_validator)




#####
# Style Sheet
#####


def set_style_label(label = QLabel, text = "", fontFam = "", fontSi = 0, fontBold = False, color = None, colorBackground = None):
        """ Widget setup """
        label.setText(text)
        set_color_style(widget = label, color = color, color_background = colorBackground)
        font = QFont()
        font.setFamily(f"{fontFam}")
        font.setPointSize(fontSi)
        font.setBold(fontBold)
        label.setFont(font)
        #label.setAlignment(Qt.AlignHCenter)

def set_color_style(widget = None, color = None, color_background = None, font_style = [],
                    border_enabled = False,border = 0,  border_color = "",
                    border_circular_enabled = False, border_radius = 0):

    """ set styleSheet Widget font ex [True, 9, "Verdana"] bold, size, type"""
    colorWidget = check_color_type(type_Color = "color", color = color)
    colorBackWidget = check_color_type(type_Color = "background-color", color = color_background)
    font_style = check_font_style(font_style = font_style)
    #border
    if border_enabled:
        border_style = f"border: {border}px solid {border_color};"
        if border_circular_enabled:
            border_style += f"border-radius: {border_radius}px;"
    else:
        border_style = ""
    #Possible future implementation....
    styleSheet = f"{colorWidget}{colorBackWidget}{font_style}{border_style}"

    #print(f"COLOR view Style: {syleSheet} for {widget}")

    widget.setStyleSheet(f"{styleSheet}")


def check_color_type(type_Color = "", color = None):
    """ Return Color for Style """
    #"color: black; background-color: rgb(170, 0, 0);"
    if color:
        if type(color) is str:
            return f"{type_Color}: {color};"
        else:
            return f"{type_Color}: rgb({color[0]}, {color[1]}, {color[2]});"
    else:
        return ""

def check_font_style(font_style = []):
    """ ex [True, 9, "Verdana"]    """
    #print(f"FONT STYLE: {fontStyle}")
    if font_style:
        if font_style[0]:
            return f"font: 75 {font_style[1]}pt \"{font_style[2]}\";"
        else:
            return f"font: {font_style[1]}pt \"{font_style[2]}\";"
    else:
        return ""