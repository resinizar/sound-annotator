from PyQt5 import QtCore, QtGui, QtWidgets



class AlertYayNay(QtWidgets.QDialog):
	def __init__(self, parent, message, yay_fun, nay_fun):
		super().__init__(parent=parent)
		self.setWindowTitle('annotator')
		self.resize(176, 80)
		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

		verticalLayout = QtWidgets.QVBoxLayout(self)

		message = QtWidgets.QLabel(message, self)
		message.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		message.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
		verticalLayout.addWidget(message)

		buttonBox = QtWidgets.QDialogButtonBox(self)
		buttonBox.setOrientation(QtCore.Qt.Horizontal)
		buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Yes|QtWidgets.QDialogButtonBox.No)
		verticalLayout.addWidget(buttonBox)

		yay_button = buttonBox.button(QtWidgets.QDialogButtonBox.Yes)
		nay_button = buttonBox.button(QtWidgets.QDialogButtonBox.No)

		yay_button.clicked.connect(yay_fun)
		nay_button.clicked.connect(nay_fun)


class AlertOk(QtWidgets.QDialog):
	def __init__(self, parent, message, ok_fun):
		super().__init__(parent=parent)
		self.setWindowTitle('annotator')
		self.resize(176, 80)
		self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

		verticalLayout = QtWidgets.QVBoxLayout(self)

		message = QtWidgets.QLabel(message, self)
		message.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		message.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
		verticalLayout.addWidget(message)

		buttonBox = QtWidgets.QDialogButtonBox(self)
		buttonBox.setOrientation(QtCore.Qt.Horizontal)
		buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
		verticalLayout.addWidget(buttonBox)

		ok_button = buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
		ok_button.clicked.connect(ok_fun)
