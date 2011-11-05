#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" Main. """

import sys
from PyQt4 import QtGui
import window

if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    WINDOW = window.MainWindow()
    WINDOW.show()
    sys.exit(APP.exec_())
