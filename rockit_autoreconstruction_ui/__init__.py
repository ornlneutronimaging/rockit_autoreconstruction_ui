import os
from qtpy.uic import loadUi
from rockit_autoreconstruction_ui import ui
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions

def load_ui(ui_filename, baseinstance):
    ui_filename = os.path.split(ui_filename)[-1]
    ui_path = os.path.dirname(ui.__file__)

    # get the location of the ui directory
    # this function assumes that all ui files are there
    filename = os.path.join(ui_path, ui_filename)

    return loadUi(filename, baseinstance=baseinstance)
