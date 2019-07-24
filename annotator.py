import os
from os import path
import logging
import shutil
import csv
from copy import deepcopy as cpy

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QVBoxLayout
import appdirs
import numpy as np
from playsound import playsound

from ui_annotator import Ui_MainWindow
from new_session import NewSession
from save_session import SaveSession
import session
from ui_alert import AlertOk



class Annotator(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)

        # set up UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # connect new and load 
        self.ui.actionNew.triggered.connect(self.new_session)
        self.ui.actionLoad.triggered.connect(self.load_session)
        self.ui.actionExit.triggered.connect(self.quit_session)

        # class vars updated in load clips
        self.d_fp = None
        self.s_fp = None
        self.csv_fn = None
        self.ss_fp = None
        self.min_dur = None
        self.f_ind = None
        self.m_ind = None
        self.wav_files = None

    def load_clips(self, d_fp, s_fp, csv_fn, ss_fp, min_dur, f_ind=0, m_ind=0):
        self.d_fp = d_fp
        self.s_fp = s_fp
        self.csv_fn = csv_fn
        self.ss_fp = ss_fp
        self.min_dur = min_dur
        self.f_ind = f_ind
        self.m_ind = m_ind

        # get all wav files contained in given directory or subdirectories
        self.wav_files = []
        for rootdir, dirs, filenames in os.walk(self.d_fp):
            for filename in filenames:
                if 'wav' in filename or 'WAV' in filename:
                    self.wav_files.append(filename)
            break  # activate this line if only top level of directory wanted

        if not self.wav_files:
            self.logger.info('There are no wav files in {}'.format(self.d_fp))
        else:
            # set up the csv table
            self.ui.table.load_table(path.join(self.s_fp, self.csv_fn))

            # enable buttons and connect to slots
            self.ui.playButton.setEnabled(True)
            self.ui.saveButton.setEnabled(True)
            self.ui.nextButton.setEnabled(True)
            self.ui.prevButton.setEnabled(True)
            self.ui.playButton.clicked.connect(self.play)
            self.ui.saveButton.clicked.connect(self.save)
            self.ui.nextButton.clicked.connect(self.next_)
            self.ui.prevButton.clicked.connect(self.prev)

            # enable menu actions and connect to slots
            self.ui.actionPlay.setEnabled(True)
            self.ui.actionSave.setEnabled(True)
            self.ui.actionNext.setEnabled(True)
            self.ui.actionPrev.setEnabled(True)
            self.ui.actionPlay.triggered.connect(self.play)
            self.ui.actionSave.triggered.connect(self.save)
            self.ui.actionNext.triggered.connect(self.next_)
            self.ui.actionPrev.triggered.connect(self.prev)

            # this is so the spectrum viewer works properly
            lay = QVBoxLayout(self.ui.scrollAreaWidgetContents)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.addWidget(self.ui.viewer)
            self.ui.scrollArea.setWidgetResizable(True)

            # start by loading the first clip
            self.ui.viewer.new_clip(path.join(self.d_fp, self.curr_filename()))

    def curr_filename(self):
        return self.wav_files[self.f_ind]

    def curr_save_filename(self):
        return 'v{}-{}.wav'.format(self.curr_filename().split('.')[0], self.m_ind)

    def new_session(self):
        self.logger.info('loading new session...')
        dialog = NewSession(self)
        dialog.show()

    def load_session(self):
        self.logger.info('loading existing session...')
        ss_fp, _ = QFileDialog.getOpenFileName(self, filter='(*.yaml)')

        try:
            d_fp, s_fp, csv_fn, min_dur, f_ind, m_ind = session.load(ss_fp)
            self.load_clips(d_fp, s_fp, csv_fn, ss_fp, float(min_dur), int(f_ind), int(m_ind))
            self.logger.info('loaded {}'.format(ss_fp))

        except FileNotFoundError:
            self.logger.info('unable to find: \'{}\''.format(ss_fp))

    def quit_session(self):
        self.logger.info('quitting session...')
        dialog = SaveSession(self)
        dialog.show()

    def exit(self):
        self.logger.info('exiting main application...')
        QApplication.quit()

    def play(self):
        self.logger.info('playing sound...')
        playsound('./support/temp.wav')  # TODO: do on a diff thread

    def save(self):
        savepath = path.join(self.s_fp, self.curr_save_filename())
        shutil.copy('./support/temp.wav', savepath)  # TODO: only do this if csv successful
        self.logger.info('saved audio file as {}'.format(savepath))

        self.ui.table.add_row([savepath, self.ui.tag.text()])

        self.m_ind += 1  

    def next_(self):
        self.f_ind += 1
        if self.f_ind >= len(self.wav_files):
            msg = 'There are no more wav files.\nYou are done!'
            alert = AlertOk(self, msg, lambda _: self.exit())
            alert.show()
        else:
            # figure out what next m_ind should be  TODO: maybe look in csv instead?
            highest = -1
            for filename in os.listdir(self.s_fp):
                if self.curr_filename().split('.')[0] in filename:  # if voc pertains to current file
                    ind = int(filename.split('-')[-1].split('.')[0])
                    if ind > highest:
                        highest = cpy(ind)

            self.m_ind = highest + 1

            self.ui.viewer.new_clip(path.join(self.d_fp, self.curr_filename()))
            self.logger.info('displaying file #{} ({})'.format(self.f_ind, self.curr_filename()))

    def prev(self):
        self.f_ind -= 1
        if self.f_ind < 0:
            msg = 'This is the first file.'
            alert = AlertOk(self, msg, lambda _: alert.done(os.EX_OK))
            alert.show()
        else:
            # figure out what next m_ind should be
            highest = -1
            for filename in os.listdir(self.s_fp):
                if self.curr_filename().split('.')[0] in filename:  # if voc pertains to current file
                    ind = int(filename.split('-')[-1].split('.')[0])
                    if ind > highest:
                        highest = cpy(ind)

            self.m_ind = highest + 1

            self.ui.viewer.new_clip(path.join(self.d_fp, self.curr_filename()))
            self.logger.info('displaying file #{} ({})'.format(self.f_ind, self.curr_filename()))
