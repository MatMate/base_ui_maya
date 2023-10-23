

def run_ui():
    
    #import rig_utilities.ui.rotation_checker_scrips_ui as rotation_checker_scrips_ui

    ##Only for debug 
    #from importlib import reload
    #reload(rotation_checker_scrips_ui)
    
    #IF this is eneabled then will create multiple windows
    #so activate only in debug state

    from .ui.rotation_checker_scrips_ui import RotationCheckerScripsUI

    RotationCheckerScripsUI.display()