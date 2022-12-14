from qtpy.QtWidgets import QDialog
from qtpy import QtGui

import os

from . import load_ui
from . import refresh_file
from .utilities.file import read_ascii
from .metadata_dialog import MetadataDialog


class DisplayLog(QDialog):

	history_file = None

	def __init__(self, parent=None, log_file_name=None, metadata_file_name=None):
		self.parent = parent
		self.log_file_name = log_file_name
		self.metadata_file_name = metadata_file_name

		QDialog.__init__(self, parent=parent)
		ui_full_path = os.path.join(os.path.dirname(__file__),
									os.path.join('ui',
												 'display_log.ui'))
		self.ui = load_ui(ui_full_path, baseinstance=self)
		self.setWindowTitle(f"log file of {os.path.basename(log_file_name)}")
		self.ui.folder_label.setText(os.path.dirname(log_file_name))
		self.update_display_text()

		if os.path.exists(self.metadata_file_name):
			self.ui.preview_metadata_pushButton.setVisible(True)
		else:
			self.ui.preview_metadata_pushButton.setVisible(False)

		icon_refresh = QtGui.QIcon(refresh_file)
		self.ui.refresh_pushButton.setIcon(icon_refresh)

	def refresh_pushButton_pressed(self):
		self.update_display_text()

	def update_display_text(self):
		if os.path.exists(self.log_file_name):
			log_text = read_ascii(self.log_file_name)
		else:
			log_text = "File is missing!"
		self.ui.log_textEdit.setText(log_text)
		# move anchor to bottom of the text
		self.ui.log_textEdit.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

	def preview_metadata_pushButton_pressed(self):
		o_metadata = MetadataDialog(parent=self,
									metadata_file_name=self.metadata_file_name)
		o_metadata.show()

	def ok_pushed(self):
		self.close()
