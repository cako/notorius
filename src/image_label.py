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

""" Image Label. """

import datetime
from PyQt4 import QtCore, QtGui, QtXml, uic

from note import Note
from constants import *
from icons import *

class ImageLabel(QtGui.QLabel):
    """
    The ImageLabel class holds PDF QPixmap to be displayed in DocumentWidget.
    """

    remove_trigger = QtCore.pyqtSignal()
    toggle_source_trigger = QtCore.pyqtSignal()
    set_clipboard_trigger = QtCore.pyqtSignal(QtCore.QString)
    change_scale_trigger = QtCore.pyqtSignal(float)

    def __init__(self, parent = None):
        super(ImageLabel, self).__init__()
        self.parent = parent
        self.preamble = PREAMBLE
        self.note_pos = QtCore.QPointF()
        self.note_icon_pos = QtCore.QPoint()
        self.current_uid = 0
        self.closest_id = 0
        self.notes = {}
        self.move = False
        self.drag = False
        self.control = False
        self.noteImage = QtGui.QImage(':img/note22.png')
        self.rubber_band = QtGui.QRubberBand( QtGui.QRubberBand.Rectangle, self)
        self.drag_position = QtCore.QPoint()

        self.setMouseTracking(True)
        self.setAcceptDrops(True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self,
                   QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"),
                    self.contextMenu)
        self.add_menu = QtGui.QMenu()
        self.addNoteAction = QtGui.QAction(self)
        self.addNoteAction.setText("Add annotation")
        self.connect(self.addNoteAction, QtCore.SIGNAL("triggered()"),
                     self.slot_add_note)
        self.add_menu.addAction(self.addNoteAction)

        self.change_menu = QtGui.QMenu()
        self.editNoteAction = QtGui.QAction(self)
        self.editNoteAction.setText("Edit annotation")
        self.connect(self.editNoteAction, QtCore.SIGNAL("triggered()"),
                     self.slot_edit_note)
        self.change_menu.addAction(self.editNoteAction)
        self.moveNoteAction = QtGui.QAction(self)
        self.moveNoteAction.setText("Move annotation")
        self.connect(self.moveNoteAction, QtCore.SIGNAL("triggered()"),
                     self.slot_move_note)
        self.change_menu.addAction(self.moveNoteAction)
        self.removeNoteAction = QtGui.QAction(self)
        self.removeNoteAction.setText("Remove annotation")
        self.connect(self.removeNoteAction, QtCore.SIGNAL("triggered()"),
                     self.slot_remove_note)
        self.change_menu.addAction(self.removeNoteAction)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            files = []
            for url in event.mimeData().urls():
                files.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), files)
        else:
            event.ignore()

    def keyPressEvent(self, event):
        if ( event.key() == QtCore.Qt.Key_Plus or
             event.key() == QtCore.Qt.Key_Equal and
             event.modifiers() == QtCore.Qt.ControlModifier):
            self.change_scale_trigger.emit(self.parent.scale + 0.25)
        elif ( event.key() == QtCore.Qt.Key_Minus and
               event.modifiers() == QtCore.Qt.ControlModifier):
            self.change_scale_trigger.emit(self.parent.scale - 0.25)
        elif ( event.key() == QtCore.Qt.Key_0 and
               event.modifiers() == QtCore.Qt.ControlModifier):
            self.change_scale_trigger.emit(1.0)

    def mouseMoveEvent(self,  event):
        """
        Event handling mouse movement.
        """
        if self.parent.Document is None:
            return
        try:
            note = self.notes[self.closest_id]
            has_note = True
        except KeyError:
            has_note = False
        if has_note:
            width = self.pt2px(self.parent.CurrentPage.pageSizeF())[0]
            x_offset = (self.rect().width() - width)/2.0
            if self.drag:
                #print 'Drag note %d' %note.uid
                note.pos = self.px2pt(event.x() - x_offset, event.y())
                self.parent.update_image()
            else:
                if (event.x() >= x_offset) and (event.x() <= width + x_offset):
                    try:
                        x1 = self.drag_position.x()
                        y1 = self.drag_position.y()
                        x2 = event.x()
                        y2 = event.y()
                        if x1 > x2:
                            x1, x2 = x2, x1
                        if y1 > y2:
                            y1, y2 = y2, y1
                        #print QtCore.QRect(QtCore.QPoint(x1, y1), QtCore.QPoint(x2, y2))
                        self.rubber_band.setGeometry(QtCore.QRect(QtCore.QPoint(x1, y1),
                                                                  QtCore.QPoint(x2, y2)))
                    except IOError:
                        print 'IOError in rubberBand.setGeometry try.'
                        pass
                    if self.find_closest(event.x(), event.y()):
                        note.generate_source()
                        img_path =  note.filename.rstrip('tex') + 'border.png'
                        QtGui.QToolTip.showText(event.globalPos(),
                                                'Note %d: <br /> <img src="%s">'
                                                % (note.uid, img_path),
                                                self)

    def mousePressEvent(self, event):
        if self.parent.Document is None:
            return
        if event.button() == 1: # Left click
            width = self.pt2px(self.parent.CurrentPage.pageSizeF())[0]
            x_offset = (self.rect().width() - width)/2.0
            if (event.x() >= x_offset) and (event.x() <= width + x_offset):
                self.drag_position = QtCore.QPoint(event.pos())
                self.rubber_band = QtGui.QRubberBand(
                                                QtGui.QRubberBand.Rectangle, self)
                self.rubber_band.setGeometry(QtCore.QRect(
                                                self.drag_position, QtCore.QSize()))
                self.rubber_band.show()
                if self.find_closest(event.x(), event.y()):
                    self.drag = True
                else:
                    self.drag = False
            else:
                self.drag = False
        else:
            self.drag = False

    def mouseReleaseEvent(self, event):
        if self.parent.Document is None:
            return
        self.drag = False
        width = self.pt2px(self.parent.CurrentPage.pageSizeF())[0]
        x_offset = (self.rect().width() - width)/2.0
        if self.move:
            note = self.notes[self.closest_id]
            note.pos = self.px2pt(event.x() - x_offset, event.y())
            note.mdate = datetime.datetime.now()
            self.parent.update_image()
            self.move = False
        if not self.rubber_band.size().isEmpty():
            x_px = self.rubber_band.x() - x_offset
            y_px = self.rubber_band.y()
            width_px =  self.rubber_band.width()
            height_px =  self.rubber_band.height()
            pos = self.px2pt(x_px, y_px)
            x_pt = pos.x()
            y_pt = pos.y()
            size = self.px2pt(width_px, height_px)
            width_pt = size.x()
            height_pt = size.y()
            rect = QtCore.QRectF(x_pt, y_pt, width_pt, height_pt)
            #print rect
            text = self.parent.CurrentPage.text(rect)
            if text:
                self.set_clipboard_trigger.emit(text)
        self.rubber_band.hide()


    def mouseDoubleClickEvent(self, event):
        if self.parent.Document is None:
            return
        try:
            self.notes[self.closest_id]
            has_note = True
        except KeyError:
            has_note = False
        width = self.pt2px(self.parent.CurrentPage.pageSizeF())[0]
        x_offset = (self.rect().width() - width)/2.0
        if has_note and not self.drag:
            if (event.x() >= x_offset) and (event.x() <= width + x_offset):
                if self.find_closest(event.x(), event.y()):
                    self.toggle_source_trigger.emit()

    def contextMenu(self, pos):
        """
        Event handling right-click contextMenu
        """
        if self.parent.Document is None:
            return
        #print self.notes.values()
        width = self.pt2px(self.parent.CurrentPage.pageSizeF())[0]
        x_offset = (self.rect().width() - width)/2.0
        if (pos.x() >= x_offset) and (pos.x() <= width + x_offset):
            if self.find_closest(pos.x(), pos.y()):
                self.change_menu.exec_(self.mapToGlobal(pos))
            else:
                self.note_pos = self.px2pt(pos.x() - x_offset, pos.y())
                self.note_icon_pos = QtCore.QPoint(pos.x() - x_offset, pos.y())
                #print 'Note position: ', self.note_pos
                #print 'Mouse position', pos
                self.add_menu.exec_(self.mapToGlobal(pos))

    def find_closest(self, x, y):
        """
        Finds closest note to coordinates (x, y).
        Returns True if successful, False otherwise.
        """
        found_it = False
        width = self.pt2px(self.parent.CurrentPage.pageSizeF())[0]
        x_offset = (self.rect().width() - width)/2.0
        if len(self.notes) != 0:
            for note in self.notes.values():
                n_x = (note.pos.x() * self.parent.scale * DPI_X/72.0) + 11
                n_y = (note.pos.y() * self.parent.scale * DPI_X/72.0) + 11
                dx = abs(x - x_offset - n_x)
                dy = abs(y - n_y)
                if dx <= 11 and dy <= 11:
                    self.closest_id = note.uid
                    found_it = True
                    break
        return found_it

    def slot_add_note(self):
        """
        Slot to add a note. Creates new uid, generates note and displays the
        icon.
        """

        try:
            uid = max(self.notes.keys()) + 1
        except ValueError:
            uid = 0
        self.current_uid = uid
        self.notes[uid] = Note('New note', self.preamble, COMPILER,
                                   self.parent.page, self.note_pos,
                                   uid)
        self.parent.update_image()

    def slot_edit_note(self):
        """
        Slot to edit note. Update the current_uid with the one closest to the
        click.
        """
        #print "Editing note %d\n" % self.closest_id
        self.current_uid = self.closest_id
        self.notes[self.current_uid].mdate = datetime.datetime.now()

    def slot_move_note(self):
        """
        Slot to move note.
        """
        self.move = True

    def slot_remove_note(self):
        """
        Slot to remove note. Update the current_uid with the one closest to the
        click. Also emits remove_trigger sinal.
        """
        #print 'Remove note %d' % self.closest_id
        self.remove_trigger.emit()

    def pt2px(self, qsize):
        """
        Convert from pt to px.
        """
        width = qsize.width()
        width *= self.parent.scale * DPI_X / 72.0

        height = qsize.height()
        height *= self.parent.scale * DPI_Y / 72.0

        return (width, height)

    def px2pt(self, x, y):
        """
        Convert from px to pt.
        """
        width = 72.0 * x/(DPI_X * self.parent.scale)

        height = 72.0 * y/(DPI_Y * self.parent.scale)

        return QtCore.QPointF(width, height)

