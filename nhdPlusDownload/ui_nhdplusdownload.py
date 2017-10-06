# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Program Files (x86)\EPA H2O\apps\qgis\python\plugins\nhdPlusDownload\ui_nhdplusdownload.ui'
#
# Created: Thu Oct 05 11:16:15 2017
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_nhdPlusDownload(object):
    def setupUi(self, nhdPlusDownload):
        nhdPlusDownload.setObjectName(_fromUtf8("nhdPlusDownload"))
        nhdPlusDownload.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(nhdPlusDownload)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label_2 = QtGui.QLabel(nhdPlusDownload)
        self.label_2.setGeometry(QtCore.QRect(50, 150, 187, 78))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.comboBox1 = QtGui.QComboBox(nhdPlusDownload)
        self.comboBox1.setGeometry(QtCore.QRect(190, 180, 186, 20))
        self.comboBox1.setObjectName(_fromUtf8("comboBox1"))

        self.retranslateUi(nhdPlusDownload)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), nhdPlusDownload.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), nhdPlusDownload.reject)
        QtCore.QMetaObject.connectSlotsByName(nhdPlusDownload)

    def retranslateUi(self, nhdPlusDownload):
        nhdPlusDownload.setWindowTitle(QtGui.QApplication.translate("nhdPlusDownload", "nhdPlusDownload", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("nhdPlusDownload", "Select a layer", None, QtGui.QApplication.UnicodeUTF8))

