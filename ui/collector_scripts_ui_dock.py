
import maya.cmds as mc
from PySide2.QtWidgets import QVBoxLayout

############
#   UI
try :
    import ui.dockable_ui as dockable_ui
    import ui.collector_scripts_widget as collector_scripts_widget
    import ui.maya_script_jobs as maya_script_jobs
except:
    
    import base_ui_maya.ui.dockable_ui as dockable_ui
    import base_ui_maya.ui.collector_scripts_widget as collector_scripts_widget
    import base_ui_maya.ui.maya_script_jobs as maya_script_jobs


############
#   UI
class CollectorScripsUI(dockable_ui.CustomDockableUI): #Python2 QtGui.QDialog

    
    WINDOW_TITLE = "Rig Utils"

    def __init__(self):
        super(CollectorScripsUI, self).__init__()
        self.setMinimumWidth(285)

        self.main_vert_lyt = QVBoxLayout()
        self.main_vert_lyt.setContentsMargins(1,1,1,1)
        #Call external UI
        self.dock_ui = collector_scripts_widget.CollectorScripsWidget()
        self.main_vert_lyt.addWidget(self.dock_ui)

        self.setLayout(self.main_vert_lyt)
    
    
    def delete_script_jobs(self):
        script_jobs = self.dock_ui.get_script_jobs()
        maya_script_jobs.delete_script_jobs(script_jobs)
        print(f"Script jobs killed --> {script_jobs}")
        
        self.dock_ui.set_script_jobs([])


    def showEvent(self, e):
        super(CollectorScripsUI, self).showEvent(e)
        if self.workspace_control_instance.is_floating():
            self.workspace_control_instance.set_label("Rig Utils")
        else:
            self.workspace_control_instance.set_label("Rig Utils")
    
    def closeEvent(self, e):
        self.delete_script_jobs()
        super(CollectorScripsUI, self).closeEvent(e)


if __name__ == "__main__":
    
    workspace_control_name = CollectorScripsUI.get_workspace_control_name()

    #Test for dockable UI delete even if is dock
    try:
        test_dialog.setParent(None)
        test_dialog.deleteLater()
    except:
        pass

    if mc.window(workspace_control_name, exists = True):
        mc.deleteUI(workspace_control_name)
    
    CollectorScripsUI.module_name_override = "rig_utilities.ui.collector_scripts_ui_dock"

    test_dialog = CollectorScripsUI()