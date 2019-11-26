import os
from os import path
import logging
import shutil
import csv
from copy import deepcopy as cpy
from threading import Thread
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QVBoxLayout
import appdirs
import numpy as np
import simpleaudio as sa

from ui_annotator import Ui_MainWindow  # Annotator's generated ui file
from new_session import NewSession
from ui_alert import AlertOk, AlertYayNay
import session
from goto import GoTo



class Annotator(QMainWindow):

    # signals (must be defined here)
    now_show_info = QtCore.pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)

        # set up UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # connect signals (all used to make threads & updates possible)
        self.ui.viewer.show_new_file_info.connect(self.show_new_file_info)
        self.ui.table.show_msg.connect(self.show_timed_msg)
        self.now_show_info.connect(self.show_file_info)

        # connect new and load 
        self.ui.actionNew.triggered.connect(self.new_session)
        self.ui.actionLoad.triggered.connect(self.load_session)
        self.ui.actionExit.triggered.connect(self.quit_session)

        # class vars updated in load clips
        self.d_fp = None
        self.s_fp = None
        self.ss_fp = None
        self.min_dur = None
        self.f_ind = None
        self.wav_files = None

    def load_clips(self, d_fp, s_fp, ss_fp, min_dur, f_ind=0):
        self.status(self.logger, 'setting up session...')
        self.d_fp = d_fp
        self.s_fp = s_fp
        self.ss_fp = ss_fp
        self.min_dur = min_dur
        self.f_ind = f_ind

        self.ui.viewer.min_dur = min_dur

        # get all wav files contained in given directory or subdirectories
        self.wav_files = []
        for rootdir, dirs, filenames in os.walk(self.d_fp):
            filenames.sort()
            for filename in filenames:
                if 'wav' in filename or 'WAV' in filename:
                    self.wav_files.append(filename)
            break  # activate this line if only top level of directory wanted

        if not self.wav_files:
            self.status(self.logger, 'No wav files found in {}'.format(self.d_fp))
        else:
            # set up the csv table
            self.ui.table.load_table(self.s_fp)

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
            self.ui.actionGoto.setEnabled(True)
            self.ui.actionPlay.triggered.connect(self.play)
            self.ui.actionSave.triggered.connect(self.save)
            self.ui.actionNext.triggered.connect(self.next_)
            self.ui.actionPrev.triggered.connect(self.prev)
            self.ui.actionGoto.triggered.connect(self.goto)

            # this is so the spectrum viewer works properly
            lay = QVBoxLayout(self.ui.scrollAreaWidgetContents)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.addWidget(self.ui.viewer)
            self.ui.scrollArea.setWidgetResizable(True)

            # start by loading the first clip
            self.ui.viewer.new_clip(path.join(self.d_fp, self.curr_filename()))

    def curr_filename(self):
        return self.wav_files[self.f_ind]

    def curr_display_msg(self):
        return 'clip #{} ({}) recorded at {} {} on {} with sampling rate {}'.format(
            self.f_ind, 
            self.curr_filename(), 
            self.ui.viewer.curr_clip.metadata['time'], 
            self.ui.viewer.curr_clip.metadata['timezone'], 
            self.ui.viewer.curr_clip.metadata['date'],
            self.ui.viewer.curr_clip.sr
            )

    def new_session(self):
        self.status(self.logger, 'loading new session...')
        NewSession(self).show()

    def load_session(self):
        self.status(self.logger, 'loading existing session...')
        ss_fp, _ = QFileDialog.getOpenFileName(self, filter='(*.yaml)')

        try:
            d_fp, s_fp, min_dur, f_ind = session.load(ss_fp)
            self.load_clips(d_fp, s_fp, ss_fp, float(min_dur), int(f_ind))

        except FileNotFoundError:
            self.status(self.logger, 'unable to find: \'{}\''.format(ss_fp))

    def quit_session(self):
        self.status(self.logger, 'quitting session...')

        msg = 'Would you like to save your current session as a .yaml file?'

        def yes_fun():
            path, _ = QFileDialog.getSaveFileName(self, filter='(*.yaml)')

            try:
                session.save(path, self.d_fp, self.s_fp, self.min_dur, str(self.f_ind))
                self.exit()
                
            except FileNotFoundError:
                self.annotator.status('unable to find: \'{}\''.format(path))
                self.open()

        AlertYayNay(self, msg, yes_fun, lambda _: self.exit()).show()

    def exit(self):
        self.status(self.logger, 'exiting main application...')
        QApplication.quit()

    def play(self):
        self.status(self.logger, 'playing selection...')

        def thread_play():
            sa.WaveObject.from_wave_file('temp.wav').play()
            self.now_show_info.emit()

        Thread(target=thread_play).start()

    # def save_to_wav(self):
    #     start, end = self.ui.viewer.get_curr_selection()
    #     self.ui.viewer.curr_clip
    #     clip_16bit = (self.ui.viewer.curr_clip.data[start:end]).astype(np.int16)
    #     wavfile.write('./temp.wav', self.sr, clip_16bit)


    def save(self):
        start, end = self.ui.viewer.get_curr_selection()
        full_path = path.join(self.d_fp, self.curr_filename())
        self.ui.table.add_row([full_path, self.ui.tag.text(), start, end, self.ui.viewer.curr_clip.sr])

    def next_(self):
        self.status(self.logger, 'getting next clip...')
        self.f_ind += 1

        if self.f_ind >= len(self.wav_files):
            msg = 'There are no more wav files.\nYou are done!'
            AlertOk(self, msg, lambda _: self.exit()).show()
        else:
            Thread(target=self.ui.viewer.new_clip, args=[path.join(self.d_fp, self.curr_filename())]).start()

    def prev(self):
        self.status(self.logger, 'getting previous clip...')
        self.f_ind -= 1
        if self.f_ind < 0:
            msg = 'This is the first file.'
            alert = AlertOk(self, msg, lambda _: alert.done(os.EX_OK))
            alert.show()
        else:
            Thread(target=self.ui.viewer.new_clip, args=[path.join(self.d_fp, self.curr_filename())]).start()

    def goto(self):
        self.status(self.logger, 'going to...')
        GoTo(self).show()

    def show_timed_msg(self, logger, msg):
        self.status(logger, msg)
        def delay():
            time.sleep(1.5)
            self.now_show_info.emit() 
        Thread(target=delay).start()  

    def show_file_info(self):
        self.ui.statusbar.showMessage(self.curr_display_msg())

    def show_new_file_info(self, logger):
        logger.info(self.curr_display_msg())
        self.ui.statusbar.showMessage(self.curr_display_msg())

    def status(self, logger, msg):
        logger.info(msg)
        self.ui.statusbar.showMessage(msg)
