"""
for reload purpose

"""
from importlib import reload

try:
    import ui.ui_tools.qt_widgets_custom as qt_widgets_custom
except:
    import base_ui_maya.ui.ui_tools.qt_widgets_custom as qt_widgets_custom

try :
    import ui.collector_scripts_widget as collector_scripts_widget
    import ui.maya_script_jobs as maya_script_jobs
except:
    import base_ui_maya.ui.collector_scripts_widget as collector_scripts_widget
    import base_ui_maya.ui.maya_script_jobs as maya_script_jobs


def reload_mod():
    print("\n"+"             RUN Debug"+"\n")

    reload(qt_widgets_custom)
    reload(collector_scripts_widget)
    reload(maya_script_jobs)