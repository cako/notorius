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

""" Offset Window. """

from PyQt4 import QtCore, QtGui

from offset_window_ui import Ui_MainWindow
from constants import *

class OffsetWindow(QtGui.QMainWindow):
    """
    OffsetWindow is the window in which the user will input the offset.
    """
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.parent = parent
        self.offset = 0
        self.setStatusBar(None)
        self.ui.okButton.setDefault(True)

        self.connect(self.ui.cancelButton, QtCore.SIGNAL("clicked()"),
                     self.slot_cancel)

        self.connect(self.ui.okButton, QtCore.SIGNAL("clicked()"),
                     self.slot_ok)

    def slot_open(self, event):
        """
        Slot for opening the Preamble window. It repopulates the window with the
        saved preamble.
        """
        # On
        if event == 2:
            self.offset = self.parent.offset
            self.ui.offsetSpinBox.setValue(self.parent.ui.pageSpinBox.value() +
                                        self.offset)
            self.show()
        # Off
        else:
            old = self.offset
            page = self.parent.ui.pageSpinBox.value() - old
            self.offset = 0
            self.parent.ui.documentWidget.offset = 0
            self.parent.ui.maxPageLabel.setText("of %d" %
                            self.parent.ui.documentWidget.num_pages)
            self.parent.ui.pageSpinBox.setMaximum(
                                        self.parent.ui.pageSpinBox.maximum() - old)
            self.parent.ui.pageSpinBox.setMinimum(
                                        self.parent.ui.pageSpinBox.minimum() - old)
            self.parent.ui.pageSpinBox.setValue(page)

    def slot_cancel(self):
        """ Slot for cancel button. Closes window without saving. """
        self.parent.ui.offsetCheckBox.setChecked(False)
        self.close()

    def slot_ok(self):
        """
        Slot for ok button. It stores the value in the preamble QTextEdit
        window.
        """
        self.offset = self.ui.offsetSpinBox.value()-self.parent.ui.pageSpinBox.value()
        #print 'Offset %d.' % self.offset
        self.parent.ui.documentWidget.offset = self.offset
        self.parent.ui.maxPageLabel.setText("of %d" %
                        (self.parent.ui.documentWidget.num_pages + self.offset))
        self.parent.ui.pageSpinBox.setMaximum(self.parent.ui.pageSpinBox.maximum() +
                                           self.offset)
        #print 'Minimum %d' %  self.parent.ui.pageSpinBox.minimum()
        self.parent.ui.pageSpinBox.setMinimum(self.parent.ui.pageSpinBox.minimum() +
                                           self.offset)
        self.parent.ui.pageSpinBox.setValue(self.ui.offsetSpinBox.value())
        self.close()
