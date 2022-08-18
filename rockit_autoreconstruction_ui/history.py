from qtpy.QtWidgets import QDialog, QMenu
from qtpy import QtGui

import os
import json

from . import load_ui
from .utilities.table_handler import TableHandler
from .display_log import DisplayLog


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

		self.autoreduce_path = self.parent.ipts_folder + os.path.join(f"IPTS-{self.parent.ipts}/shared/autoreduce/")
		history_file = self.autoreduce_path + "ct_scans_folder_processed.json"
		self.history_file = history_file
		if os.path.exists(history_file):
			with open(history_file, 'r') as json_file:
				history_data = json.load(json_file)
			list_folders = history_data['list_folders']
			o_table = TableHandler(table_ui=self.ui.history_tableWidget)
			for _row, _folder in enumerate(list_folders):
				o_table.insert_empty_row(row=_row)
				o_table.insert_item(row=_row,
									column=0,
									editable=False,
									value=_folder)
		else:
			self.ui.error_label.setText("file does not exists yet!")

	def history_right_click(self, point):
		menu = QMenu(self)

		display_log = menu.addAction("Preview reconstruction log ...")
		menu.addSeparator()
		remove_selection = menu.addAction("Remove selected row(s)")

		action = menu.exec_(QtGui.QCursor.pos())

		o_table = TableHandler(table_ui=self.ui.history_tableWidget)
		selected_rows = o_table.get_rows_of_table_selected()

		if action == remove_selection:
			for _row in selected_rows[::-1]:
				o_table.remove_row(_row)

		elif action == display_log:

			for _row in selected_rows:

				# figure out log file name
				folder_name = o_table.get_item_str_from_cell(row=_row, column=0)
				base_folder_name = os.path.basename(folder_name) + "_autoreduce.log"
				log_file_name = os.path.join(os.path.join(self.autoreduce_path, "reduction_log"), base_folder_name)

				o_display = DisplayLog(parent=self,
									   log_file_name=log_file_name)
				o_display.show()

	def ok_pushed(self):
		unformatted_content = self.ui.history_textEdit.toPlainText()
		formatted_content = unformatted_content.split("\n")
		# remove empty row and duplicates
		formatted_content = list(set([_entry for _entry in formatted_content if _entry != ""]))
		dict = {'list_folders': formatted_content}
		with open(self.history_file, 'w') as json_file:
			json.dump(dict, json_file)

		self.close()
