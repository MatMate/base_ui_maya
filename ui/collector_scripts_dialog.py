import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2.QtWidgets import QWidget, QVBoxLayout, QDialog

##############
# import UI
try :
    import ui.collector_scripts_widget as collector_scripts_widget
    import ui.maya_script_jobs as maya_script_jobs
except:
    import base_ui_maya.ui.collector_scripts_widget as collector_scripts_widget
    import base_ui_maya.ui.maya_script_jobs as maya_script_jobs

###
#   UI
######
class CollectorScripsUI(QDialog): #Python2 QtGui.QDialog
    #save instance current class
    dlg_instance = None

    @classmethod
    def display(cls):
        """
            create instance if donsn't exist
        """
        if not cls.dlg_instance:
            cls.dlg_instance = CollectorScripsUI()

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            #come into view
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    @classmethod
    def get_maya_window(cls):
        """
            Return the Maya main widget as a python object
        """
        maya_window_ptr = omui.MQtUtil.mainWindow()
        if maya_window_ptr:
            return wrapInstance(int(maya_window_ptr), QWidget) #Python2 long(ptr)


    def __init__(self):
        super(CollectorScripsUI, self).__init__(self.get_maya_window())

        self.setMinimumWidth(285)
        self.main_vert_lyt = QVBoxLayout()
        self.main_vert_lyt.setContentsMargins(3,3,3,3)
        #Call external UI
        self.widget = collector_scripts_widget.CollectorScripsWidget()
        self.main_vert_lyt.addWidget(self.widget)
        
        self.setWindowTitle("Rig Utils")
        self.setLayout(self.main_vert_lyt)
    
    ######
    #  Extend Window methods with custom properties
    #  Save position Windows and set this at the next start
    ############
    def create_script_jobs(self):
        self.widget.create_script_jobs()

        
    def delete_script_jobs(self):
        script_jobs = self.widget.get_script_jobs()
        maya_script_jobs.delete_script_jobs(script_jobs)
        print(f"Script jobs killed --> {script_jobs}")
        
        self.widget.set_script_jobs([])

        


    def showEvent(self, e):
        super(CollectorScripsUI, self).showEvent(e)
        
        if self.geometry:
            self.restoreGeometry(self.geometry)


    def closeEvent(self, e):
        if isinstance(self, CollectorScripsUI):
            super(CollectorScripsUI, self).closeEvent(e)
            #self.delete_script_jobs()
            self.geometry = self.saveGeometry()

