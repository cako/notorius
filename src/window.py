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

""" Window. """

import os
import subprocess
import threading
import popplerqt4
from PyQt4 import QtCore, QtGui, uic
from platform import system as systemplat
from time import sleep
from random import randint

PREAMBLE = '''\documentclass[12pt,a4paper]{article}
\usepackage[utf8x]{inputenc}
'''

WELCOME = u'''\\begin{center}
Hello and welcome to notorius!\\\\
It's got $\LaTeX$ and $\int$\\vspace{-1mm}$\hbar í \\tau$!
\end{center}'''

PLATFORM = systemplat()
if PLATFORM == 'Linux':
    try:
        PROC1 = subprocess.Popen(["xdpyinfo"], stdout=subprocess.PIPE)
        PROC2 = subprocess.Popen(["grep", "dots"], stdin=PROC1.stdout,
                                                   stdout=subprocess.PIPE)
        OUT = PROC2.communicate()[0]
        PROC1.stdout.close()
        PROC2.stdout.close()
        DPI = OUT.strip().split()[1]
        (DPI_X, DPI_Y) = [ int(dpi) for dpi in DPI.split('x') ]
    except OSError:
        DPI_X = DPI_X = 96
else:
    DPI_X = DPI_X = 96

if PLATFORM == 'Windows':
    DIR = os.path.dirname(__file__)+"\\"
else:
    DIR = os.path.dirname(__file__)+"/"

COMPILER = 'pdflatex'
try:
    PROC = subprocess.Popen([COMPILER, "--version"], stdout=subprocess.PIPE)
    PROC.stdout.close()
except OSError:
    COMPILER = 'latex'

class PreambleWindow(QtGui.QMainWindow):
    """
    PackageDialog allows for editing of packages
    """
    def __init__(self, parent = None, preamble = PREAMBLE):
        QtGui.QMainWindow.__init__(self, parent)
        uic.loadUi(DIR + 'package_window.ui', self)
        self.parent = parent
        self.preamble = unicode(preamble)

        self.connect(self.cancelButton, QtCore.SIGNAL("clicked()"),
                     self.slot_cancel)

        self.connect(self.saveButton, QtCore.SIGNAL("clicked()"),
                     self.slot_save)

    def slot_open(self):
        self.preamble = self.parent.preamble
        self.preambleTextEdit.setText(self.preamble)
        self.show()

    def slot_cancel(self):
        self.close()

    def slot_save(self):
        self.preamble = unicode(self.preambleTextEdit.toPlainText())
        self.parent.preamble = self.preamble
        self.close()

