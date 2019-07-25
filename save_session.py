import os
import logging

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QDialog, QDialogButtonBox

from ui_savesession import Ui_Dialog
import session



class SaveSession(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent=parent)
        self.annotator = parent
        self.logger = logging.getLogger(self.__class__.__name__)

        # set up UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        yay_button = self.ui.buttonBox.button(QDialogButtonBox.Yes)
        nay_button = self.ui.buttonBox.button(QDialogButtonBox.No)

        # connect buttons
        yay_button.clicked.connect(self.save_session)
        nay_button.clicked.connect(self.exit)
        
    def save_session(self):
        path, _ = QFileDialog.getSaveFileName(self, filter='(*.yaml)')

        try:
            session.save(path,
                self.annotator.d_fp, 
                self.annotator.s_fp, 
                self.annotator.csv_fn, 
                str(self.annotator.min_dur),
                str(self.annotator.f_ind), 
                str(self.annotator.m_ind)
            )
            
            self.exit()
            
        except FileNotFoundError:
            self.logger.info('unable to find: \'{}\''.format(path))
            self.open()

    def exit(self):
        self.logger.info('exiting save session...')
        self.annotator.exit()
