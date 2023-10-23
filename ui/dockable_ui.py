from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget
from shiboken2 import getCppPointer

from maya import OpenMayaUI  as omui
from maya import cmds as mc



####
# General Class
#####

class CustomWorkspaceControl(object):

    
    def __init__(self, parent='None', name = ""):

        self.name = name
        self.widget = None

    def create(self, label, widget, ui_script=None):
        mc.workspaceControl(self.name, label = label)

        if ui_script:
            mc.workspaceControl(self.name, e=True, uiScript = ui_script)
        
        self.add_widget_to_layout(widget)
        self.set_visible(True)
    
    def restore(self, widget):
        self.add_widget_to_layout(widget)
    
    def add_widget_to_layout(self, widget):
        if widget:
            self.widget = widget
            self.widget.setAttribute(Qt.WA_DontCreateNativeAncestors)
            
            # if exist add the content there
            #same posiotion
            workspace_control_ptr = int(omui.MQtUtil.findControl(self.name))
            widget_ptr = int(getCppPointer(self.widget)[0])

            omui.MQtUtil.addWidgetToMayaLayout(widget_ptr, workspace_control_ptr)

    def exists(self):
        return mc.workspaceControl(self.name, q = True, exists = True)

    def is_visible(self):
        return mc.workspaceControl(self.name, q = True, visible = True)

    def set_visible(self, visible):
        if visible:
            mc.workspaceControl(self.name, e = True, restore = True)
        else:
            mc.workspaceControl(self.name, e = True, visible = False)
    
    def set_label(self, label):
        mc.workspaceControl(self.name, e = True, label = label)
    
    def is_floating(self):
        return mc.workspaceControl(self.name, q = True, floating = True)

    def is_collapsed(self):
        return mc.workspaceControl(self.name, q = True, collapse = True)
    
class CustomDockableUI(QWidget):

    WINDOW_TITLE = "MatMateDockUI"

    ui_istance = None

    @classmethod
    def display(cls):
        if cls.ui_istance:
            cls.ui_istance.show_workspace_control()
        else:
            cls.ui_istance = cls()

    @classmethod
    def get_workspace_control_name(cls):
        print(f" INSIDE METHODS {cls.__name__}WorkspaceControl")
        return f"{cls.__name__}WorkspaceControl"
    
    @classmethod
    def get_ui_script(cls):
        module_name = cls.__module__

        if module_name == "__main__":
            module_name = cls.module_name_override

        ui_script = f"from {module_name} import {cls.__name__}\n{cls.__name__}.display()"
        print(f"\nSCRIPT PATH\n{ui_script}\n")
        return ui_script

    def __init__(self):
        super(CustomDockableUI, self).__init__()

        self.setObjectName(self.__class__.__name__)
        self.setMinimumSize(200, 100)

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.create_workspace_control()

    def create_widgets(self):
        pass

    def create_layout(self):
        pass

    def create_connections(self):
        pass


    #####
    # Dock
    ########    
    def show_workspace_control(self):
        self.workspace_control_instance.set_visible(True)

    def create_workspace_control(self):
        print(self.get_workspace_control_name())
        self.workspace_control_instance = CustomWorkspaceControl(name = self.get_workspace_control_name())

        #if already exists restore else create a new
        if self.workspace_control_instance.exists():
            self.workspace_control_instance.restore(self)
        else:
            print(f"\n---------------- RECREATED ______________ \n")
            
            self.workspace_control_instance.create(self.WINDOW_TITLE, self, ui_script = self.get_ui_script())
