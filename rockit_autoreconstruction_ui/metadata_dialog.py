from qtpy.QtWidgets import QDialog
from qtpy import QtGui

import os

from . import load_ui
from . import refresh_file
from .utilities.file import read_ascii


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
		self.setWindowTitle(f"{os.path.basename(self.metadata_file_name)}")

		# self.ui.folder_label.setText(os.path.dirname(log_file_name))
		# self.update_display_text()
		#
		# if os.path.exists(self.metadata_file_name):
		# 	self.ui.preview_metadata_pushButton.setVisible(True)
		# else:
		# 	self.ui.preview_metadata_pushButton.setVisible(False)
		#
		# icon_refresh = QtGui.QIcon(refresh_file)
		# self.ui.refresh_pushButton.setIcon(icon_refresh)

	def ok_pushed(self):
		self.close()
