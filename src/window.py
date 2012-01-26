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

""" Main Window. """

import os
import datetime
import popplerqt4
import zipfile

from window_ui import Ui_MainWindow
from preamble_window import PreambleWindow
from offset_window import OffsetWindow
from document_widget import DocumentWidget
from search_widget import SearchWidget
from annotation_widget import AnnotationWidget
from note import Note
from constants import *
from icons import *


from PyQt4 import QtCore, QtGui, QtXml
from xml.etree import ElementTree as xml

VERSION = '0.1.%s' %'120126-1518'

class MainWindow(QtGui.QMainWindow):
    """ Main Window Class """
    def mousePressEvent(self, event):
        print 'main has focus?', self.hasFocus()

    add_windows_trigger = QtCore.pyqtSignal(list)

    def __init__(self, parent=None, document = None):
        """ Initialize MainWindow """
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':img/note64.png'))
        self._preamble = PREAMBLE
        self.offset = 0
        self.docpath = ''
        self.rmdoc = False
        self.displayed_uid = -1
        self.okular_notes = []

        # Toolbar icons
        self.ui.actionOpen.setIcon(QtGui.QIcon.fromTheme("document-open"))
        self.ui.actionExport.setIcon(QtGui.QIcon.fromTheme("document-save-as"))
        self.ui.actionQuit.setIcon(QtGui.QIcon.fromTheme("application-exit"))

        self.ui.actionPreambleEditor.setIcon(QtGui.QIcon.fromTheme(
                                                        "preferences-other"))

        self.ui.actionAbout.setIcon(QtGui.QIcon.fromTheme("help-about"))

        # Toolbar connections
        self.connect(self.ui.actionOpen, QtCore.SIGNAL("triggered()"),
                     self.slot_gui_open)
        self.connect(self.ui.actionExport, QtCore.SIGNAL("triggered()"),
                     self.slot_export)
        self.connect(self.ui.actionQuit, QtCore.SIGNAL("triggered()"),
                     self.close)

        self.connect(self.ui.actionControls,
                     QtCore.SIGNAL("toggled(bool)"),
                     self.ui.controlsWidget.setVisible)
        self.connect(self.ui.actionAnnotationSource,
                     QtCore.SIGNAL("toggled(bool)"),
                     self.ui.annotationSourceDockWidget.setVisible)
        self.connect(self.ui.actionAnnotation,
                     QtCore.SIGNAL("toggled(bool)"),
                     self.ui.annotationDockWidget.setVisible)
        self.connect(self.ui.controlsWidget,
                     QtCore.SIGNAL("visibilityChanged(bool)"),
                     self.slot_hide_controls)
        self.connect(self.ui.annotationDockWidget,
                     QtCore.SIGNAL("visibilityChanged(bool)"),
                     self.slot_hide_annotation)
        self.connect(self.ui.annotationSourceDockWidget,
                     QtCore.SIGNAL("visibilityChanged(bool)"),
                     self.slot_hide_annotation_source)

        self.connect(self.ui.actionAbout, QtCore.SIGNAL("triggered()"),
                     self.slot_about)

        # Document controls
        if PLATFORM == 'Windows':
            self.ui.previousPageButton.setText('Previous')
            self.ui.nextPageButton.setText('Next')
            font_metrics = QtGui.QFontMetrics(QtGui.QFont())
            size_p = font_metrics.size(QtCore.Qt.TextSingleLine, 'Previous')
            size_n = font_metrics.size(QtCore.Qt.TextSingleLine, 'Next')
            self.ui.previousPageButton.setMinimumWidth(size_p.width() + 10)
            self.ui.nextPageButton.setMinimumWidth(size_n.width() + 10)
        else:
            self.ui.previousPageButton.setIcon(QtGui.QIcon.fromTheme("go-previous"))
            self.ui.nextPageButton.setIcon(QtGui.QIcon.fromTheme("go-next"))
        self.ui.controlsWidget.mouseMoveEvent = self.highlight_buttons

        self.offsetWindow = OffsetWindow(self)
        self.connect(self.ui.offsetCheckBox, QtCore.SIGNAL("stateChanged(int)"),
                     self.offsetWindow.slot_open)

        # Search widget
        self.ui.searchWidget = SearchWidget(self.ui.searchDockWidgetContents)
        self.ui.gridLayout_4.addWidget(self.ui.searchWidget, 0, 0, 1, 1)
        self.ui.searchDockWidget.hide()
        self.ui.searchWidget.hide_trigger.connect(self.ui.searchDockWidget.hide)
        self.ui.searchWidget.change_page_trigger.connect(self.ui.pageSpinBox.setValue)
        #self.ui.searchWidget.show_trigger.connect(self.ui.searchDockWidget.show)

        # PDF viewer widget
        self.ui.scrollArea.setMinimumWidth(0)
        self.ui.documentWidget = DocumentWidget(self.ui.scrollArea)
        self.ui.documentWidget.setObjectName("documentWidget")
        self.ui.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.ui.scrollArea.setWidget(self.ui.documentWidget.ImgLabel)
        self.connect(self.ui.documentWidget.ImgLabel,
                     QtCore.SIGNAL("dropped"), self.slot_load_dropped)
        self.ui.documentWidget.ImgLabel.change_scale_trigger.connect(
                                                self.ui.scaleSpinBox.setValue)
        self.ui.documentWidget.ImgLabel.show_search_trigger.connect(
                                                self.slot_show_search_widget)
        self.ui.documentWidget.ImgLabel.hide_search_trigger.connect(
                                                self.ui.searchWidget.hide)

        # Connections for PDF viewer
        self.connect(self.ui.previousPageButton, QtCore.SIGNAL("clicked()"),
                     self.slot_prev_page)
        self.connect(self.ui.nextPageButton, QtCore.SIGNAL("clicked()"),
                     self.slot_next_page)
        self.connect(self.ui.pageSpinBox, QtCore.SIGNAL("valueChanged(int)"),
                     self.ui.documentWidget.change_page)
        self.connect(self.ui.scaleSpinBox, QtCore.SIGNAL("valueChanged(double)"),
                    self.ui.documentWidget.set_scale)
        self.connect(self.ui.scaleComboBox,
                     QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.slot_scale)

        # Scroll Widget for annotation
        self.ui.scrollAreaAnnotation = QtGui.QScrollArea(self.ui.annotationDockWidget)
        self.ui.scrollAreaAnnotation.setWidgetResizable(True)
        self.ui.scrollAreaAnnotation.setObjectName("scrollAreaAnnotation")
        self.ui.gridLayoutAnnotationDock.addWidget(self.ui.scrollAreaAnnotation,
                                                0, 0, 1, 1)

        # Beginning note
        self.current_note = Note(WELCOME, self.preamble)

        # Annotation PNG widget
        self.ui.annotationWidget = AnnotationWidget(self.ui.scrollAreaAnnotation,
                                                 self.current_note.icon)
        self.ui.annotationWidget.setObjectName("annotationWidget")

        self.ui.scrollAreaAnnotation.setBackgroundRole(QtGui.QPalette.Light)
        self.ui.scrollAreaAnnotation.setWidget(self.ui.annotationWidget.ImgLabel)
        self.ui.actionAnnotation.toggle()

        # Connections for Annotation widget
        self.connect(self.ui.compileButton, QtCore.SIGNAL("clicked()"),
                     self.slot_force_compile)

        # Annotation Source Widget
        self.ui.annotationSourceTextEdit.setText(WELCOME)
        self.connect(self.ui.documentWidget.ImgLabel.addNoteAction,
                     QtCore.SIGNAL("triggered()"), self.slot_change_note)
        self.connect(self.ui.documentWidget.ImgLabel.editNoteAction,
                     QtCore.SIGNAL("triggered()"), self.slot_change_note)
        #self.connect(self.ui.documentWidget.ImgLabel.removeNoteAction,
                     #QtCore.SIGNAL("triggered()"), self.slot_remove_note)
        self.ui.documentWidget.ImgLabel.remove_trigger.connect(
                                                    self.slot_remove_note)
        self.ui.documentWidget.ImgLabel.toggle_source_trigger.connect(
                                        self.ui.actionAnnotationSource.toggle)
        self.ui.actionAnnotationSource.toggle()

        # Connections for Annotation Source Widget
        self.timer = QtCore.QTimer()
        self.timer.start(3500)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.slot_compile_annotation)
        self.old_text = ''

        # Preamble editor
        self.preambleEditorWindow = PreambleWindow(self)
        self.connect(self.ui.actionPreambleEditor, QtCore.SIGNAL("triggered()"),
                     self.preambleEditorWindow.slot_open)

        # Status bar
        self.ui.documentWidget.ImgLabel.set_clipboard_trigger.connect(
                                                    self.slot_set_status)

        if document is not None:
            self.load_file(document)

    @property
    def preamble(self):
        return self._preamble
    @preamble.setter
    def preamble(self, preamble):
        self._preamble = preamble
        self.current_note.preamble = preamble
        self.slot_compile_annotation()

    def highlight_buttons(self, event):
        if self.ui.previousPageButton.underMouse():
            self.ui.previousPageButton.setFlat(False)
        else:
            self.ui.previousPageButton.setFlat(True)

        if self.ui.nextPageButton.underMouse():
            self.ui.nextPageButton.setFlat(False)
        else:
            self.ui.nextPageButton.setFlat(True)

    def slot_load_dropped(self, files):
        if self.docpath == '' or files[0].endswith('.xml'):
            self.load_file(files.pop(0))
        windows = []
        for doc in files:
            win = MainWindow(document=doc)
            windows += [win]
            win.show()
        self.add_windows_trigger.emit(windows)
        #print files

    def slot_set_status(self, text):
        """ Slot to set statusBar with message. """
        self.statusBar().showMessage('Copied "%s" to clipboard.' % 
                                     unicode(text).strip())
    def slot_about(self):
        about_msg = '''
        <p><center><font size="4"><b>Notorius %s</b></font></center></p>
        <p><b>Author</b>: Carlos da Costa</p>
        <p><b>Code at</b>: <a href="https://github.com/cako/notorius">
                                    https://github.com/cako/notorius<a/></p>
        <p><b>License</b>: <a href="http://www.gnu.org/licenses/gpl-3.0.txt">
                                    GNU General Public License version 3</a></p>
                    ''' % VERSION
        QtGui.QMessageBox.about(self, "About me", about_msg)

    def slot_gui_open(self):
        """ Slot for actionOpen. """
        if PLATFORM == 'Windows':
            home = os.getenv('HOMEPATH')
        else:
            home = os.getenv('HOME')
        if not home:
            home = DIR
        filename = unicode(
                   QtGui.QFileDialog.getOpenFileName(self, 'Open file', home,
"PDF files (*.pdf);;Okular (*.okular);;ZIP archive (*.zip);; XML file (*.xml)"))
        self.load_file(filename)

    def load_file(self, filename = None):
        def parse_metadata(root):
            notes = {}
            for page in root.find('pageList').findall('page'):
                pg = int(page.attrib['number'])
                annotlist = page.find('annotationList')
                for annot in annotlist.findall('annotation'):
                    if ( annot.attrib['type'] == "1" and
                                        pg <= self.ui.documentWidget.num_pages ):
                        base = annot.find('base')
                        try:
                            author = base.attrib['author']
                        except KeyError:
                            author = ''
                        try:
                            text = base.attrib['contents']
                        except KeyError:
                            text = ''
                        try:
                            cdate = base.attrib['creationDate']
                        except KeyError:
                            cdate = ''
                        try:
                            mdate = base.attrib['modifyDate']
                        except KeyError:
                            mdate = ''
                        try:
                            preamble = base.attrib['preamble']
                        except KeyError:
                            preamble = PREAMBLE
                        try:
                            uname = base.attrib['uniqueName']
                            # notorius-1-0 becomes 0
                            uid = int(uname.rsplit('-')[-1])
                        except KeyError:
                            try:
                                uid = max(notes.keys())
                            except ValueError:
                                uid = 0

                        boundary = base.find('boundary')
                        x = float(boundary.attrib['l'])
                        y = float(boundary.attrib['t'])
                        size = self.ui.documentWidget.Document.page(
                                                        pg).pageSizeF()
                        pos = QtCore.QPointF(x*size.width(),
                                             y*size.height())
                        note = Note(text, preamble, page = pg, pos = pos,
                                    uid = uid)
                        notes[uid] = note
                        note.cdate = datetime.datetime.strptime(cdate, "%Y-%m-%dT%H:%M:%S")
                        note.mdate = datetime.datetime.strptime(mdate, "%Y-%m-%dT%H:%M:%S")
                        note.update()
                    else:
                        self.okular_notes += [ annot ]
            return notes
        loaded = False
        if filename:
            self.ui.nextPageButton.setEnabled(True)
            self.ui.previousPageButton.setEnabled(True)
            self.ui.pageSpinBox.setEnabled(True)
            self.ui.offsetCheckBox.setEnabled(True)
            self.ui.offsetCheckBox.setChecked(False)
            self.ui.scaleSpinBox.setEnabled(True)
            self.ui.scaleComboBox.setEnabled(True)
            #file_dir = os.path.dirname(filename)
            self.okular_notes = []
            if filename.endswith('.zip') or filename.endswith('.okular'):
                self.rmdoc = True
                zipf = zipfile.ZipFile(filename, 'r')
                zipf.extractall(TMPDIR)
                # [ 'filename.pdf', 'content.xml', 'metadata.xml' ]
                # becomes [ 'filename.pdf' ] which then becomes 'filename.pdf'
                # then TMPDIR is added.
                # Important! filename can have .okular extension!
                self.docpath = os.path.join(TMPDIR,
                                            [ fl for fl in zipf.namelist() if (
                                            fl.rsplit('.')[1] != 'xml') ][0])
                # Must insert try statement!
                self.ui.documentWidget.load_document(self.docpath)
                loaded = True
                root = xml.parse(os.path.join(TMPDIR, 'metadata.xml')).getroot()
                notes = parse_metadata(root)
                for aux in ['content.xml', 'metadata.xml']:
                    os.remove(os.path.join(TMPDIR, aux))
                self.ui.documentWidget.ImgLabel.notes = notes
                self.ui.documentWidget.update_image()
                self.setWindowTitle('Notorius - %s' %os.path.basename(filename))
                if self.okular_notes:
                    warning = 'Not loading annotations that are '
                    warning += 'not text notes or are out of range.'
                    QtGui.QMessageBox.warning(self, "Warning", warning)
            elif filename.endswith('.xml'):
                if self.docpath == '':
                    QtGui.QMessageBox.warning(self, "Warning",
                                            'You need to load a PDF first!.')
                    loaded = False
                else:
                    self.rmdoc = False
                    root = xml.parse(filename).getroot()
                    self.ui.documentWidget.ImgLabel.notes = parse_metadata(root)
                    self.ui.documentWidget.update_image()
                    loaded = True
                    self.setWindowTitle(
                        'Notorius - %s + %s' % (os.path.basename(self.docpath),
                                                os.path.basename(filename)))
                    if self.okular_notes:
                        warning = 'Not loading annotations that are '
                        warning += 'not text notes or are out of range.'
                        QtGui.QMessageBox.warning(self, "Warning", warning)
            else:
                if not filename.endswith('.pdf'):
                    print "Treating file as pdf!"
                self.rmdoc = False
                self.docpath = filename
                self.ui.documentWidget.load_document(self.docpath)
                self.setWindowTitle('Notorius - %s' %os.path.basename(filename))
                loaded = True

            if loaded:
                self.ui.pageSpinBox.setValue(1)
                self.ui.pageSpinBox.setMinimum(-self.ui.documentWidget.num_pages + 1)
                self.ui.pageSpinBox.setMaximum(self.ui.documentWidget.num_pages)
                self.ui.scaleComboBox.setCurrentIndex(0)
                self.ui.maxPageLabel.setText("of %d" %
                                          self.ui.documentWidget.num_pages)
                self.ui.actionExport.setEnabled(True)
                self.ui.searchWidget.documentWidget = self.ui.documentWidget
                self.statusBar().showMessage('Opened file %s.' % filename)
        else:
            print 'No file to load!'

    def slot_export(self):
        file_dir = os.path.dirname(self.docpath)
        file_base = os.path.basename(self.docpath)
        filt = QtCore.QString()
        filename = unicode(QtGui.QFileDialog.getSaveFileName(self,
            'Save archive as', file_dir,
            "Okular archive (*.okular);;ZIP archive (*.zip);;XML file (*.xml)",
            filt))
        if filename:
            # Create the content.xml file
            if filt != 'XML file (*.xml)':
                content_path = os.path.join(TMPDIR, 'content.xml')
                root = xml.Element('OkularArchive')
                child_files = xml.SubElement(root, 'Files')
                child_doc = xml.SubElement(child_files, 'DocumentFileName')
                child_doc.text = file_base
                child_meta = xml.SubElement(child_files, 'MetadataFileName')
                child_meta.text = 'metadata.xml'
                xml.ElementTree(root).write(content_path)

            # Create the metadata.xml file
            if filt != 'XML file (*.xml)':
                metadata_path = os.path.join(TMPDIR, 'metadata.xml')
            else:
                metadata_path = filename
            root = xml.Element('documentInfo')
            pagelist = xml.SubElement(root, 'pageList')
            notes = self.ui.documentWidget.ImgLabel.notes
            for note in notes.values():
                try:
                    page = [ pg for pg in pagelist if (
                                int(pg.attrib['number']) == note.page) ][0]
                    annotlist = page.find('annotationList')

                except IndexError:
                    page = xml.SubElement(pagelist, 'page')
                    page.set('number', str(note.page))
                    annotlist = xml.SubElement(page, 'annotationList')

                annot = xml.SubElement(annotlist, 'annotation')
                annot.set('type', '1')

                base = xml.SubElement(annot, 'base')
                base.set('creationDate', note.cdate.isoformat()) #BOGUS DATE
                base.set('uniqueName', 'notorius-%d-%d' % (note.page, note.uid))
                base.set('author', USERNAME)
                base.set('contents', note.text)
                base.set('preamble', note.preamble)
                base.set('modifyDate', note.mdate.isoformat()) #BOGUS DATE
                base.set('color', '#ffff00')

                boundary = xml.SubElement(base, 'boundary')
                size = self.ui.documentWidget.Document.page(note.page).pageSizeF()
                posx = note.pos.x()/size.width()
                posy = note.pos.y()/size.height()
                boundary.set('l', str(posx))
                boundary.set('r', str(posx + 0.03)) # "Empirical values"
                boundary.set('b', str(posy + 0.022))
                boundary.set('t', str(posy))

                window = xml.SubElement(base, 'window')
                window.set('width', '0')
                window.set('flags', '-1')
                window.set('title', '')
                window.set('left', '0')
                window.set('height', '0')
                window.set('summary', 'LaTeXNote')
                window.set('top', '0')

                text = xml.SubElement(annot, 'text')
                text.set('icon', 'None')

            # Write okular notes that are not displayed
            for annot in self.okular_notes:
                pg_n = False
                try:
                    pg_n = annot.find('base').attrib['uniqueName'].split('-')[1]
                except IndexError:
                    # Did not find page, ignore
                    pass
                if pg_n:
                    try:
                        page = [ pg for pg in pagelist if (
                                    pg.attrib['number'] == pg_n) ][0]
                        annotlist = page.find('annotationList')

                    except IndexError:
                        page = xml.SubElement(pagelist, 'page')
                        page.set('number', str(note.page))
                        annotlist = xml.SubElement(page, 'annotationList')
                    annotlist.append(annot)


            xml.ElementTree(root).write(metadata_path)

            # Create the archive
            if ( filt == "ZIP archive (*.zip)" and not
                                                filename.endswith('.zip') ):
                filename += '.zip'
            elif ( filt == "Okular archive (*.okular)" and not
                                                filename.endswith('.okular') ):
                filename += '.okular'
            elif ( filt == 'XML file (*.xml)' and not
                                                filename.endswith('.xml') ):
                filename += '.xml'
            if filt != 'XML file (*.xml)':
                zipf = zipfile.ZipFile(filename, 'w')
                zipf.write(self.docpath, file_base)
                for (path, name) in [(content_path, 'content.xml'),
                                     (metadata_path, 'metadata.xml')]:
                    zipf.write(path, name)
                    os.remove(path)

                zipf.close()
            self.statusBar().showMessage('Exported annotations to file %s.'
                                                                    % filename)

    def slot_change_note(self):
        """
        Slot to add or edit note. Replaces current note display in
        annotationSourceTextEdit and annotationWidget with the new note.
        """
        self.ui.annotationSourceDockWidget.show()
        self.ui.actionAnnotationSource.setChecked(True)
        uid = self.ui.documentWidget.ImgLabel.current_uid
        if (self.displayed_uid != -1 and self.displayed_uid != -2):
            text = unicode(self.ui.annotationSourceTextEdit.toPlainText())
            self.current_note.text = text
        self.current_note = self.ui.documentWidget.ImgLabel.notes[uid]
        self.ui.annotationSourceTextEdit.setText(self.current_note.text)
        self.ui.annotationSourceDockWidget.setWindowTitle('Note %d'
                                                        % self.current_note.uid)
        self.ui.annotationDockWidget.setWindowTitle('Note %d'
                                                        % self.current_note.uid)
        self.slot_force_compile()

    def slot_remove_note(self):
        """
        Removes note along with all its files. If the  current note is being
        replaced, blank annotationSourceTextEdit and annotationWidget.
        """
        uid = self.ui.documentWidget.ImgLabel.closest_id
        #print 'Current note: %d' % self.ui.documentWidget.ImgLabel.current_uid
        self.ui.documentWidget.ImgLabel.notes[uid].remove_files()
        self.ui.documentWidget.ImgLabel.notes[uid].remove_png()
        #print 'Main remove note %d' % uid
        if self.ui.documentWidget.ImgLabel.current_uid == uid:
            self.ui.annotationSourceTextEdit.setText('')
            white_pix = QtGui.QPixmap()
            white_pix.fill()
            self.ui.annotationWidget.ImgLabel.setPixmap(white_pix)
            self.ui.documentWidget.ImgLabel.displayed_uid = -2
            self.ui.documentWidget.ImgLabel.current_uid = -2
            self.ui.annotationSourceDockWidget.setWindowTitle('')
            self.ui.annotationDockWidget.setWindowTitle('')
        del self.ui.documentWidget.ImgLabel.notes[uid]
        self.ui.documentWidget.update_image()

    def slot_hide_controls(self):
        """ Slot to hide controls properly and avoid recursion. """
        if self.ui.controlsWidget.isVisible():
            self.ui.actionControls.setChecked(True)
        if self.ui.annotationDockWidget.isHidden():
            self.ui.actionControls.setChecked(False)

    def slot_hide_annotation(self):
        """ Slot to hide annotation properly and avoid recursion. """
        if self.ui.annotationDockWidget.isVisible():
            self.ui.actionAnnotation.setChecked(True)
        if self.ui.annotationDockWidget.isHidden():
            self.ui.actionAnnotation.setChecked(False)

    def slot_hide_annotation_source(self):
        """ Slot to hide annotation source properly and avoid recursion. """
        if self.ui.annotationSourceDockWidget.isVisible():
            self.ui.actionAnnotationSource.setChecked(True)
        if self.ui.annotationSourceDockWidget.isHidden():
            self.ui.actionAnnotationSource.setChecked(False)

    def slot_prev_page(self):
        """ Slot to go to the previous page. """
        self.ui.pageSpinBox.setValue(self.ui.pageSpinBox.value() - 1)

    def slot_next_page(self):
        """ Slot to go to the next page. """
        self.ui.pageSpinBox.setValue(self.ui.pageSpinBox.value() + 1)

    def slot_scale(self, event):
        """ Slot to change the scale. """
        if event == 0:
            self.ui.scaleSpinBox.setEnabled(True)
            self.ui.documentWidget.set_scale(self.ui.scaleSpinBox.value())
        else:
            self.ui.scaleSpinBox.setEnabled(False)
            self.ui.documentWidget.fit_to_width_or_height(event)

    def slot_force_compile(self):
        """ Slot to force compilation through the compileButton. """
        self.old_text = ''
        self.slot_compile_annotation()

    def slot_compile_annotation(self):
        """
        Slot to compile the current annotation by changing annotationWidget's
        ImgLabel's Pixmap to the updated one.
        """
        text = unicode(self.ui.annotationSourceTextEdit.toPlainText())
        if (self.old_text != text and
            self.ui.documentWidget.ImgLabel.current_uid  != -2):
            self.old_text = text
            self.current_note.remove_png()
            self.current_note.text = text
            self.current_note.update()
            self.displayed_uid = self.current_note.uid
            self.ui.annotationWidget.ImgLabel.setPixmap(
                                            self.current_note.icon)

    def slot_show_search_widget(self):
        self.ui.searchDockWidget.show()
        self.ui.searchWidget.searchLineEdit.selectAll()
        self.ui.searchWidget.searchLineEdit.setFocus()

    def keyPressEvent(self, event):
        if self.docpath != '':
            if (event.matches(QtGui.QKeySequence.Find) or
                                            event.key() == QtCore.Qt.Key_Slash):
                self.slot_show_search_widget()
            elif event.key() == QtCore.Qt.Key_Escape:
                self.ui.searchDockWidget.hide()

    def resizeEvent(self, event):
        """ Slot to adjust widgets when MainWindow is resized. """
        if self.ui.scaleComboBox.currentIndex() == 1:
            self.ui.documentWidget.fit_to_width_or_height(1)
        elif self.ui.scaleComboBox.currentIndex() == 2:
            self.ui.documentWidget.fit_to_width_or_height(2)

    def closeEvent(self, event):
        """
        On close, cleanup files.
        """
        for note in self.ui.documentWidget.ImgLabel.notes.values():
            note.remove_files()
            note.remove_png()
        self.current_note.remove_files()
        self.current_note.remove_png()
        if self.rmdoc:
            os.remove(self.docpath)
        try:
            os.rmdir(TMPDIR)
        except OSError:
            #print 'Directory %s could not be removed. It could be non-empty.' % TMPDIR
            pass
