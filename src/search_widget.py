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

""" Search Widget. """

import popplerqt4
from PyQt4 import QtCore, QtGui

class SearchWidget(QtGui.QWidget):
    """
    SearchWidget holds the search results.
    """

    hide_trigger = QtCore.pyqtSignal()
    change_page_trigger = QtCore.pyqtSignal(int)
    #show_trigger = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setObjectName("searchWidget")
        self.documentWidget = None

        self.searchLineEdit = QtGui.QLineEdit(self)
        self.searchLineEdit.setObjectName("searchLineEdit")

        self.searchTree = QtGui.QTreeWidget(self)
        self.searchTree.setObjectName("searchTree")
        self.searchTree.setHeaderLabels(["Search results"])

        self.connect(self.searchLineEdit, QtCore.SIGNAL("editingFinished()"),
                                          self.slot_search)
        self.connect(self.searchTree,
                     QtCore.SIGNAL("currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)"),
                     #QtCore.SIGNAL("itemActivated(QTreeWidgetItem*,int)"),
                     #QtCore.SIGNAL("itemChanged(QTreeWidgetItem*,int)"),
                     #QtCore.SIGNAL("itemClicked(QTreeWidgetItem*,int)"),
                     #QtCore.SIGNAL("itemCollapsed(QTreeWidgetItem*)"),
                     #QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem*,int)"),
                     #QtCore.SIGNAL("itemEntered(QTreeWidgetItem*,int)"),
                     #QtCore.SIGNAL("itemExpanded(QTreeWidgetItem*)"),
                     #QtCore.SIGNAL("itemPressed(QTreeWidgetItem*,int)"),
                     #QtCore.SIGNAL("itemSelectionChanged()"),
                     self.slot_changed_index)

        self.gridLayout = QtGui.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addWidget(self.searchLineEdit, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.searchTree)

    def keyPressEvent(self, event):
        if (event.matches(QtGui.QKeySequence.Find) or
                                        event.key() == QtCore.Qt.Key_Slash):
            self.searchLineEdit.selectAll()
            self.searchLineEdit.setFocus()
            #self.show_trigger.emit()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.hide_trigger.emit()

    def hideEvent(self, event):
        self.documentWidget.highlights = []
        self.documentWidget.update_image()

    def slot_changed_index(self, item, previtem=None):
        #print unicode(item.text(column))
        try:
            (rec, pg) = self.search_results[item]
            self.documentWidget.highlights = [[rec, pg]]
            if pg != self.documentWidget.page:
                self.change_page_trigger.emit(pg + 1 +
                                              self.documentWidget.offset)
            self.documentWidget.update_image()
            (x, y) = self.documentWidget.ImgLabel.pt2px(
                                                QtCore.QSizeF(rec.x(), rec.y()))
            self.documentWidget.parent.ensureVisible(x, y)
        except KeyError:
            pass


    def slot_search(self):
        if not self.searchLineEdit.hasFocus():
            return
        self.searchTree.clear()
        text = unicode(self.searchLineEdit.text())
        cur_page = self.documentWidget.page
        self.search_results = {}

        # self.search results has the following structure:
        # self.search_results[QTreeWidgetItem] = [[QRectF, page],
        #                                         [QRectF, page], etc]

        first = True
        first_item = None
        for page in ( range(cur_page, self.documentWidget.num_pages) +
                      range(0, cur_page) ):
            first_of_page = True
            loc = QtCore.QRectF()
            while self.documentWidget.Document.page(page).search(
                        text,
                        loc,
                        popplerqt4.Poppler.Page.NextResult,
                        popplerqt4.Poppler.Page.CaseInsensitive):

                if first_of_page:
                    page_item = QtGui.QTreeWidgetItem(
                        ['Page %d' % (page + self.documentWidget.offset + 1)])
                    self.searchTree.addTopLevelItem(page_item)
                    first_of_page = False

                # Widdened box to grab text 14% of the hole doc to each box
                wide = self.documentWidget.Document.page(page).pageSizeF()
                wide = wide.width() * 0.14
                loc_wide = QtCore.QRectF(loc.x() - wide, loc.y(),
                                         loc.width() + 2*wide, loc.height())
                display = self.documentWidget.Document.page(page).text(loc_wide)
                #display = '%f, %f, %f, %f' % (loc_wide.x(), loc_wide.y(),
                #loc_wide.width(), loc_wide.height())

                loc_item = QtGui.QTreeWidgetItem([display])
                #print 'Created ', loc_item
                page_item.addChild(loc_item)
                if first:
                    first_item = loc_item
                    first = False

                self.search_results[loc_item] = [QtCore.QRectF(
                                                   loc.x(), loc.y(),
                                                   loc.width(), loc.height()),
                                                 page]
        if first_item is not None:
            #self.searchTree.setCurrentItem(first_item)
            #self.slot_changed_index(first_item, 0)
            self.documentWidget.highlights = [ [rec, pg] for (rec, 
                                           pg) in self.search_results.values() ]
            self.documentWidget.update_image()
