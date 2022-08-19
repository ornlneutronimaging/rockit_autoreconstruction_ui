from qtpy.QtWidgets import QApplication, QMainWindow
import sys
import os
import logging
import warnings
from enum import Enum
import yaml
import io

warnings.filterwarnings("ignore")

from . import load_ui
from . import __version__
from .utilities.status_message_config import StatusMessageStatus, show_status_message
from .history import History

DEBUG = True
AUTOREDUCE_CONFIG_FILE_NAME = "autoreduce_cg1d_config.yaml"


class Status(Enum):
    ok = 'ok'
    error = 'error'


class MainWindow(QMainWindow):

    autoreduce_config_file = None
    ipts_folder = "/HFIR/CG1D/"
    if DEBUG: ipts_folder = "/Users/j35/HFIR/CG1D/"

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

        status = self.initialize_config_file_name()
        if status == Status.error:
            return

        status = self.read_yaml()
        if status == Status.error:
            return

        self.initialize_widgets()

    def initialize_widgets(self):

        self.ui.activate_auto_reconstruction_checkBox.setChecked(self.autoreduction_mode)
        self.activate_auto_reconstruction_clicked()

        self.ui.ipts_spinBox.setValue(int(self.ipts))

        if self.xmin:
            self.ui.xmin_spinBox.setValue(self.xmin)
            self.ui.xmin_checkBox.setChecked(True)
        else:
            self.ui.xmin_checkBox.setChecked(False)
        self.crop_xmin_checkbox_update()

        if self.ymin:
            self.ui.ymin_spinBox.setValue(self.ymin)
            self.ui.ymin_checkBox.setChecked(True)
        else:
            self.ui.ymin_checkBox.setChecked(False)
        self.crop_ymin_checkbox_update()

        if self.xmax:
            self.ui.xmax_spinBox.setValue(self.xmax)
            self.ui.xmax_checkBox.setChecked(True)
        else:
            self.ui.xmax_checkBox.setChecked(False)
        self.crop_xmax_checkbox_update()

        if self.ymax:
            self.ui.ymax_spinBox.setValue(self.ymax)
            self.ui.ymax_checkBox.setChecked(True)
        else:
            self.ui.ymax_checkBox.setChecked(False)
        self.crop_ymax_checkbox_update()

        self.ui.ob_checkBox.setChecked(self.ob_auto_selection_mode)
        self.ui.maximum_number_of_ob_radioButton.setChecked(self.ob_use_max_number_of_files)
        self.ui.ob_days_spinBox.setValue(self.ob_days)
        self.ui.ob_hours_spinBox.setValue(self.ob_hours)
        self.ui.ob_minutes_spinBox.setValue(self.ob_minutes)

        self.automatic_open_beam_checkBox_changed(self.ui.ob_checkBox.isChecked())
        self.ob_radioButton_changed()

    def read_yaml(self):
        file_name = self.autoreduce_config_file
        with open(file_name, "r") as stream:
            yaml_data = yaml.safe_load(stream)

        try:
            self.ipts = yaml_data['DataPath']['ipts']
        except KeyError:
            self.ipts = 23788

        try:
            self.crop_roi_mode = yaml_data['ROI']['mode']
        except KeyError:
            self.crop_roi_mode = False

        checked_crop_roi_checkbox = self.crop_roi_mode
        try:
            self.xmin = yaml_data['ROI']['xmin']
        except KeyError:
            self.xmin = None
            checked_crop_roi_checkbox = False

        try:
            self.xmax = yaml_data['ROI']['xmax']
        except KeyError:
            self.xmax = None
            checked_crop_roi_checkbox = False

        try:
            self.ymin = yaml_data['ROI']['ymin']
        except KeyError:
            self.ymin = None
            checked_crop_roi_checkbox = False

        try:
            self.ymax = yaml_data['ROI']['ymax']
        except KeyError:
            self.ymax = None
            checked_crop_roi_checkbox = False

        try:
            self.autoreduction_mode = yaml_data['autoreduction']
        except KeyError:
            self.autoreduction_mode = False

        self.ui.crop_roi_checkBox.setChecked(checked_crop_roi_checkbox)
        self.crop_roi_checkBox_changed()

        try:
            self.ob_auto_selection_mode = yaml_data['OB_auto_selection']['mode']
        except KeyError:
            self.ob_auto_selection_mode = True

        try:
            self.ob_days = yaml_data['OB_auto_selection']['days']
        except KeyError:
            self.ob_days = 0

        try:
            self.ob_hours = yaml_data['OB_auto_selection']['hours']
        except KeyError:
            self.ob_hours = 3

        try:
            self.ob_minutes = yaml_data['OB_auto_selection']['minutes']
        except KeyError:
            self.ob_minutes = 0

        try:
            self.ob_max_number_of_files = yaml_data['ob_auto_selection']['max_number_of_files']
        except KeyError:
            self.ob_max_number_of_files = 10

        try:
            self.ob_use_max_number_of_files = yaml_data['ob_auto_selection']['use_max_number_of_files']
        except KeyError:
            self.ob_use_max_number_of_files = False

        return Status.ok

    def initialize_statusbar(self):
        self.setStyleSheet("QStatusBar{padding-left:8px;color:red;font-weight:bold;}")

    def initialize_config_file_name(self):
        autoreduce_config_path = "/HFIR/CG1D/shared/autoreduce/"
        if DEBUG:
            autoreduce_config_path = "/Users/j35/HFIR/CG1D/shared/autoreduce/"

        self.autoreduce_config_file = os.path.join(autoreduce_config_path, AUTOREDUCE_CONFIG_FILE_NAME)

        if os.path.exists(self.autoreduce_config_file):
            show_status_message(parent=self,
                                message=f"config: {self.autoreduce_config_file} located!",
                                status=StatusMessageStatus.working)
            return Status.ok
        else:
            show_status_message(parent=self,
                                message=f"{self.autoreduce_config_file} DOES NOT EXIST!",
                                status=StatusMessageStatus.error)
            self.ui.setEnabled(False)
            return Status.error

    # event handler
    def ipts_value_changed(self, value):
        self.ipts_number = self.ui.ipts_spinBox.value()

    def preview_clicked(self):
        o_history = History(parent=self)
        o_history.show()

    def activate_auto_reconstruction_clicked(self):
        activate_status = self.ui.activate_auto_reconstruction_checkBox.isChecked()
        self.ui.auto_reconstruction_frame.setEnabled(activate_status)

    def crop_roi_checkBox_changed(self):
        status = self.ui.crop_roi_checkBox.isChecked()
        self.ui.crop_roi_groupBox.setEnabled(status)
        self.ui.ymax_checkBox.setEnabled(status)
        self.ui.ymin_checkBox.setEnabled(status)
        self.ui.xmin_checkBox.setEnabled(status)
        self.ui.xmax_checkBox.setEnabled(status)

    def crop_xmin_checkbox_update(self):
        self.crop_xmin_checkBox_changed(self.ui.xmin_checkBox.isChecked())

    def crop_xmin_checkBox_changed(self, state):
        self.ui.xmin_spinBox.setEnabled(state)

    def crop_xmax_checkbox_update(self):
        self.crop_xmax_checkBox_changed(self.ui.xmax_checkBox.isChecked())

    def crop_xmax_checkBox_changed(self, state):
        self.ui.xmax_spinBox.setEnabled(state)

    def crop_ymin_checkbox_update(self):
        self.crop_ymin_checkBox_changed(self.ui.ymin_checkBox.isChecked())

    def crop_ymin_checkBox_changed(self, state):
        self.ui.ymin_spinBox.setEnabled(state)

    def crop_ymax_checkbox_update(self):
        self.crop_ymax_checkBox_changed(self.ui.ymax_checkBox.isChecked())

    def crop_ymax_checkBox_changed(self, state):
        self.ui.ymax_spinBox.setEnabled(state)

    def automatic_open_beam_checkBox_changed(self, state):
        self.ui.ob_groupBox.setEnabled(state)

    def ob_radioButton_changed(self):
        state_ob_time = self.ui.maximum_time_ob_radioButton.isChecked()
        list_ui = [self.ui.ob_days_spinBox,
                   self.ui.ob_days_label,
                   self.ui.ob_hours_spinBox,
                   self.ui.ob_hours_label,
                   self.ui.ob_minutes_spinBox,
                   self.ui.ob_minutes_label]
        for _ui in list_ui:
            _ui.setEnabled(state_ob_time)

    def ok_clicked(self):
        ipts_number = self.ui.ipts_spinBox.value()

        crop_roi_mode = self.ui.crop_roi_checkBox.isChecked()
        if crop_roi_mode:

            if self.ui.xmin_checkBox.isChecked():
                xmin = self.ui.xmin_spinBox.value()
            else:
                xmin = None

            if self.ui.ymin_checkBox.isChecked():
                ymin = self.ui.ymin_spinBox.value()
            else:
                ymin = None

            if self.ui.xmax_checkBox.isChecked():
                xmax = self.ui.xmax_spinBox.value()
            else:
                xmax = None

            if self.ui.ymax_checkBox.isChecked():
                ymax = self.ui.ymax_spinBox.value()
            else:
                ymax = None

        else:
            xmin = None
            ymin = None
            xmax = None
            ymax = None

        autoreduction_mode = self.ui.activate_auto_reconstruction_checkBox.isChecked()

        yaml_data = {'DataPath':
                         {'ipts': ipts_number,
                          },
                     'ROI': {
                         'mode': crop_roi_mode,
                         'xmin': xmin,
                         'ymin': ymin,
                         'xmax': xmax,
                         'ymax': ymax,
                            },
                     'autoreduction': autoreduction_mode,
                     }
        with io.open(self.autoreduce_config_file, 'w') as outfile:
            yaml.dump(yaml_data, outfile, default_flow_style=False, allow_unicode=True)

        self.close()

    def closeEvent(self, event):
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
