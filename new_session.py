import logging
import os
from os import path

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QDialog, QDialogButtonBox, QLabel, QPushButton

from ui_newsession import Ui_Dialog  # NewSession's generated ui file
from ui_alert import AlertYayNay



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
        ok_button.clicked.connect(self.open_session)

        # vars set in dialog
        self.d_fp = None
        self.s_fp = None
        
    def get_data_folder(self):
        path = QFileDialog.getExistingDirectory(self)
        self.ui.dataFolder.setText(path)
        self.d_fp = path
        self.logger.info('selected {} as data path'.format(path))

    def get_save_folder(self):
        path, _ = QFileDialog.getSaveFileName(self, filter='(*.csv)')
        self.ui.saveFolder.setText(path)
        self.s_fp = path
        self.logger.info('selected {} as save file'.format(path))

    def open_session(self):
        self.annotator.status(self.logger, 'opening new session...')
        min_dur = float(self.ui.minDur.text())

        if self.d_fp is None:
            self.d_fp = self.ui.dataFolder.text()

        if self.s_fp is None:
            self.s_fp = self.ui.saveFolder.text()

        if path.exists(self.s_fp):
            fp, fn = path.split(self.s_fp)
            msg = 'The data file {} already exists in {}.\nWould you like to proceed?'.format(fn, fp)
            def yay_fun():
                self.annotator.load_clips(
                self.d_fp, self.s_fp, 'ss.txt', min_dur, 0)
                alert.done(os.EX_OK)
            alert = AlertYayNay(self, msg, yay_fun, lambda _: alert.done(os.EX_OK))
            alert.show()

        else:
            self.annotator.load_clips(self.d_fp, self.s_fp, 'ss.txt', min_dur, 0)
