# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/offset_window.ui'
#
# Created: Sat Mar 24 12:24:59 2012
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(270, 91)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.cancelButton = QtGui.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(85, 40, 85, 28))
        self.cancelButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.cancelButton.setObjectName("cancelButton")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(14, 9, 188, 18))
        self.label.setObjectName("label")
        self.offsetSpinBox = QtGui.QSpinBox(self.centralwidget)
        self.offsetSpinBox.setGeometry(QtCore.QRect(205, 5, 60, 28))
        self.offsetSpinBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.offsetSpinBox.setMinimum(-16777215)
        self.offsetSpinBox.setMaximum(16777215)
        self.offsetSpinBox.setProperty("value", 1)
        self.offsetSpinBox.setObjectName("offsetSpinBox")
        self.okButton = QtGui.QPushButton(self.centralwidget)
        self.okButton.setGeometry(QtCore.QRect(180, 40, 85, 28))
        self.okButton.setObjectName("okButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 270, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Which page are you on now?", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("MainWindow", "Ok", None, QtGui.QApplication.UnicodeUTF8))

