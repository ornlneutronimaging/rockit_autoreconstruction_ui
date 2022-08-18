from qtpy.QtWidgets import QDialog, QMenu
from qtpy import QtGui

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
		self.history_file = history_file
		if os.path.exists(history_file):
			with open(history_file, 'r') as json_file:
				history_data = json.load(json_file)
			list_folders = history_data['list_folders']
			list_folders_formatted = "\n".join(list_folders)
			self.ui.history_textEdit.setPlainText(list_folders_formatted)

		else:
			self.ui.history_textEdit.setPlainText("file does not exists yet!")

	def history_right_click(self, point):
		menu = QMenu(self)

		remove_selection = menu.addAction("Remove selected row(s)")
		display_log = menu.addAction("Preview reconstruction log")

		action = menu.exec_(QtGui.QCursor.pos())
		if action == remove_selection:
			print("remove")
		elif action == display_log:
			print("display")

	def ok_pushed(self):
		unformatted_content = self.ui.history_textEdit.toPlainText()
		formatted_content = unformatted_content.split("\n")
		# remove empty row and duplicates
		formatted_content = list(set([_entry for _entry in formatted_content if _entry != ""]))
		dict = {'list_folders': formatted_content}
		with open(self.history_file, 'w') as json_file:
			json.dump(dict, json_file)

		self.close()
