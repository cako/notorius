#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" Window. """

import sys
import poppler
import popplerqt4
from PyQt4 import QtCore, QtGui, uic

class DocumentWidget(QtGui.QWidget):
    """ PlotWidget is the main component of MainWindow. """
    def __init__(self, parent = None):
        """ Initialize PlotWidget. """
        self.theparent = parent
        QtGui.QWidget.__init__(self, parent)
        self.click = False
        self.PdfImage = None

    def paintEvent(self, event):
        """ Sets up a painter and paint with the help of Helper. """
        painter = QtGui.QPainter()
        painter.begin(self)
        #painter.setRenderHint(QtGui.QPainter.Antialiasing)
        #white_brush = QtGui.QBrush(QtCore.Qt.white)
        #black_brush = QtGui.QBrush(QtCore.Qt.black)
        #red_palette = QtGui.QPalette(QtCore.Qt.red)
        #self.setAutoFillBackground(True)
        #self.setPalette(red_palette)
        if self.PdfImage:
            painter.drawImage(self.theparent.rect(), self.PdfImage)
        painter.end()

    def mousePressEvent(self, event):
        """ Repaints when mouse moves. """
        self.click = True
        self.update()

    def mouseReleaseEvent(self, event):
        """ Repaints when mouse moves. """
        self.click = False
        self.update()

    def mouseMoveEvent(self, event):
        """ Repaints when mouse moves. """
        self.click = False
        self.update()

    def loadDocument(self, document):
        self.document = popplerqt4.Poppler.Document.load(document)
        self.PdfPage =  self.document.page(0)
        self.PdfImage = self.PdfPage.renderToImage(300, 300, -1, -1, -1, -1,
                                                   self.PdfPage.Rotate0)
        self.update()

class ExitDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        print uic.loadUi('dialog.ui', self)

class MainWindow(QtGui.QMainWindow):
    """ Main Window Class """
    def __init__(self, parent=None):
        """ Initiaize Main Window """
        QtGui.QMainWindow.__init__(self, parent)
        uic.loadUi('window.ui', self)

        # Menu slots
        for (action, slot) in [ [self.actionOpen, self.slot_open] ,
                                [self.actionQuit, self.slot_quit] ]:
            self.connect(action, QtCore.SIGNAL("triggered()"), slot)

        self.documentWidget = DocumentWidget(self.scrollAreaWidgetContents)
        self.documentWidget.setObjectName("documentWidget")
        self.documentWidget.setGeometry(QtCore.QRect(0, 0, 916, 335))
        self.gridLayout_3.addWidget(self.documentWidget, 0, 0, 1, 1)

    def slot_open(self):
        """ Slot for openAction. """
        filename = unicode(QtGui.QFileDialog.getOpenFileName(self, 'Open file'))
        if filename:
            self.documentWidget.loadDocument(filename)
            self.statusBar().showMessage('Opened file to %s.' % filename)
    def slot_quit(self):
        quitDialog = ExitDialog()
        print 'this'
        quitDialog.show()
        quitDialog.open()
        print 'that'

