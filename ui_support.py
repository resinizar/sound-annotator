from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QPainter, QBrush, QPen, QImage, QPixmap
import logging
from os import path
import csv

from audio import AudioClip



class SpecViewer(QLabel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.c1 = (0, 0)
        self.c2 = (0, 0)
        self.curr_clip = None
        self.min_dur = 1

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
        x, y = self.c1
        w, h = self.c2[0] - self.c1[0], self.c2[1] - self.c1[1]
        painter.setPen(QPen(QtCore.Qt.yellow, 3, QtCore.Qt.SolidLine))
        painter.setBrush(QBrush(QtCore.Qt.yellow, QtCore.Qt.DiagCrossPattern))
        painter.drawRect(x, y, w, h)

    def new_clip(self, fp):
        # super(SpecViewer, self).paintEvent(e)
        self.curr_clip = AudioClip(fp)
        viewable_spec = (self.curr_clip.spec * 255).astype('uint8')
        h, w = viewable_spec.shape
        pixMap = QPixmap.fromImage(QImage(viewable_spec, w, h, int(viewable_spec.nbytes/h), QImage.Format_Grayscale8))
        self.setPixmap(pixMap)

    def save_selection(self):
        start = min(self.c1[0], self.c2[0])
        end = max(self.c1[0], self.c2[0])
        self.curr_clip.write_mini_clip('./support/temp.wav', start, end, self.min_dur)


class CSVTable(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.csv_fp = None  # set when table is loaded
        self.num_rows = -1  # so onItemChanged doesn't do unecessary work
        self.itemChanged.connect(self.onItemChanged)
        
    def load_table(self, csv_fp):
        self.csv_fp = csv_fp
        if not path.exists(csv_fp):
            with open(csv_fp, 'w') as csvfile:
                w = csv.writer(csvfile)
                w.writerow(['fp', 'tag'])

        with open(csv_fp, 'r') as csvfile:
            rows = list(csv.reader(csvfile))
            self.setRowCount(len(rows))
            self.setColumnCount(len(rows[0]))
            
            for i, row in enumerate(rows):
                for j, val in enumerate(row):
                    self.setCurrentCell(i, j)
                    self.setItem(i, j, QTableWidgetItem(val))
        self.num_rows = len(rows)

    def add_row(self, row):
        with open(self.csv_fp, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)

        pos = self.rowCount()
        self.insertRow(pos)
        self.setItem(pos, 0, QTableWidgetItem(row[0]))
        self.setItem(pos, 1, QTableWidgetItem(row[1]))
        self.num_rows += 1
        self.logger.info('added row {} to table.'.format(row))

    def onItemChanged(self, item):
        if item.row() <= self.num_rows:
            with open(self.csv_fp, 'r') as csvfile:
                rows = list(csv.reader(csvfile))
                old_val = rows[item.row()][item.column()]
                rows[item.row()][item.column()] = item.text()
            with open(self.csv_fp, 'w') as csvfile:
                w = csv.writer(csvfile)
                w.writerows(rows)
            self.logger.info('changed {} to {}'.format(old_val, item.text()))


