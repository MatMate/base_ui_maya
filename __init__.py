"""
Matteo Girolami

Methods for maya


# for Users of maya 2023  ----


#####################################
from importlib import reload

import base_ui_maya.ui.debug_methods as debug_methods
reload(debug_methods)
debug_methods.reload_mod()

#Command Call
import base_ui_maya.ui.collector_scripts_dialog as collector_scripts_dialog

##Only for debug 
from importlib import reload
reload(collector_scripts_dialog)

#IF this is eneabled then will create multiple windows
#so activate only in debug state

from base_ui_maya.ui.collector_scripts_dialog import CollectorScripsUI

CollectorScripsUI.display()

######################################







"""