import logging

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QDialog, QDialogButtonBox

from ui_newsession import Ui_Dialog



class NewSession(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent=parent)
        self.annotator = parent
        self.logger = logging.getLogger(self.__class__.__name__)

        # set up UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        ok_button = self.ui.buttonBox.button(QDialogButtonBox.Ok)

        # connect buttons
        self.ui.dataFolderButton.clicked.connect(self.get_data_folder)
        self.ui.saveFolderButton.clicked.connect(self.get_save_folder)
        ok_button.clicked.connect(self.open)

        # vars set in dialog
        self.d_fp = None
        self.s_fp = None
        
    def get_data_folder(self):
        folder = QFileDialog.getExistingDirectory(self)
        self.ui.dataFolder.setText(folder)
        self.d_fp = folder
        self.logger.info('selected {}'.format(folder))

    def get_save_folder(self):
        folder = QFileDialog.getExistingDirectory(self)
        self.ui.saveFolder.setText(folder)
        self.s_fp = folder
        self.logger.info('selected {}'.format(folder))

    def open(self):
        csv_fn = self.ui.csvFileName.text()
        min_dur = float(self.ui.minDur.text())
        self.annotator.load_clips(self.d_fp, self.s_fp, csv_fn, 'ss.txt', min_dur, 0, 0)