class Note(object):
    """
    Note handles the creation and compilation of notes.
    """
    def __init__(self, text = None, preamble = PREAMBLE, compiler = COMPILER,
                 page = 1, pos = None, note_id = -1):
        self.filename = self.generate_filename()
        self.ImgPixmap = QtGui.QPixmap()

        self.text = text
        self._preamble = preamble
        self.compiler = compiler
        self.page = page
        self.pos = pos
        self.note_id = note_id

    @property
    def preamble(self):
        return self._preamble
    @preamble.setter
    def preamble(self, preamble):
        self._preamble = preamble
        self.ImageLabel = preamble
        self.update()

    def generate_filename(self):
        exists = True
        while exists:
            filename = str(randint(0, 999999)) + ".note.tex"
            try:
                filehandle = open(filename, 'w')
                exists = False
            except IOError:
                exists = True
        self.filename = filename
        return filename

    def generate_file(self):
        #print 'Generating file'
        try:
            filehandle = open(self.filename, 'w')
            filehandle.write(self.tex_source.encode('UTF-8'))
            filehandle.close()
            return True
        except IOError:
            print 'Could not write note!'
            return False

    def generate_from_tex(self):
        #print 'Generating dvi/pdf/ps'
        try:
            subprocess.call([self.compiler, "--interaction=nonstopmode",
                             self.filename], stdout=subprocess.PIPE)
            return True
        except OSError:
            print 'You do not have %s installed!' % self.compiler
            return False

    def generate_png(self):
        #print 'Generating png'
        filebase = self.filename.rstrip('tex')
        if self.compiler == 'latex':
            ext = 'dvi'
        elif self.compiler == 'pdflatex':
            ext = 'pdf'
        elif self.compiler == 'pslatex':
            ext = 'ps'
        filename_ext = filebase + ext
        filename_png = filebase + 'png'

        # Gotta learn how to use bbox on -T option
        dvipng_command = ["dvipng", "-x", "1500", "-Q", "17", "-T", "tight",
                            "--follow", "-o", filename_png, filename_ext]
        imagemagick_command  = ["convert", "-trim", "-density",
                                "%fx%f" % (1.5*DPI_X, 1.5*DPI_Y),
                                filename_ext, filename_png]
        if ext == 'dvi':
            try:
                subprocess.call(dvipng_command, stdout=subprocess.PIPE)
                return True
            except OSError:
                print 'You do not have a dvipng distribution!'
                print 'Falling back on imagemagick'
                try:
                    subprocess.call(imagemagick_command, stdout=subprocess.PIPE)
                    return True
                except OSError:
                    print 'You do not have imagemagick installed!'
                    return False
        elif (ext == 'pdf') or (ext == 'ps'):
            try:
                subprocess.call(imagemagick_command, stdout=subprocess.PIPE)
                subprocess.call(["convert", "-bordercolor", "white", "-border",
                                 "10x10", "-bordercolor", "grey", "-border",
                                 "2x2", filename_png, filebase + 'border.png'],
                                 stdout=subprocess.PIPE)
                return True
            except OSError:
                print 'You do not have imagemagick installed!'
                return False


    def generate_source(self):
        #print 'Generating source'
        tex_source  = self.preamble  + "\n"
        tex_source += '\pagestyle{empty}' + "\n"
        tex_source += "\\begin{document}\n"
        tex_source += "\\noindent\n"
        tex_source += self.text
        tex_source += "\n"+ '\end{document}'
        self.tex_source = tex_source

    def remove_files(self):
        #print 'Removing files'
        if self.compiler == 'latex':
            exte = 'dvi'
        elif self.compiler == 'pdflatex':
            exte = 'pdf'
        elif self.compiler == 'pslatex':
            exte = 'ps'
        for ext in ["aux", "log", "tex", exte]:
            filename = self.filename.rstrip('tex') + ext
            try:
                os.remove(filename)
            except OSError:
                print 'File %s was already removed.' % filename
                pass

    def remove_png(self):
        #print 'Removing png'
        for ext in ['png', 'border.png']:
            filename = self.filename.rstrip('tex') + ext
            try:
                os.remove(filename)
            except OSError:
                print 'File %s was already removed.' % filename
                pass

    def update(self):
        print 'Updating note %s' % self.note_id
        self.generate_source()
        if self.generate_file():
            if self.generate_from_tex():
                if self.generate_png():
                    self.remove_files()
                    self.ImgPixmap.load(self.filename.rstrip('tex') + 'png')

