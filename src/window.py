#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" Window. """

import sys
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
        # -1 fits height, -2 fits width
        self.scale = -1

    def paintEvent(self, event):
        """ Sets up a painter and paint with the help of Helper. """
        painter = QtGui.QPainter()
        painter.begin(self)
        #painter.setRenderHint(QtGui.QPainter.Antialiasing)
        #painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
        #painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        if self.Image:
            page_qsizef = self.CurrentPage.pageSizeF()
            ratio = page_qsizef.height()/page_qsizef.width()
            draw_image_rect = self.theparent.rect()
            if self.scale == -1:
                draw_image_rect.setWidth(draw_image_rect.height()/ratio)
                painter.drawImage(draw_image_rect, self.Image)
            elif self.scale == -2:
                draw_image_rect.setHeight(draw_image_rect.width()*ratio)
                painter.drawImage(draw_image_rect, self.Image)
            else:
                print 'Not yet implemented!'
        print 'paint current page'
        painter.end()

    def set_scale(self, event):
        self.scale = float(event)
        self.update()

    def load_document(self, document):
        self.Document = popplerqt4.Poppler.Document.load(document)
        self.CurrentPage =  self.Document.page(0)
        self.Image = self.CurrentPage.renderToImage(300, 300, -1, -1, -1, -1,
                                                    self.CurrentPage.Rotate0)
        self.num_pages = self.Document.numPages()
        self.update()

    def change_page(self, event):
        print event
        event = int(event)
        self.CurrentPage = self.Document.page( (event-1)%self.num_pages )
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

        self.pageSpinBox.setValue(1)
        # Connections
        self.connect(self.pageSpinBox, QtCore.SIGNAL("valueChanged(QString)"),
                     self.documentWidget.change_page)
        self.connect(self.scaleSpinBox, QtCore.SIGNAL("valueChanged(QString)"),
                    self.documentWidget.set_scale)

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
