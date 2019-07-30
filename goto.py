import logging
import os
from os import path

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QDialog, QDialogButtonBox, QLabel, QPushButton

from ui_goto import Ui_Dialog  # Goto's generated ui file



class GoTo(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent=parent)
        self.annotator = parent
        self.logger = logging.getLogger(self.__class__.__name__)

        # set up UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        ok_button = self.ui.buttonBox.button(QDialogButtonBox.Ok)
        cancel_button = self.ui.buttonBox.button(QDialogButtonBox.Cancel)

        # connect buttons
        ok_button.clicked.connect(self.goto_file)
        cancel_button.clicked.connect(lambda _: self.done(os.EX_OK))
        self.ui.chooseButton.clicked.connect(self.get_filename)

    def get_filename(self):
        fp, _ = QFileDialog.getOpenFileName(self, directory=self.annotator.d_fp, filter='(*.wav)')
        _, fn = path.split(fp)
        self.ui.filename.setText(fn)

    def goto_file(self):
        filename = self.ui.filename.text()

        try:
            f_ind = self.annotator.wav_files.index(filename)
            self.annotator.f_ind = f_ind - 1  # use -1 becuase next_ method will incrememnt
            self.annotator.next_()
        except ValueError as err:
            self.annotator.show_timed_msg(self.logger, 'Error: Unable to find \'{}\'.'.format(filename))
            self.logger.info(err)

        self.done(os.EX_OK)