class ImageLabel(QtGui.QLabel):

    remove_trigger = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        super(ImageLabel, self).__init__()
        self.parent = parent
        self.preamble = PREAMBLE
        self.note_pos = QtCore.QPointF()
        self.note_icon_pos = QtCore.QPoint()
        self.current_note_id = 0
        self.closest_id = 0
        self.notes = {}
        self.noteImage = QtGui.QImage(DIR + 'img/note22.png')
        self.setMouseTracking(True)
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        #QtGui.QToolTip.setPalette(QtGui.QPalette(QtCore.Qt.white))
        #QtGui.QToolTip.showText(QtCore.QPoint(0,0),
        #'Alou <img src="%stest.border.png">' % DIR, self,
        #QtCore.QRect(0,0,100,100))
        #self.setToolTip('<img src="%stest.border.png">' % DIR)
        #QtCore.QRect(0,0,10,10))

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
        self.removeNoteAction = QtGui.QAction(self)
        self.removeNoteAction.setText("Remove annotation")
        self.connect(self.removeNoteAction, QtCore.SIGNAL("triggered()"),
                     self.slot_remove_note)
        self.change_menu.addAction(self.removeNoteAction)

    def mouseMoveEvent(self,  event):
        try:
            width = self.pt_to_px(self.parent.CurrentPage.pageSizeF())[0]
        except AttributeError:
            # No PDF has been loaded yet.
            width = 0

        x_offset = (self.rect().width() - width)/2.0
        if (event.x() >= x_offset) and (event.x() <= width + x_offset):
            if self.find_closest(event.x(), event.y()):
                note = self.notes[self.closest_id]
                note.generate_source()
                img_path =  DIR + note.filename.rstrip('tex') + 'border.png'
                QtGui.QToolTip.showText(event.globalPos(),
                                        'Note %d: <br /> <img src="%s">'
                                        % (note.note_id, img_path),
                                        self)
            else:
                self.parent.update_image()

    #def mouseReleaseEvent(self, event):
        #try:
            #width = self.pt_to_px(self.parent.CurrentPage.pageSizeF())[0]
        #except AttributeError:
            ## No PDF has been loaded yet.
            #width = 0
        #x_offset = (self.rect().width() - width)/2.0
        #if (event.x() >= x_offset) and (event.x() <= width + x_offset):
            #if self.find_closest(event.x(), event.y()):
                #print 'Click note %d' % self.closest_id
                #note = self.notes[self.closest_id]
                #note.generate_source()
                ##if note.generate_file():
                    ##if note.generate_from_tex():
                        ##if note.generate_png():
                            ##note.remove_files()
                #image = QtGui.QImage(note.filename.rstrip('tex') + 'border.png')
                #print '%s' % note.filename.rstrip('tex') + 'border.png'
                #painter = QtGui.QPainter()
                #painter.begin(self.parent.Image)
                #painter.drawImage(event.x() - x_offset, event.y(), image)
                #painter.end()
                #self.parent.ImgLabel.setPixmap(QtGui.QPixmap.fromImage(self.parent.Image))
            #else:
                #self.parent.update_image()

    def contextMenu(self, pos):
        #print self.notes.values()
        try:
            width = self.pt_to_px(self.parent.CurrentPage.pageSizeF())[0]
        except AttributeError:
            # No PDF has been loaded yet.
            width = 0
        x_offset = (self.rect().width() - width)/2.0
        if (pos.x() >= x_offset) and (pos.x() <= width + x_offset):
            if self.find_closest(pos.x(), pos.y()):
                self.change_menu.exec_(self.mapToGlobal(pos))
                print 'Edit'
            else:
                print 'Add'
                self.note_pos = self.px_2_pt(pos.x() - x_offset, pos.y())
                self.note_icon_pos = QtCore.QPoint(pos.x() - x_offset, pos.y())
                #print 'Note position: ', self.note_pos
                #print 'Mouse position', pos
                self.add_menu.exec_(self.mapToGlobal(pos))
        else:
            print 'Not in area'

    def find_closest(self, x, y):
        found_it = False
        width = self.pt_to_px(self.parent.CurrentPage.pageSizeF())[0]
        x_offset = (self.rect().width() - width)/2.0
        if len(self.notes) != 0:
            for note in self.notes.values():
                n_x = (note.pos.x() * self.parent.scale * DPI_X/72.0) + 11
                n_y = (note.pos.y() * self.parent.scale * DPI_X/72.0) + 11
                dx = abs(x - x_offset - n_x)
                dy = abs(y - n_y)
                if dx <= 11 and dy <= 11:
                    self.closest_id = note.note_id
                    found_it = True
                    break
        return found_it

    def slot_add_note(self):
        try:
            note_id = max(self.notes.keys()) + 1
        except ValueError:
            note_id = 0
        self.current_note_id = note_id
        self.notes[note_id] = Note('New note', self.preamble, COMPILER,
                                   self.parent.page, self.note_pos,
                                   note_id)

        x, y = self.pt_to_px(QtCore.QSize(self.note_pos.x(), self.note_pos.y()))
        painter = QtGui.QPainter()
        painter.begin(self.parent.Image)
        painter.drawImage(self.note_icon_pos, self.noteImage)
        painter.end()

        self.parent.ImgLabel.setPixmap(
                            QtGui.QPixmap.fromImage(self.parent.Image))

    def slot_edit_note(self):
        print "Editing note %d\n" % self.closest_id
        self.current_note_id = self.closest_id

    def slot_remove_note(self):
        print 'Remove note %d' % self.closest_id
        self.current_note_id = self.closest_id
        self.remove_trigger.emit()

    def pt_to_px(self, qsize):
        width = qsize.width()
        width *= self.parent.scale * DPI_X / 72.0

        height = qsize.height()
        height *= self.parent.scale * DPI_Y / 72.0

        return (width, height)

    def px_2_pt(self, x, y):
        width = 72.0 * x/(DPI_X * self.parent.scale)

        height = 72.0 * y/(DPI_Y * self.parent.scale)

        return QtCore.QPointF(width, height)

