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
        self.Document = None
        self.CurrentPage = None
        self.Image = None
        self.num_pages = None

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
        if self.Image:
            page_qsizef = self.CurrentPage.pageSizeF()
            ratio = page_qsizef.height()/page_qsizef.width()
            draw_image_rect = self.theparent.rect()
            # This next line guarantees the Image is not distorted
            draw_image_rect.setHeight(draw_image_rect.width()*ratio)
            painter.drawImage(draw_image_rect, self.Image)
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

    def load_document(self, document):
        self.Document = popplerqt4.Poppler.Document.load(document)
        self.CurrentPage =  self.Document.page(0)
        self.Image = self.CurrentPage.renderToImage(300, 300, -1, -1, -1, -1,
                                                   self.CurrentPage.Rotate0)
        self.num_pages = self.Document.numPages()
        self.update()

    def change_page(self, event):
        self.CurrentPage = self.Document.page((event - 1)%self.num_pages)
        self.Image = self.CurrentPage.renderToImage(300, 300, -1, -1, -1, -1,
                                                   self.CurrentPage.Rotate0)
        self.update()

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

        # PDF viewer widget
        self.documentWidget = DocumentWidget(self.scrollAreaWidgetContents)
        self.documentWidget.setObjectName("documentWidget")
        self.documentWidget.setGeometry(QtCore.QRect(0, 0, 916, 335))
        self.gridLayout_3.addWidget(self.documentWidget, 0, 0, 1, 1)

        # Page spinbox widget
        #self.pageSpinBox.setMinimum(1)

        # Connections
        self.connect(self.pageSpinBox, QtCore.SIGNAL("valueChanged(int)"),
                     self.documentWidget.change_page)

    def slot_open(self):
        """ Slot for actionQuit. """
        filename = unicode(QtGui.QFileDialog.getOpenFileName(self, 'Open file'))
        if filename:
            self.documentWidget.load_document(filename)
            self.pageSpinBox.setValue(1)
            self.pageSpinBox.setMinimum(-self.documentWidget.num_pages + 1)
            self.pageSpinBox.setMaximum(self.documentWidget.num_pages)
            self.statusBar().showMessage('Opened file to %s.' % filename)

    def slot_quit(self):
        """ Slot for actionQuit. """
        self.close()
