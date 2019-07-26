from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import logging
from os import path
import csv



class CSVTable(QTableWidget):

    show_msg = QtCore.pyqtSignal(logging.Logger, str)

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.csv_fp = None  # set when table is loaded
        self.num_rows = -1  # so onItemChanged doesn't do unecessary work
        self.itemChanged.connect(self.onItemChanged)
        
    def load_table(self, csv_fp):
        self.logger.info('loading \'{}\''.format(csv_fp))
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
        if item.row() < self.num_rows:
            with open(self.csv_fp, 'r') as csvfile:
                rows = list(csv.reader(csvfile))
                old_val = rows[item.row()][item.column()]
                rows[item.row()][item.column()] = item.text()
            with open(self.csv_fp, 'w') as csvfile:
                w = csv.writer(csvfile)
                w.writerows(rows)
            msg = 'changed {} to {} in csv file in row {}'.format(old_val, item.text(), item.row() + 1)
            self.show_msg.emit(self.logger, msg)


