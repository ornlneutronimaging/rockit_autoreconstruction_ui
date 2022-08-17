from qtpy.QtWidgets import QApplication, QMainWindow
import sys
import os
import logging
import warnings

warnings.filterwarnings("ignore")

from . import load_ui
from . import __version__
from .utilities.status_message_config import StatusMessageStatus, show_status_message

DEBUG = True
AUTOREDUCE_CONFIG_FILE_NAME = "autoreduce_cg1d_config.yaml"


class MainWindow(QMainWindow):

    autoreduce_config_file = None

    def __init__(self, parent=None):
        """
        Initialization
        Parameters
        ----------
        """
        super(MainWindow, self).__init__(parent)
        self.ui = load_ui('mainWindow.ui', baseinstance=self)
        self.setWindowTitle(f"rockit auto-reconstruction ui - v{__version__}")
        self.initialize()

    def initialize(self):
        self.initialize_statusbar()
        self.initialize_config_file_name()

    def initialize_statusbar(self):
        self.setStyleSheet("QStatusBar{padding-left:8px;color:red;font-weight:bold;}")

    def initialize_config_file_name(self):
        if DEBUG:
            autoreduce_config_path = "/Users/j35/HFIR/CG1D/shared/autoreduce/"
        else:
            autoreduce_config_path = "/HFIR/CG1D/shared/autoreduce/"
        self.autoreduce_config_file = os.path.join(autoreduce_config_path, AUTOREDUCE_CONFIG_FILE_NAME)
        show_status_message(parent=self,
                            message=f"config: {self.autoreduce_config_file}",
                            status=StatusMessageStatus.working)

    # event handler
    def ipts_value_changed(self, value):
        print(f"ipts_value changed: {value}")

    def preview_clicked(self):
        print("preview clicked")

    def reset_history_clicked(self):
        print("reset history clicked")

    def activate_auto_reconstruction_clicked(self):
        activate_status = self.ui.activate_auto_reconstruction_checkBox.isChecked()
        self.ui.auto_reconstruction_frame.setEnabled(activate_status)

    def ok_clicked(self):
        print("ok clicked")

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
