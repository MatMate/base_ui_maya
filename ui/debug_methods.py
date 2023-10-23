"""
for reload purpose

"""
from importlib import reload

try:
    import ui.ui_tools.qt_widgets_custom as qt_widgets_custom
except:
    import base_ui_maya.ui.ui_tools.qt_widgets_custom as qt_widgets_custom


def reload_mod():
    print("\n"+"             RUN Debug"+"\n")

    reload(qt_widgets_custom)