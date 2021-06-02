import sys
from cx_Freeze import setup, Executable
import os


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))

# os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
# os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

includefiles = ["images/"]
build_exe_options = {"packages": ["os"], "excludes": [""], "include_files": includefiles}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

    setup(
        name = "SnapShare",
        version = "1.0.0",  
        description = "SnapShare - Auto Screenshot Tool",
        options = {
        "build_exe": build_exe_options,
        },
        executables = [
        Executable("SnapShare.py",
            base=base,
        	icon=r"images/snapshare.ico",  # Must be .ico only,
            )
        ]
        )
# Turn Debug = False