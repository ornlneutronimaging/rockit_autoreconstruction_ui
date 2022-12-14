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

		self.init_ob_local_reference_dict()
		self.init_ob_combobox()

		self.init_dc_local_reference_dict()
		self.init_dc_combobox()

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
		self.fill_sample_table()
		# self.fill_ob_table()

	def fill_sample_table(self):
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

	def init_ob_local_reference_dict(self):
		self.ob_local_dict = self.get_local_reference_dict(key='ob')

	def init_dc_local_reference_dict(self):
		self.dc_local_dict = self.get_local_reference_dict(key='dc')

	def get_local_reference_dict(self, key=None):
		_dict = self.data[key]
		local_reference_dict = {}
		for _key in _dict.keys():
			local_reference_dict[_dict[_key]['filename']] = _key
		return local_reference_dict

	def init_ob_combobox(self):
		ob_local_reference_dict = self.ob_local_dict
		list_files = list(ob_local_reference_dict.keys())
		self.ui.ob_comboBox.addItems(list_files)

	def init_dc_combobox(self):
		dc_local_reference_dict = self.dc_local_dict
		list_files = list(dc_local_reference_dict.keys())
		self.ui.dc_comboBox.addItems(list_files)

	def ob_index_changed(self, index):
		combo_text = self.ui.ob_comboBox.currentText()
		metadata_index = self.ob_local_dict[combo_text]
		ob_dict = self.data['ob'][metadata_index]
		o_ob = TableHandler(table_ui=self.ui.ob_tableWidget)
		o_ob.remove_all_rows()

		_row_index = 0
		for _key in ob_dict.keys():
			if _key in LIST_KEYS_TO_IGNORE:
				continue

			o_ob.insert_empty_row(row=_row_index)

			o_ob.insert_item(row=_row_index,
								 column=0,
								 editable=False,
								 value=ob_dict[_key]['name'])

			o_ob.insert_item(row=_row_index,
								 column=1,
								 editable=False,
								 value=ob_dict[_key]['value'])
			_row_index += 1

	def dc_index_changed(self, index):
		combo_text = self.ui.dc_comboBox.currentText()
		metadata_index = self.dc_local_dict[combo_text]
		dc_dict = self.data['dc'][metadata_index]
		o_dc = TableHandler(table_ui=self.ui.dc_tableWidget)
		o_dc.remove_all_rows()

		_row_index = 0
		for _key in dc_dict.keys():
			if _key in LIST_KEYS_TO_IGNORE:
				continue

			o_dc.insert_empty_row(row=_row_index)

			o_dc.insert_item(row=_row_index,
								 column=0,
								 editable=False,
								 value=dc_dict[_key]['name'])

			o_dc.insert_item(row=_row_index,
								 column=1,
								 editable=False,
								 value=dc_dict[_key]['value'])
			_row_index += 1

	def sample_selection_changed(self):
		self.table_selection_changed(source='sample')

	def ob_selection_changed(self):
		self.table_selection_changed(source='ob')

	def dc_selection_changed(self):
		self.table_selection_changed(source='dc')

	def table_selection_changed(self, source='sample'):
		list_table_ui = list([self.ui.sample_tableWidget, self.ui.ob_tableWidget, self.ui.dc_tableWidget])
		if source == 'sample':
			index_to_pop = 0
		elif source == 'ob':
			index_to_pop = 1
		else:
			index_to_pop = 2
		source_table_ui = list_table_ui.pop(index_to_pop)

		o_source = TableHandler(table_ui=source_table_ui)
		selected_row = o_source.get_row_selected()

		for _table_ui in list_table_ui:
			o_table = TableHandler(table_ui=_table_ui)
			o_table.block_signals(True)
			o_table.select_row(row=selected_row)
			o_table.block_signals(False)

	def ok_pushed(self):
		self.close()
