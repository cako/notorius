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
""" Main. """

import window
import sys
from PyQt4 import QtGui

class Application(QtGui.QApplication):
    """ Application Class """
    def __init__(self, argv):
        super(QtGui.QApplication, self).__init__(argv)
        docs = sys.argv[1:]
        self.windows = []
        if docs:
            for doc in docs:
                win = window.MainWindow(document=doc)
                win.ui.documentWidget.ImgLabel.set_clipboard_trigger.connect(
                                                    self.slot_set_clipboard)
                win.add_windows_trigger.connect(self.slot_add_windows)
                win.show()
                self.windows.append(win)
        else:
            win = window.MainWindow()
            win.ui.documentWidget.ImgLabel.set_clipboard_trigger.connect(
                                                self.slot_set_clipboard)
            win.add_windows_trigger.connect(self.slot_add_windows)
            win.show()
            self.windows = [win]

    def slot_set_clipboard(self, text):
        """ Slot to set th clipboard to selection. """
        clip = self.clipboard()
        clip.setText(unicode(text).strip())

    def slot_add_windows(self, windows):
        for win in windows:
            win.ui.documentWidget.ImgLabel.set_clipboard_trigger.connect(
                                                self.slot_set_clipboard)
            self.windows.append(win)

if __name__ == '__main__':
    APP = Application(sys.argv)
    sys.exit(APP.exec_())
