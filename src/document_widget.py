#!/usr/bin/python
# -*- coding: UTF-8 -*-
#==============================================================================#
#                                                                              #
# Copyright 2011 Carlos Alberto da Costa Filho                                 #
#                                                                              #
# This file is part of Notorius.                                               #
#                                                                              #
# Notorius is free software: you can redistribute it and/or modify             #
# it under the terms of the GNU General Public License as published by         #
# the Free Software Foundation, either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
# Notorius is distributed in the hope that it will be useful,                  #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                 #
# GNU General Public License for more details.                                 #
#                                                                              #
# You should have received a copy of the GNU General Public License            #
# along with this program. If not, see <http://www.gnu.org/licenses/>.         #
#                                                                              #
#==============================================================================#

""" Document Widget. """

import popplerqt4
from PyQt4 import QtCore, QtGui

from image_label import ImageLabel
from constants import *

class DocumentWidget(QtGui.QWidget):
    """
    DocumentWidget is the main component of MainWindow. It displays the PDF.
    """

    def __init__(self, parent = None):
        """ Initialize DocumentWidget. """
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.Document = None
        self.CurrentPage = None
        self.Image = None
        self.highlights = None
        self.num_pages = 0
        self.page = 0
        self.offset = 0
        self.ImgLabel = ImageLabel(self)
        self.ImgLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ImgPixmap = QtGui.QPixmap()
        self.scale = 1

    def set_scale(self, event):
        """ Sets the scale with which the document will be redered. """
        self.scale = event
        if self.Document is not None:
            self.update_image()

    def load_document(self, document):
        """
        Load the document. Sets current page to the first page and the scale to 1.
        """
        self.Document = popplerqt4.Poppler.Document.load(document)
        self.Document.setRenderHint(self.Document.Antialiasing)
        self.Document.setRenderHint(self.Document.TextAntialiasing)
        self.Document.setRenderHint(self.Document.TextHinting)
        self.CurrentPage =  self.Document.page(self.page)
        self.num_pages = self.Document.numPages()
        self.set_scale(1)

    def change_page(self, event):
        """ Changes the page. """
        if self.Document is not None:
            self.page = ((event - self.offset -1) % self.num_pages)
            #print 'Page %d.' % self.page
            self.CurrentPage = self.Document.page(self.page)
            self.update_image()
            self.parent.ensureVisible(0, 0)

    def fit_to_width_or_height(self, event):
        """
        Changes the scale in such a way that it fits the width or the height of
        the window.
        width: event = 1
        height: event = 2
        """
        if self.Document is not None:
            page_size =  self.CurrentPage.pageSizeF()
            if event == 1:
                # 18 is window border, 4 is shadow
                width = self.parent.rect().width() - 18 - 6
                self.scale = 72.0*width/(DPI_X * page_size.width())
            else:
                # 2 is window border, 4 is shadow
                height = self.parent.rect().height() - 2 - 6
                self.scale = 72.0*height/(DPI_Y * page_size.height())
            self.update_image()

    def update_image(self):
        """ Updates Image and ImgLabel. """
        if self.Document is not None:
            self.Image = self.CurrentPage.renderToImage(DPI_X*self.scale,
                                                        DPI_Y*self.scale)
            self.ImgLabel.setPixmap(self.ImgPixmap.fromImage(self.Image))

            background = QtGui.QImage(QtCore.QSize(self.Image.width() + 6,
                                                   self.Image.height() + 6),
                                      self.Image.format())
            painter = QtGui.QPainter()
            painter.begin(background)
            painter.fillRect(QtCore.QRect(0, 0, background.width(),
                                                background.height()),
                             QtGui.QColor(60, 60, 60))
            painter.drawImage(1, 1, self.Image)
            painter.fillRect(QtCore.QRect(0, self.Image.height() + 2, 6, 4),
                             QtGui.QColor(203, 201, 200))
            painter.fillRect(QtCore.QRect(self.Image.width() + 2, 0, 4, 6),
                             QtGui.QColor(203, 201, 200))

            if self.highlights is not None:
                for rect in self.highlights:
                    (x, y) = self.ImgLabel.pt2px(
                                            QtCore.QSizeF(rect.x(), rect.y()))
                    (w, h) = self.ImgLabel.pt2px(QtCore.QSizeF(rect.width(),
                                                               rect.height()))
                    painter.fillRect(QtCore.QRect(x + 1, y + 1, w, h),
                                     QtGui.QColor(255, 255, 0, 100))

            painter.end()

            for note in self.ImgLabel.notes.values():
                if note.page == self.page:
                    #print note.uid
                    x = note.pos.x()
                    x *= self.scale * DPI_X / 72.0

                    y = note.pos.y()
                    y *= self.scale * DPI_Y / 72.0

                    #print x,y
                    painter = QtGui.QPainter()
                    painter.begin(background)
                    painter.drawImage(x, y, self.ImgLabel.noteImage)
                    painter.end()

            self.ImgLabel.setPixmap(QtGui.QPixmap.fromImage(background))