class AnnotationWidget(QtGui.QWidget):
    """
    AnnotationWidget holds the compiled annotation.
    """
    def __init__(self, parent = None, ImgPixmap = None):
        """ Initialize DocumentWidget. """
        QtGui.QWidget.__init__(self, parent)
        self.ImgLabel = QtGui.QLabel()
        self.ImgLabel.setAlignment(QtCore.Qt.AlignCenter)
        if ImgPixmap is None:
            self.ImgPixmap = QtGui.QPixmap()
        else:
            self.ImgPixmap = ImgPixmap
        self.ImgLabel.setPixmap(self.ImgPixmap)

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
        self.num_pages = None
        self.page = 0
        self.ImgLabel = ImageLabel(self)
        self.ImgLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ImgPixmap = QtGui.QPixmap()
        self.scale = 1

    def set_scale(self, event):
        """ Sets the scale with which the document will be redered. """
        self.scale = float(event)
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
            self.page = (event-1) % self.num_pages
            self.CurrentPage = self.Document.page(self.page)
            self.update_image()

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
                width = self.parent.rect().width() - 18 # Window border
                self.scale = 72.0*width/(DPI_X * page_size.width())
            else:
                height = self.parent.rect().height() - 2 # Window border
                self.scale = 72.0*height/(DPI_Y * page_size.height())
            self.update_image()

    def update_image(self):
        """ Updates Image and ImgLabel. """
        if self.Document is not None:
            self.Image = self.CurrentPage.renderToImage(DPI_X*self.scale,
                                                        DPI_Y*self.scale)
            self.ImgLabel.setPixmap(self.ImgPixmap.fromImage(self.Image))

            for note in self.ImgLabel.notes.values():
                if note.page == self.page:
                    #print note.note_id
                    x = note.pos.x()
                    x *= self.scale * DPI_X / 72.0

                    y = note.pos.y()
                    y *= self.scale * DPI_Y / 72.0

                    #print x,y
                    painter = QtGui.QPainter()
                    painter.begin(self.Image)
                    painter.drawImage(x, y, self.ImgLabel.noteImage)
                    painter.end()

            self.ImgLabel.setPixmap(QtGui.QPixmap.fromImage(self.Image))

