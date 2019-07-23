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



class Annotator(QMainWindow):
    def __init__(self, d_fp, s_fp, csv_fn, ss_fp, min_dur, f_ind=0, d_ind=0):
        QMainWindow.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)
        print()

        # set up UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # this is so the spectrum viewer works properly
        lay = QVBoxLayout(self.ui.scrollAreaWidgetContents)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.ui.viewer)
        self.ui.scrollArea.setWidgetResizable(True)

        # connect actions and buttons
        self.ui.playButton.clicked.connect(self.play)
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.nextButton.clicked.connect(self.next_)
        self.ui.prevButton.clicked.connect(self.prev)
        self.ui.actionPlay.triggered.connect(self.play)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionNext.triggered.connect(self.next_)
        self.ui.actionPrev.triggered.connect(self.prev)
        self.ui.actionOpen.triggered.connect(self.open)
        # self.ui.actionExit.triggered.connect(self.exit)

        # class vars
        self.d_fp = d_fp
        self.s_fp = s_fp
        self.csv_fn = csv_fn
        self.ss_fp = ss_fp
        self.min_dur = min_dur
        self.f_ind = f_ind
        self.d_ind = d_ind

        # get all wav files contained in given directory or subdirectories
        self.wav_files = []
        for rootdir, dirs, filenames in os.walk(self.d_fp):
            for filename in filenames:
                if 'wav' in filename or 'WAV' in filename:
                    self.wav_files.append(filename)
            break  # activate this line if only top level of directory wanted

        # set up the csv table
        self.ui.table.load_table(path.join(self.s_fp, self.csv_fn))

        # start by loading the first clip
        self.ui.viewer.new_clip(path.join(self.d_fp, self.curr_filename()))

    def curr_filename(self):
        return self.wav_files[self.f_ind]

    def curr_save_filename(self):
        return 'v{}-{}.wav'.format(self.curr_filename().split('.')[0], self.d_ind)        

    def open(self):
        folder = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)
        self.logger.info('selected {}'.format(folder))

    def play(self):
        playsound('./support/temp.wav')  # TODO: do on a diff thread

    def save(self):
        savepath = path.join(self.s_fp, self.curr_save_filename())
        shutil.copy('./support/temp.wav', savepath)  # TODO: only do this if csv successful
        self.logger.info('saved to {}'.format(savepath))

        self.ui.table.add_row([savepath, self.ui.tag.text()])

        self.d_ind += 1  

    def next_(self):
        self.f_ind += 1
        if self.f_ind >= len(self.wav_files):
            pass  # TODO: exit program

        # figure out what next d_ind should be  TODO: maybe look in csv instead?
        highest = -1
        for filename in os.listdir(self.s_fp):
            if self.curr_filename().split('.')[0] in filename:  # if voc pertains to current file
                ind = int(filename.split('-')[-1].split('.')[0])
                if ind > highest:
                    highest = cpy(ind)

        self.d_ind = highest + 1

        self.ui.viewer.new_clip(path.join(self.d_fp, self.curr_filename()))
        self.logger.info('displaying file #{} ({})'.format(self.f_ind, self.curr_filename()))

    def prev(self):
        self.f_ind -= 1
        
        # figure out what next d_ind should be
        highest = -1
        for filename in os.listdir(self.s_fp):
            if self.curr_filename().split('.')[0] in filename:  # if voc pertains to current file
                ind = int(filename.split('-')[-1].split('.')[0])
                if ind > highest:
                    highest = cpy(ind)

        self.d_ind = highest + 1

        self.ui.viewer.new_clip(path.join(self.d_fp, self.curr_filename()))
        self.logger.info('displaying file #{} ({})'.format(self.f_ind, self.curr_filename()))

    # def exit(self):
    #     logger.info('not implemented')