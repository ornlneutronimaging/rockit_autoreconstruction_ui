from qtpy.QtWidgets import QDialog

import os

from . import load_ui


class DisplayMasterLog(QDialog):

	history_file = None

	def __init__(self, parent=None):
		self.parent = parent
		self.log_file_name = os.path.join(self.parent.ipts_folder, "shared/autoreduce/reduce_cg1d.log")

		QDialog.__init__(self, parent=parent)
		ui_full_path = os.path.join(os.path.dirname(__file__),
									os.path.join('ui',
												 'display_master_log.ui'))
		self.ui = load_ui(ui_full_path, baseinstance=self)
		self.ui.file_label.setText(self.log_file_name)

		if os.path.exists(self.log_file_name):
			log_text = self.read_ascii(self.log_file_name)
		else:
			log_text = "File is missing!"
		self.ui.log_textEdit.setText(log_text)

	def ok_pushed(self):
		self.close()

	def clear_pushed(self):
		with open(self.log_file_name, 'w') as f:
			f.write("")

	def read_ascii(self, filename=''):
		"""return contain of an ascii file"""
		with open(filename, 'r') as f:
			text = f.read()
		return text
