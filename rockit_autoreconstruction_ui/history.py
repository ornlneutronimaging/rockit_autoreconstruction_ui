from qtpy.QtWidgets import QDialog, QMenu
from qtpy import QtGui
import numpy as np
import os
import json
import datetime
import subprocess
import logging

from . import load_ui, refresh_file
from .utilities.table_handler import TableHandler
from .display_log import DisplayLog
from .utilities.file import read_ascii

SUCCESSFUL_MESSAGE = "RECONSTRUCTION LAUNCHED!"
IMARS3D_CONFIGFILE_EXTENSION = "_imars3d_config.json"


class HistoryColumnIndex:
	status = 0
	input_raw_folder = 1
	log_file_name = 2
	imars3d_config_file = 3
	script = 4
	output_folder = 5


class LogStatusColor:

	ok = QtGui.QColor(0, 255, 0)
	bad = QtGui.QColor(255, 0, 0)
	in_progress = QtGui.QColor(0, 255, 250)


class LogStatus:
	ok = "success!"
	bad = "failed!"
	check_log = "Check log file for status!"
	file_does_not_exist = "File missing!"
	in_progress = "in progress!"


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
		self.initialization()
		self.update_table()
		self.update_refresh_time()

	def initialization(self):
		o_table = TableHandler(table_ui=self.ui.history_tableWidget)

		o_table.full_reset()

		for _col in np.arange(6):
			o_table.insert_empty_column(column=0)

		o_table.set_column_names(["Status", "Input raw folder", "Log file name", "iMars3d config. file", "Script", "Output folder"])
		column_sizes = [85, 300, 300, 300, 300, 300]
		o_table.set_column_sizes(column_sizes=column_sizes)

		self.autoreduce_path = self.parent.ipts_folder + os.path.join(f"IPTS-{self.parent.ipts}/shared/autoreduce/")
		self.base_raw_folder = self.parent.ipts_folder + os.path.join(f"IPTS-{self.parent.ipts}/raw/ct_scans")
		history_file = self.autoreduce_path + "ct_scans_folder_processed.json"
		self.history_file = history_file
		icon_refresh = QtGui.QIcon(refresh_file)
		self.ui.refresh_button.setIcon(icon_refresh)

	def output_folder_exists(self, folder):
		"""Check if the output folder is already there. if not, status is in progress"""
		if os.path.exists(folder):
			return True
		return False

	def update_table(self):
		if os.path.exists(self.history_file):
			with open(self.history_file, 'r') as json_file:
				history_data = json.load(json_file)
			list_folders = history_data['list_folders']
			o_table = TableHandler(table_ui=self.ui.history_tableWidget)
			for _row, _folder in enumerate(list_folders):
				o_table.insert_empty_row(row=_row)
				o_table.insert_item(row=_row,
									column=HistoryColumnIndex.input_raw_folder,
									editable=False,
									value=os.path.basename(_folder))

				folder_name = o_table.get_item_str_from_cell(row=_row, column=HistoryColumnIndex.input_raw_folder)
				base_folder_name = os.path.basename(folder_name) + "_autoreduce.log"
				log_file_name = os.path.join(os.path.join(self.autoreduce_path, "reduction_log"), base_folder_name)

				# only for the first row, retrieve top path
				if _row == 0:
					self.ui.raw_folder.setText(self.base_raw_folder)
					self.ui.autoreduce_folder.setText(self.autoreduce_path)

				o_table.insert_item(row=_row,
						column=HistoryColumnIndex.log_file_name,
						editable=False,
						value=os.path.basename(log_file_name))

				output_folder = os.path.join(self.autoreduce_path, os.path.basename(folder_name))
				o_table.insert_item(row=_row,
						column=HistoryColumnIndex.output_folder,
						editable=False,
						value=output_folder)

				if not os.path.exists(log_file_name):
					log_status = LogStatus.bad
					qcolor=LogStatusColor.bad

				else:

					log_status = LogStatus.check_log

					# if last line is done we can check if the file is there too
					with open(log_file_name, 'r') as f:
						log_data = f.readlines()

					if log_data[-1].startswith("Done!"):
						if self.output_folder_exists(output_folder):
							qcolor = LogStatusColor.ok
							log_status = LogStatus.ok
						else:
							qcolor = LogStatusColor.bad
							log_status = LogStatus.bad
					else:
						qcolor=LogStatusColor.in_progress
						log_status = LogStatus.in_progress

				o_table.insert_item(row=_row,
									column=HistoryColumnIndex.status,
									editable=False,
									value=log_status)
				
				# imars3d config file 
				imars3d_config_file = os.path.basename(output_folder + IMARS3D_CONFIGFILE_EXTENSION)
				o_table.insert_item(row=_row,
						column=HistoryColumnIndex.imars3d_config_file,
						editable=False,
						value=imars3d_config_file)

				# cmd
				full_imars3d_config_file = os.path.join(self.autoreduce_path, imars3d_config_file)
				if os.path.exists(full_imars3d_config_file):
					with open(full_imars3d_config_file, 'r') as json_file:
						config_file = json.load(json_file)
					cmd = config_file.get("cmd", "Not defined!")
				else:
					cmd = "Not defined!"
				o_table.insert_item(row=_row,
						column=HistoryColumnIndex.script,
						editable=False,
						value=cmd)

				o_table.set_background_color_of_row(row=_row,
													qcolor=qcolor)

		else:
			self.ui.error_label.setText("file does not exists yet!")

	def history_right_click(self, point):
		menu = QMenu(self)

		display_log = menu.addAction("Preview reconstruction log ...")
		menu.addSeparator()
		remove_selection = menu.addAction("Automatically re-run reconstruction!")
		rerun_selection = menu.addAction("Manually re-run reconstruction!")

		action = menu.exec_(QtGui.QCursor.pos())

		o_table = TableHandler(table_ui=self.ui.history_tableWidget)
		selected_rows = o_table.get_rows_of_table_selected()

		if action == remove_selection:
			for _row in selected_rows[::-1]:
				o_table.remove_row(_row)

		elif action == rerun_selection:
			for _row in selected_row(_row):
				cmd = o_table.get_item_str_from_cell(row=_row,
										 column=4)
				logging.info(f"Manually running cmd: {cmd}")
				proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, universal_newlines=True)
				proc.communicate()

		elif action == display_log:

			for _row in selected_rows:

				# figure out log file name
				folder_name = o_table.get_item_str_from_cell(row=_row, column=0)
				base_folder_name = os.path.basename(folder_name) + "_autoreduce.log"
				metadata_name = os.path.basename(folder_name) + "_sample_ob_dc_metadata.json"
				metadata_file_name = os.path.join(os.path.join(self.autoreduce_path, "reduction_log"), metadata_name)
				log_file_name = os.path.join(os.path.join(self.autoreduce_path, "reduction_log"), base_folder_name)

				o_display = DisplayLog(parent=self,
									   log_file_name=log_file_name,
									   metadata_file_name=metadata_file_name)
				o_display.show()

	def ok_pushed(self):
		o_table = TableHandler(table_ui=self.ui.history_tableWidget)
		nbr_row = o_table.row_count()
		table_content = []
		for _row in np.arange(nbr_row):
			cell_str = o_table.get_item_str_from_cell(row=_row, column=0)
			table_content.append(cell_str)
		dict = {'list_folders': table_content}
		with open(self.history_file, 'w') as json_file:
			json.dump(dict, json_file)

	def refresh_button_clicked(self):
		o_table = TableHandler(table_ui=self.ui.history_tableWidget)
		o_table.remove_all_rows()
		self.update_table()
		# inform of last refresh
		self.update_refresh_time()

	def update_refresh_time(self):
		now = datetime.datetime.now()
		now_text = f"{now.hour}:{now.minute}:{now.second}"
		self.ui.last_refresh_label.setText(now_text)
