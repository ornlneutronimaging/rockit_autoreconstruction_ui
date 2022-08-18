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
		self.ui.folder_label.setText(os.path.dirname(log_file_name))

		if os.path.exists(log_file_name):
			log_text = self.read_ascii(log_file_name)
		else:
			log_text = "File is missing!"
		self.ui.log_textEdit.setText(log_text)

	def ok_pushed(self):
		self.close()

	def read_ascii(self, filename=''):
		'''return contain of an ascii file'''
		with open(filename, 'r') as f:
			text = f.read()
		return text
