from qtpy.QtWidgets import QDialog

import os

from . import load_ui


class DisplayLog(QDialog):

	history_file = None

	def __init__(self, parent=None, log_file_name=None):
		self.parent = parent

		QDialog.__init__(self, parent=parent)
		ui_full_path = os.path.join(os.path.dirname(__file__),
									os.path.join('ui',
												 'display_log.ui'))
		self.ui = load_ui(ui_full_path, baseinstance=self)
		self.setWindowTitle(f"log file of {os.path.basename(log_file_name)}")
		self.ui.folder_label.setText(log_file_name)

	def ok_pushed(self):
		self.close()
