# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/newsession.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(445, 256)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.csvFileName = QtWidgets.QLineEdit(Dialog)
        self.csvFileName.setMinimumSize(QtCore.QSize(300, 0))
        self.csvFileName.setMaximumSize(QtCore.QSize(400, 16777215))
        self.csvFileName.setPlaceholderText("")
        self.csvFileName.setObjectName("csvFileName")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.csvFileName)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label)
        self.minDur = QtWidgets.QLineEdit(Dialog)
        self.minDur.setMinimumSize(QtCore.QSize(300, 0))
        self.minDur.setMaximumSize(QtCore.QSize(400, 16777215))
        self.minDur.setObjectName("minDur")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.minDur)
        self.dataFolderButton = QtWidgets.QPushButton(Dialog)
        self.dataFolderButton.setMinimumSize(QtCore.QSize(80, 0))
        self.dataFolderButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.dataFolderButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.dataFolderButton.setObjectName("dataFolderButton")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.dataFolderButton)
        self.saveFolderButton = QtWidgets.QPushButton(Dialog)
        self.saveFolderButton.setMinimumSize(QtCore.QSize(80, 0))
        self.saveFolderButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.saveFolderButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.saveFolderButton.setObjectName("saveFolderButton")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.saveFolderButton)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_1 = QtWidgets.QLabel(Dialog)
        self.label_1.setObjectName("label_1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_1)
        self.dataFolder = QtWidgets.QLineEdit(Dialog)
        self.dataFolder.setMinimumSize(QtCore.QSize(300, 0))
        self.dataFolder.setMaximumSize(QtCore.QSize(400, 16777215))
        self.dataFolder.setObjectName("dataFolder")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.dataFolder)
        self.saveFolder = QtWidgets.QLineEdit(Dialog)
        self.saveFolder.setMinimumSize(QtCore.QSize(300, 0))
        self.saveFolder.setMaximumSize(QtCore.QSize(400, 16777215))
        self.saveFolder.setObjectName("saveFolder")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.saveFolder)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "annotator"))
        self.label_3.setText(_translate("Dialog", "CSV File Name"))
        self.csvFileName.setText(_translate("Dialog", "data.csv"))
        self.label.setText(_translate("Dialog", "Minimum Duration"))
        self.minDur.setText(_translate("Dialog", "1.0"))
        self.dataFolderButton.setText(_translate("Dialog", "Choose..."))
        self.saveFolderButton.setText(_translate("Dialog", "Choose..."))
        self.label_2.setText(_translate("Dialog", "Save Path:"))
        self.label_1.setText(_translate("Dialog", "Data Path:"))
