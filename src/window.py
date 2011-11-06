#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" Window. """

from __future__ import division
import platform
import popplerqt4
from PyQt4 import QtCore, QtGui, uic

PLATFORM = platform.system()
if PLATFORM == 'Linux':
    import subprocess
    proc1 = subprocess.Popen(['xdpyinfo'], stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(["grep", "dots"], stdin=proc1.stdout,
                                               stdout=subprocess.PIPE)
    output = proc2.communicate()[0]
    res = output.strip().split()[1]
    (DPI_X, DPI_Y) = [int(DPI) for DPI in res.split('x')]
else:
    DPI_X = DPI_X = 96

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
        self.ImgLabel = QtGui.QLabel()
        self.ImgPixmap = QtGui.QPixmap()
        # -1 fits height, -2 fits width
        self.scale = 1

    #def paintEvent(self, event):
        #""" Sets up a painter and paint with the help of Helper. """
        #painter = QtGui.QPainter()
        #painter.begin(self)
        ##painter.setRenderHint(QtGui.QPainter.Antialiasing)
        ##painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
        ##painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        #painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        #if self.Image:
            #page_qsizef = self.CurrentPage.pageSizeF()
            #ratio = page_qsizef.height()/page_qsizef.width()
            #draw_image_rect = self.theparent.rect()
            #if self.scale == -1:
                #draw_image_rect.setWidth(draw_image_rect.height()/ratio)
                #painter.drawImage(draw_image_rect, self.Image)
            #elif self.scale == -2:
                #draw_image_rect.setHeight(draw_image_rect.width()*ratio)
                #painter.drawImage(draw_image_rect, self.Image)
            #else:
                #print 'Not yet implemented!'
        #painter.end()

    def set_scale(self, event):
        self.scale = float(event)
        self.Image = self.CurrentPage.renderToImage(DPI_X*self.scale,
                                                    DPI_Y*self.scale)
        self.ImgLabel.setPixmap(self.ImgPixmap.fromImage(self.Image))
        padding = (self.theparent.size().width() - self.Image.size().width())/2
        self.theparent.move(padding, 0)

    def load_document(self, document):
        self.Document = popplerqt4.Poppler.Document.load(document)
        self.Document.setRenderHint(self.Document.Antialiasing)
        self.Document.setRenderHint(self.Document.TextAntialiasing)
        self.Document.setRenderHint(self.Document.TextHinting)
        self.CurrentPage =  self.Document.page(0)
        self.num_pages = self.Document.numPages()
        self.set_scale(1)

    def change_page(self, event):
        if self.Document:
            self.CurrentPage = self.Document.page( (event-1)%self.num_pages )
            self.Image = self.CurrentPage.renderToImage(DPI_X*self.scale,
                                                        DPI_Y*self.scale)
            self.ImgLabel.setPixmap(self.ImgPixmap.fromImage(self.Image))

    def fit_to_width_or_height(self, event):
        page_size =  self.CurrentPage.pageSizeF()
        if event == 1:
            width = self.theparent.rect().width() - 18
            self.set_scale(72.0*width/(DPI_X * page_size.width()))
        else:
            height = self.theparent.rect().height()
            self.set_scale(72.0*height/(DPI_Y * page_size.height()))

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

        # Scroll Widget
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        # PDF viewer widget
        self.documentWidget = DocumentWidget(self.scrollArea)
        self.documentWidget.setObjectName("documentWidget")
        self.documentWidget.setGeometry(QtCore.QRect(0, 0, 916, 335))
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.documentWidget.ImgLabel)

        # Connections
        self.connect(self.previousPageButton, QtCore.SIGNAL("clicked()"),
                     self.slot_prev_pageSpinBox)
        self.connect(self.nextPageButton, QtCore.SIGNAL("clicked()"),
                     self.slot_next_pageSpinBox)
        self.connect(self.pageSpinBox, QtCore.SIGNAL("valueChanged(int)"),
                     self.documentWidget.change_page)
        self.connect(self.scaleSpinBox, QtCore.SIGNAL("valueChanged(QString)"),
                    self.documentWidget.set_scale)
        self.connect(self.scaleComboBox,
                     QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.slot_scaleComboBox)

    def slot_open(self):
        """ Slot for actionQuit. """
        filename = unicode(QtGui.QFileDialog.getOpenFileName(self, 'Open file'))
        if filename:
            self.documentWidget.load_document(filename)
            self.pageSpinBox.setValue(1)
            self.pageSpinBox.setMinimum(-self.documentWidget.num_pages + 1)
            self.pageSpinBox.setMaximum(self.documentWidget.num_pages)
            self.scaleComboBox.setCurrentIndex(0)
            self.maxPageLabel.setText("/ "+str(self.documentWidget.num_pages))
            self.statusBar().showMessage('Opened file to %s.' % filename)

    def slot_quit(self):
        """ Slot for actionQuit. """
        self.close()

    def slot_prev_pageSpinBox(self):
        self.pageSpinBox.setValue(self.pageSpinBox.value() - 1)

    def slot_next_pageSpinBox(self):
        self.pageSpinBox.setValue(self.pageSpinBox.value() + 1)

    def slot_scaleComboBox(self, event):
        if event == 0:
            self.scaleSpinBox.setEnabled(True)
            self.documentWidget.set_scale(self.scaleSpinBox.value())
        else:
            self.scaleSpinBox.setEnabled(False)
            self.documentWidget.fit_to_width_or_height(event)
