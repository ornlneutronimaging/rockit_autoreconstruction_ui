from qtpy.QtWidgets import QDialog
import os
import json

from . import load_ui


class History(QDialog):

	history_file = None

	def __init__(self, parent=None):
		self.parent = parent

		QDialog.__init__(self, parent=parent)
		ui_full_path = os.path.join(os.path.dirname(__file__),
									os.path.join('ui',
												 'history.ui'))
		self.ui = load_ui(ui_full_path, baseinstance=self)
		self.setWindowTitle(f"History of {self.parent.ipts} ct_scans folders reduced!")

		history_file = self.parent.ipts_folder + os.path.join(f"IPTS-{self.parent.ipts}/shared/autoreduce/ct_scans_folder_processed.json")
		print(history_file)
		if os.path.exists(history_file):
			with open(history_file, 'r') as json_file:
				history_data = json.load(json_file)
			list_folders = history_data['list_folders']
			list_folders_formatted = "\n".join(list_folders)
			self.ui.history_textEdit.setText(list_folders_formatted)

		else:
			self.ui.history_textEdit.setText("file does not exists!")

	def ok_pushed(self):
		print("ok pushed")
