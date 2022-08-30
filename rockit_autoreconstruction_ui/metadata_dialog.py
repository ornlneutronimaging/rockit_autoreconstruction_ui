from qtpy.QtWidgets import QDialog
from qtpy import QtGui
import json
import os

from . import load_ui
from .utilities.table_handler import TableHandler

LIST_KEYS_TO_IGNORE = ['filename', 'time_stamp', 'time_stamp_user_format']


class MetadataDialog(QDialog):

	history_file = None

	def __init__(self, parent=None, metadata_file_name=None):
		self.parent = parent
		self.metadata_file_name = metadata_file_name

		QDialog.__init__(self, parent=parent)
		ui_full_path = os.path.join(os.path.dirname(__file__),
									os.path.join('ui',
												 'dialog_metadata.ui'))
		self.ui = load_ui(ui_full_path, baseinstance=self)
		self.setWindowTitle(f"Sample, OB and DC metadata file")
		self.ui.folder_of_input_file.setText(os.path.dirname(self.metadata_file_name))
		self.ui.name_of_input_file_label.setText(os.path.basename(self.metadata_file_name))
		self.init_tables()

		self.load_json()
		self.fill_tables()

	def init_tables(self):
		column_sizes = [250, 300]

		o_sample = TableHandler(table_ui=self.ui.sample_tableWidget)
		o_sample.set_column_sizes(column_sizes=column_sizes)

		o_ob = TableHandler(table_ui=self.ui.ob_tableWidget)
		o_ob.set_column_sizes(column_sizes=column_sizes)

		o_dc = TableHandler(table_ui=self.ui.dc_tableWidget)
		o_dc.set_column_sizes(column_sizes=column_sizes)

	def load_json(self):
		with open(self.metadata_file_name, 'r') as json_file:
			self.data = json.load(json_file)

	def fill_tables(self):

		# sample
		o_sample = TableHandler(table_ui=self.ui.sample_tableWidget)
		sample_dict = self.data['sample']
		_row_index = 0
		for _key in sample_dict.keys():
			if _key in LIST_KEYS_TO_IGNORE:
				continue

			o_sample.insert_empty_row(row=_row_index)

			o_sample.insert_item(row=_row_index,
								 column=0,
								 editable=False,
								 value=sample_dict[_key]['name'])

			o_sample.insert_item(row=_row_index,
								 column=1,
								 editable=False,
								 value=sample_dict[_key]['value'])
			_row_index += 1

	def ok_pushed(self):
		self.close()
