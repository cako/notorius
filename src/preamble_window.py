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

""" PreambleWindow. """

import os
from PyQt4 import QtCore, QtGui

from preamble_window_ui import Ui_MainWindow
from constants import *


class PreambleWindow(QtGui.QMainWindow):
    """
    PreambleWindow allows for editing of the preamble.
    """
    def __init__(self, parent = None, preamble = PREAMBLE):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.parent = parent
        self.preamble = unicode(preamble)
        self.setStatusBar(None)

        self.connect(self.ui.cancelButton, QtCore.SIGNAL("clicked()"),
                     self.slot_cancel)

        self.connect(self.ui.saveButton, QtCore.SIGNAL("clicked()"),
                     self.slot_save)

    def slot_open(self):
        """
        Slot for opening PreambleWindow. It repopulates the window with the
        saved preamble.
        """
        self.preamble = self.parent.preamble
        self.ui.preambleTextEdit.setText(self.preamble)
        self.show()

    def slot_cancel(self):
        """ Slot for cancel button. Closes window without saving. """
        self.close()

    def slot_save(self):
        """
        Slot for save button. It stores the value in the preamble QTextEdit
        window.
        """
        self.preamble = unicode(self.ui.preambleTextEdit.toPlainText())
        self.parent.preamble = self.preamble
        self.close()
