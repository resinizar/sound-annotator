from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QBrush, QPen, QImage, QPixmap, QColor
import logging
from math import ceil

from audio_clip import AudioClip



class SpecViewer(QLabel):

    show_new_file_info = QtCore.pyqtSignal(logging.Logger)
    
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.c1 = (0, 0)
        self.c2 = (0, 0)
        self.curr_clip = None
        self.min_dur = None
        self.pen_weight = 1
        self.h = self.pen_weight 

    def mousePressEvent(self, e):
        self.logger.debug('mouse pressed at ({}, {})'.format(e.x(), e.y()))
        self.c1 = e.x(), e.y()
        self.c2 = e.x(), e.y()
        self.update()

    def mouseMoveEvent(self, e):
        self.c2 = e.x(), e.y()
        self.update()

    def mouseReleaseEvent(self, e):
        self.logger.debug('mouse released at ({}, {})'.format(e.x(), e.y()))
        self.c2 = e.x(), e.y()
        self.update()
        self.save_selection()

    def paintEvent(self, e):
        super(SpecViewer, self).paintEvent(e)
        painter = QPainter(self)
        x, _ = self.c1
        w = self.c2[0] - self.c1[0]
        painter.setPen(QPen(QColor(178, 217, 181), self.pen_weight, QtCore.Qt.SolidLine))
        painter.setBrush(QBrush(QColor(178, 217, 181), QtCore.Qt.Dense7Pattern))
        painter.drawRect(x, self.pen_weight, w, self.h - self.pen_weight)

    def new_clip(self, fp):
        self.c1 = (0, 0)
        self.c2 = (0, 0)
        self.update()
        self.curr_clip = AudioClip(fp)
        viewable_spec = (self.curr_clip.spec * 255).astype('uint8')
        self.h, w = viewable_spec.shape
        self.setPixmap(QPixmap.fromImage(QImage(viewable_spec, w, self.h, 
            int(viewable_spec.nbytes / self.h), QImage.Format_Grayscale8)))
        self.show_new_file_info.emit(self.logger)

    def save_selection(self):
        start_spec = min(self.c1[0], self.c2[0])  # get start and end in spectrogram space
        end_spec = max(self.c1[0], self.c2[0])

        _, spec_w = self.curr_clip.spec.shape  # get min dur in spec space
        min_dur_spec = self.min_dur * self.curr_clip.sr * spec_w / len(self.curr_clip.clip)

        dur_spec = end_spec - start_spec
        if dur_spec < min_dur_spec:
            pad_len = ceil((min_dur_spec - dur_spec) / 2)
            start_spec = max(start_spec - pad_len, 0)
            end_spec = min(end_spec + pad_len, spec_w)

            self.c1 = (start_spec, self.c1[1])
            self.c2 = (end_spec, self.c2[1])
            self.update()

        self.curr_clip.write_mini_clip('./temp.wav', start_spec, end_spec)
