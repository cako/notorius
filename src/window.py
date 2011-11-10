#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" Window. """

import os
import subprocess
import popplerqt4
from PyQt4 import QtCore, QtGui, uic
from platform import system as systemplat
from random import randint

PREAMBLE = '''\documentclass[12pt,a4paper]{article}
\usepackage[utf8x]{inputenc}
'''

WELCOME = u"""\\begin{center}
Hello and welcome to notorius!
\end{center}
\[ \int_\Omega\,dµ = µ(\Omega) \]"""


PLATFORM = systemplat()
if PLATFORM == 'Linux':
    try:
        PROC1 = subprocess.Popen(["xdpyinfo"], stdout=subprocess.PIPE)
        PROC2 = subprocess.Popen(["grep", "dots"], stdin=PROC1.stdout,
                                                   stdout=subprocess.PIPE)
        OUT = PROC2.communicate()[0]
        DPI = OUT.strip().split()[1]
        (DPI_X, DPI_Y) = [ int(dpi) for dpi in DPI.split('x') ]
    except OSError:
        DPI_X = DPI_X = 96
else:
    DPI_X = DPI_X = 96

class PreambleWindow(QtGui.QMainWindow):
    """
    PackageDialog allows for editing of packages
    """
    def __init__(self, parent = None, preamble = PREAMBLE):
        QtGui.QMainWindow.__init__(self, parent)
        uic.loadUi('package_window.ui', self)
        self.ParentWindow = parent
        self.preamble = unicode(preamble)

        self.connect(self.cancelButton, QtCore.SIGNAL("clicked()"),
                     self.slot_cancel)

        self.connect(self.saveButton, QtCore.SIGNAL("clicked()"),
                     self.slot_save)

    def slot_open(self):
        self.preamble = self.ParentWindow.preamble
        self.preambleTextEdit.setText(self.preamble)
        self.show()

    def slot_cancel(self):
        self.close()

    def slot_save(self):
        self.preamble = unicode(self.preambleTextEdit.toPlainText())
        self.ParentWindow.preamble = self.preamble
        self.close()

class Note(object):
    """
    Note handles the creation and compilation of notes.
    """
    def __init__(self, text = None, preamble = PREAMBLE, note_id=0):
        self.filename = self.generate_filename()
        self.ImgPixmap = QtGui.QPixmap()
        self.note_id = note_id
        self._preamble = preamble
        self._text = text
        if text is not None:
            self.text = text

    @property
    def text(self):
        return self._text
    @text.setter
    def text(self, text):
        self._text = text
        self.update()

    @property
    def preamble(self):
        return self._preamble
    @preamble.setter
    def preamble(self, preamble):
        self._preamble = preamble
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
        filehandle = open(self.filename, 'w')
        filehandle.write(self.tex_source.encode('UTF-8'))
        filehandle.close()

    def generate_dvi(self):
        try:
            latex_proc = subprocess.call(["latex", "--interaction=nonstopmode",
                                           self.filename],
                                           stdout=subprocess.PIPE)
        except OSError:
            print 'You do not have a LaTeX distribution!'

    def generate_png(self):
        filebase = self.filename.rstrip('tex')
        filename_dvi = filebase + 'dvi'
        filename_png = filebase + 'png'
        # Gotta learn how to use bbox on -T option
        try:
            dvipng_proc = subprocess.call(["dvipng", "-x", "1500", "-Q", "17",
                                            "-T", "tight", "--follow", "-o",
                                            filename_png, filename_dvi],
                                            stdout=subprocess.PIPE)
        except OSError:
            print 'You do not have a dvipng distribution!'

    def generate_source(self):
        tex_source  = self.preamble  + "\n"
        tex_source += '\pagestyle{empty}' + "\n"
        tex_source += "\\begin{document}\n"
        tex_source += self.text
        tex_source += "\n"+ '\end{document}'
        self.tex_source = tex_source

    def remove_files(self):
        for ext in ["aux", "log", "dvi", "tex"]:
            os.remove(self.filename.rstrip('tex') + ext)

    def remove_png(self):
        os.remove(self.filename.rstrip('tex') + 'png')

    def update(self):
        self.generate_source()
        self.generate_file()
        self.generate_dvi()
        self.generate_png()
        self.remove_files()
        self.ImgPixmap.load(self.filename.rstrip('tex') + 'png')

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
        self.ParentWidget = parent
        self.Document = None
        self.CurrentPage = None
        self.Image = None
        self.num_pages = None
        self.ImgLabel = QtGui.QLabel()
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
        self.CurrentPage =  self.Document.page(0)
        self.num_pages = self.Document.numPages()
        self.set_scale(1)

    def change_page(self, event):
        """ Changes the page. """
        if self.Document is not None:
            self.CurrentPage = self.Document.page( (event-1)%self.num_pages )
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
                width = self.ParentWidget.rect().width() - 18 # Window border
                self.scale = 72.0*width/(DPI_X * page_size.width())
            else:
                height = self.ParentWidget.rect().height() - 2 # Window border
                self.scale = 72.0*height/(DPI_Y * page_size.height())
            self.update_image()

    def update_image(self):
        """ Updates Image and ImgLabel. """
        if self.Document is not None:
            self.Image = self.CurrentPage.renderToImage(DPI_X*self.scale,
                                                        DPI_Y*self.scale)
            self.ImgLabel.setPixmap(self.ImgPixmap.fromImage(self.Image))

class MainWindow(QtGui.QMainWindow):
    """ Main Window Class """
    def __init__(self, parent=None):
        """ Initialize MainWindow """
        QtGui.QMainWindow.__init__(self, parent)
        uic.loadUi('window.ui', self)
        self._preamble = PREAMBLE

        # File menu
        self.connect(self.actionOpen, QtCore.SIGNAL("triggered()"),
                     self.slot_open)
        self.connect(self.actionQuit, QtCore.SIGNAL("triggered()"),
                     self.close)

        # Windows menu
        self.connect(self.actionControls,
                     QtCore.SIGNAL("toggled(bool)"),
                     self.controlsDockWidget.setVisible)
        self.connect(self.actionAnnotationSource,
                     QtCore.SIGNAL("toggled(bool)"),
                     self.annotationSourceDockWidget.setVisible)
        self.connect(self.actionAnnotation,
                     QtCore.SIGNAL("toggled(bool)"),
                     self.annotationDockWidget.setVisible)

        self.connect(self.controlsDockWidget,
                     QtCore.SIGNAL("visibilityChanged(bool)"),
                     self.slot_hide_controls)
        self.connect(self.annotationDockWidget,
                     QtCore.SIGNAL("visibilityChanged(bool)"),
                     self.slot_hide_annotation)
        self.connect(self.annotationSourceDockWidget,
                     QtCore.SIGNAL("visibilityChanged(bool)"),
                     self.slot_hide_annotation_source)

        # Scroll Widget for PDF viewer
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

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

    def slot_hide_controls(self, event):
        """ Slot to hide controls properly and avoid recursion. """
        if self.controlsDockWidget.isVisible():
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
        self.current_note.remove_png()
        text = unicode(self.annotationSourceTextEdit.toPlainText())
        self.current_note.text = text
        self.annotationWidget.ImgLabel.setPixmap(self.current_note.ImgPixmap)

    def resizeEvent(self, event):
        """ Slot to adjust widgets when MainWindow is resized. """
        if self.scaleComboBox.currentIndex() == 1:
            self.documentWidget.fit_to_width_or_height(1)
        elif self.scaleComboBox.currentIndex() == 2:
            self.documentWidget.fit_to_width_or_height(2)

    def closeEvent(self, event):
        self.current_note.remove_png()
