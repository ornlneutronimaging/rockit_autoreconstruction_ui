from qtpy.QtWidgets import QApplication, QMainWindow
import sys
import os
import logging
import warnings

warnings.filterwarnings("ignore")

from . import load_ui
from . import __version__


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        """
        Initialization
        Parameters
        ----------
        """
        super(MainWindow, self).__init__(parent)
        self.ui = load_ui('mainWindow.ui', baseinstance=self)
        self.setWindowTitle(f"rockit auto-reconstruction ui - v{__version__}")

    def closeEvent(self, event):
        logging.info(" #### Leaving maverick ####")
        self.close()


def main(args):
    app = QApplication(args)
    app.setStyle("Fusion")
    app.aboutToQuit.connect(clean_up)
    app.setApplicationDisplayName("rockit auto-reconstruction ui")
    application = MainWindow()
    application.show()
    sys.exit(app.exec_())


def clean_up():
    app = QApplication.instance()
    app.closeAllWindows()