class MainWindow(QtGui.QMainWindow):
    """ Main Window Class """
    def __init__(self, parent=None):
        """ Initialize MainWindow """
        QtGui.QMainWindow.__init__(self, parent)
        uic.loadUi(DIR + 'window.ui', self)
        self.setWindowIcon(QtGui.QIcon(DIR + 'img/note64.png'))
        self._preamble = PREAMBLE
        self.displayed_note_id = -1

        # File menu
        self.connect(self.actionOpen, QtCore.SIGNAL("triggered()"),
                     self.slot_open)
        self.connect(self.actionQuit, QtCore.SIGNAL("triggered()"),
                     self.close)

        # Windows menu
        self.connect(self.actionControls,
                     QtCore.SIGNAL("toggled(bool)"),
                     self.controlsWidget.setVisible)
        self.connect(self.actionAnnotationSource,
                     QtCore.SIGNAL("toggled(bool)"),
                     self.annotationSourceDockWidget.setVisible)
        self.connect(self.actionAnnotation,
                     QtCore.SIGNAL("toggled(bool)"),
                     self.annotationDockWidget.setVisible)

        self.connect(self.controlsWidget,
                     QtCore.SIGNAL("visibilityChanged(bool)"),
                     self.slot_hide_controls)
        self.connect(self.annotationDockWidget,
                     QtCore.SIGNAL("visibilityChanged(bool)"),
                     self.slot_hide_annotation)
        self.connect(self.annotationSourceDockWidget,
                     QtCore.SIGNAL("visibilityChanged(bool)"),
                     self.slot_hide_annotation_source)

        # PDF viewer widget
        self.documentWidget = DocumentWidget(self.scrollArea)
        self.documentWidget.setObjectName("documentWidget")
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.documentWidget.ImgLabel)

        # Connections for PDF viewer
        self.connect(self.previousPageButton, QtCore.SIGNAL("clicked()"),
                     self.slot_prev_page)
        self.connect(self.nextPageButton, QtCore.SIGNAL("clicked()"),
                     self.slot_next_page)
        self.connect(self.pageSpinBox, QtCore.SIGNAL("valueChanged(int)"),
                     self.documentWidget.change_page)
        self.connect(self.scaleSpinBox, QtCore.SIGNAL("valueChanged(QString)"),
                    self.documentWidget.set_scale)
        self.connect(self.scaleComboBox,
                     QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.slot_scale)

        # Scroll Widget for annotation
        self.scrollAreaAnnotation = QtGui.QScrollArea(self.annotationDockWidget)
        self.scrollAreaAnnotation.setWidgetResizable(True)
        self.scrollAreaAnnotation.setObjectName("scrollAreaAnnotation")
        self.gridLayoutAnnotationDock.addWidget(self.scrollAreaAnnotation,
                                                0, 0, 1, 1)

        # Beginning note
        self.current_note = Note(WELCOME, self.preamble)

        # Annotation PNG widget
        self.annotationWidget = AnnotationWidget(self.scrollAreaAnnotation,
                                                 self.current_note.ImgPixmap)
        self.annotationWidget.setObjectName("annotationWidget")

        self.scrollAreaAnnotation.setBackgroundRole(QtGui.QPalette.Light)
        self.scrollAreaAnnotation.setWidget(self.annotationWidget.ImgLabel)

        # Connections for Annotation widget
        self.connect(self.compileButton, QtCore.SIGNAL("clicked()"),
                     self.slot_compile_annotation)

        # Annotation Source Widget
        self.annotationSourceTextEdit.setText(WELCOME)
        self.connect(self.documentWidget.ImgLabel.addNoteAction,
                     QtCore.SIGNAL("triggered()"), self.slot_change_note)
        self.connect(self.documentWidget.ImgLabel.editNoteAction,
                     QtCore.SIGNAL("triggered()"), self.slot_change_note)
        #self.connect(self.documentWidget.ImgLabel.removeNoteAction,
                     #QtCore.SIGNAL("triggered()"), self.slot_remove_note)
        self.documentWidget.ImgLabel.remove_trigger.connect(
                                                    self.slot_remove_note)

        # Connections for Annotation Source Widget
        self.timer = QtCore.QTimer()
        self.timer.start(3500)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.slot_compile_annotation)
        self.old_text = ''

        # Package editor
        self.packageWindow = PreambleWindow(self)
        self.connect(self.actionPackagesDialog, QtCore.SIGNAL("triggered()"),
                     self.packageWindow.slot_open)

    @property
    def preamble(self):
        return self._preamble
    @preamble.setter
    def preamble(self, preamble):
        self._preamble = preamble
        self.current_note.preamble = preamble
        self.slot_compile_annotation()

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
            self.statusBar().showMessage('Opened file %s.' % filename)

    def slot_change_note(self):
        note_id = self.documentWidget.ImgLabel.current_note_id
        if (self.displayed_note_id != -1 and self.displayed_note_id != -2):
            text = unicode(self.annotationSourceTextEdit.toPlainText())
            self.current_note.text = text
        else:
            self.current_note.remove_png()
        #self.current_note.remove_png()
        self.current_note = self.documentWidget.ImgLabel.notes[note_id]
        self.annotationSourceTextEdit.setText(self.current_note.text)
        self.slot_compile_annotation()

    def slot_remove_note(self):
        note_id = self.documentWidget.ImgLabel.closest_id
        self.documentWidget.ImgLabel.notes[note_id].remove_files()
        self.documentWidget.ImgLabel.notes[note_id].remove_png()
        print 'Main remove note %d' % note_id
        if self.documentWidget.ImgLabel.current_note_id == note_id:
            self.annotationSourceTextEdit.setText('')
            whitePixmap = QtGui.QPixmap()
            whitePixmap.fill()
            self.annotationWidget.ImgLabel.setPixmap(whitePixmap)
            self.documentWidget.ImgLabel.displayed_note_id = -2
            self.documentWidget.ImgLabel.current_note_id = -2
        del self.documentWidget.ImgLabel.notes[note_id]
        self.documentWidget.update_image()

    def slot_hide_controls(self, event):
        """ Slot to hide controls properly and avoid recursion. """
        if self.controlsWidget.isVisible():
            self.actionControls.setChecked(True)
        if self.annotationDockWidget.isHidden():
            self.actionControls.setChecked(False)

    def slot_hide_annotation(self, event):
        """ Slot to hide annotation properly and avoid recursion. """
        if self.annotationDockWidget.isVisible():
            self.actionAnnotation.setChecked(True)
        if self.annotationDockWidget.isHidden():
            self.actionAnnotation.setChecked(False)

    def slot_hide_annotation_source(self, event):
        """ Slot to hide annotation source properly and avoid recursion. """
        if self.annotationSourceDockWidget.isVisible():
            self.actionAnnotationSource.setChecked(True)
        if self.annotationSourceDockWidget.isHidden():
            self.actionAnnotationSource.setChecked(False)

    def slot_prev_page(self):
        """ Slot to go to the previous page. """
        self.pageSpinBox.setValue(self.pageSpinBox.value() - 1)

    def slot_next_page(self):
        """ Slot to go to the next page. """
        self.pageSpinBox.setValue(self.pageSpinBox.value() + 1)

    def slot_scale(self, event):
        """ Slot to change the scale. """
        if event == 0:
            self.scaleSpinBox.setEnabled(True)
            self.documentWidget.set_scale(self.scaleSpinBox.value())
        else:
            self.scaleSpinBox.setEnabled(False)
            self.documentWidget.fit_to_width_or_height(event)

    def slot_compile_annotation(self):
        """
        Slot to compile the current annotation by changing annotationWidget's
        ImgLabel's Pixmap to the updated one.
        """
        text = unicode(self.annotationSourceTextEdit.toPlainText())
        if (self.old_text != text and
            self.documentWidget.ImgLabel.current_note_id  != -2):
            self.old_text = text
            self.current_note.remove_png()
            self.current_note.text = text
            self.current_note.update()
            self.displayed_note_id = self.current_note.note_id
            self.annotationWidget.ImgLabel.setPixmap(
                                            self.current_note.ImgPixmap)

    def resizeEvent(self, event):
        """ Slot to adjust widgets when MainWindow is resized. """
        if self.scaleComboBox.currentIndex() == 1:
            self.documentWidget.fit_to_width_or_height(0)
        elif self.scaleComboBox.currentIndex() == 2:
            self.documentWidget.fit_to_width_or_height(2)

    def closeEvent(self, event):
        for note in self.documentWidget.ImgLabel.notes.values():
            note.remove_files()
            note.remove_png()
        self.current_note.remove_files()
        self.current_note.remove_png()
