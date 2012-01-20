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

#import window_ui
from preamble_window import PreambleWindow
from offset_window import OffsetWindow
from document_widget import DocumentWidget
from search_widget import SearchWidget
from annotation_widget import AnnotationWidget
from note import Note
from constants import *
from icons import *


from PyQt4 import QtCore, QtGui, QtXml, uic
from xml.etree import ElementTree as xml

VERSION = '0.1.%s' %'120120-1915'

class MainWindow(QtGui.QMainWindow):
    """ Main Window Class """

    add_windows_trigger = QtCore.pyqtSignal(list)

    def highlight_buttons(self, event):
        if self.previousPageButton.underMouse():
            self.previousPageButton.setFlat(False)
        else:
            self.previousPageButton.setFlat(True)

        if self.nextPageButton.underMouse():
            self.nextPageButton.setFlat(False)
        else:
            self.nextPageButton.setFlat(True)

    def __init__(self, parent=None, document = None):
        """ Initialize MainWindow """
        QtGui.QMainWindow.__init__(self, parent)
        uic.loadUi(os.path.join(DIR, 'window.ui'), self)
        self.setWindowIcon(QtGui.QIcon(':img/note64.png'))
        self._preamble = PREAMBLE
        self.offset = 0
        self.docpath = ''
        self.rmdoc = False
        self.displayed_uid = -1
        self.okular_notes = []

        # Toolbar icons
        self.actionOpen.setIcon(QtGui.QIcon.fromTheme("document-open"))
        self.actionExport.setIcon(QtGui.QIcon.fromTheme("document-save-as"))
        self.actionQuit.setIcon(QtGui.QIcon.fromTheme("application-exit"))

        self.actionPreambleEditor.setIcon(QtGui.QIcon.fromTheme(
                                                        "preferences-other"))

        self.actionAbout.setIcon(QtGui.QIcon.fromTheme("help-about"))

        # Toolbar connections
        self.connect(self.actionOpen, QtCore.SIGNAL("triggered()"),
                     self.slot_gui_open)
        self.connect(self.actionExport, QtCore.SIGNAL("triggered()"),
                     self.slot_export)
        self.connect(self.actionQuit, QtCore.SIGNAL("triggered()"),
                     self.close)

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

        self.connect(self.actionAbout, QtCore.SIGNAL("triggered()"),
                     self.slot_about)

        # Document controls
        if PLATFORM == 'Windows':
            self.previousPageButton.setText('Previous')
            self.nextPageButton.setText('Next')
            font_metrics = QtGui.QFontMetrics(QtGui.QFont())
            size_p = font_metrics.size(QtCore.Qt.TextSingleLine, 'Previous')
            size_n = font_metrics.size(QtCore.Qt.TextSingleLine, 'Next')
            self.previousPageButton.setMinimumWidth(size_p.width() + 10)
            self.nextPageButton.setMinimumWidth(size_n.width() + 10)
        else:
            self.previousPageButton.setIcon(QtGui.QIcon.fromTheme("go-previous"))
            self.nextPageButton.setIcon(QtGui.QIcon.fromTheme("go-next"))
        self.controlsWidget.mouseMoveEvent = self.highlight_buttons

        self.offsetWindow = OffsetWindow(self)
        self.connect(self.offsetCheckBox, QtCore.SIGNAL("stateChanged(int)"),
                     self.offsetWindow.slot_open)

        # Search widget
        self.searchWidget = SearchWidget(self.searchDockWidgetContents)
        self.gridLayout_4.addWidget(self.searchWidget, 0, 0, 1, 1)
        self.searchDockWidget.hide()
        self.searchWidget.hide_trigger.connect(self.searchDockWidget.hide)
        self.searchWidget.change_page_trigger.connect(self.pageSpinBox.setValue)
        #self.searchWidget.show_trigger.connect(self.searchDockWidget.show)

        # PDF viewer widget
        self.scrollArea.setMinimumWidth(0)
        self.documentWidget = DocumentWidget(self.scrollArea)
        self.documentWidget.setObjectName("documentWidget")
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.documentWidget.ImgLabel)
        self.connect(self.documentWidget.ImgLabel, QtCore.SIGNAL("dropped"),
                                                                self.slot_load_dropped)
        self.documentWidget.ImgLabel.change_scale_trigger.connect(self.scaleSpinBox.setValue)

        # Connections for PDF viewer
        self.connect(self.previousPageButton, QtCore.SIGNAL("clicked()"),
                     self.slot_prev_page)
        self.connect(self.nextPageButton, QtCore.SIGNAL("clicked()"),
                     self.slot_next_page)
        self.connect(self.pageSpinBox, QtCore.SIGNAL("valueChanged(int)"),
                     self.documentWidget.change_page)
        self.connect(self.scaleSpinBox, QtCore.SIGNAL("valueChanged(double)"),
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
                                                 self.current_note.icon)
        self.annotationWidget.setObjectName("annotationWidget")

        self.scrollAreaAnnotation.setBackgroundRole(QtGui.QPalette.Light)
        self.scrollAreaAnnotation.setWidget(self.annotationWidget.ImgLabel)
        self.actionAnnotation.toggle()

        # Connections for Annotation widget
        self.connect(self.compileButton, QtCore.SIGNAL("clicked()"),
                     self.slot_force_compile)

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
        self.documentWidget.ImgLabel.toggle_source_trigger.connect(
                                        self.actionAnnotationSource.toggle)
        self.actionAnnotationSource.toggle()

        # Connections for Annotation Source Widget
        self.timer = QtCore.QTimer()
        self.timer.start(3500)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.slot_compile_annotation)
        self.old_text = ''

        # Preamble editor
        self.preambleEditorWindow = PreambleWindow(self)
        self.connect(self.actionPreambleEditor, QtCore.SIGNAL("triggered()"),
                     self.preambleEditorWindow.slot_open)

        # Status bar
        self.documentWidget.ImgLabel.set_clipboard_trigger.connect(
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
                                        pg <= self.documentWidget.num_pages ):
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
                        size = self.documentWidget.Document.page(
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
            self.nextPageButton.setEnabled(True)
            self.previousPageButton.setEnabled(True)
            self.pageSpinBox.setEnabled(True)
            self.offsetCheckBox.setEnabled(True)
            self.offsetCheckBox.setChecked(False)
            self.scaleSpinBox.setEnabled(True)
            self.scaleComboBox.setEnabled(True)
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
                self.documentWidget.load_document(self.docpath)
                loaded = True
                root = xml.parse(os.path.join(TMPDIR, 'metadata.xml')).getroot()
                notes = parse_metadata(root)
                for aux in ['content.xml', 'metadata.xml']:
                    os.remove(os.path.join(TMPDIR, aux))
                self.documentWidget.ImgLabel.notes = notes
                self.documentWidget.update_image()
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
                    self.documentWidget.ImgLabel.notes = parse_metadata(root)
                    self.documentWidget.update_image()
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
                self.documentWidget.load_document(self.docpath)
                self.setWindowTitle('Notorius - %s' %os.path.basename(filename))
                loaded = True

            if loaded:
                self.pageSpinBox.setValue(1)
                self.pageSpinBox.setMinimum(-self.documentWidget.num_pages + 1)
                self.pageSpinBox.setMaximum(self.documentWidget.num_pages)
                self.scaleComboBox.setCurrentIndex(0)
                self.maxPageLabel.setText("of %d" %
                                          self.documentWidget.num_pages)
                self.actionExport.setEnabled(True)
                self.searchWidget.documentWidget = self.documentWidget
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
            notes = self.documentWidget.ImgLabel.notes
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
                size = self.documentWidget.Document.page(note.page).pageSizeF()
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
        self.annotationSourceDockWidget.show()
        self.actionAnnotationSource.setChecked(True)
        uid = self.documentWidget.ImgLabel.current_uid
        if (self.displayed_uid != -1 and self.displayed_uid != -2):
            text = unicode(self.annotationSourceTextEdit.toPlainText())
            self.current_note.text = text
        self.current_note = self.documentWidget.ImgLabel.notes[uid]
        self.annotationSourceTextEdit.setText(self.current_note.text)
        self.annotationSourceDockWidget.setWindowTitle('Note %d'
                                                        % self.current_note.uid)
        self.annotationDockWidget.setWindowTitle('Note %d'
                                                        % self.current_note.uid)
        self.slot_force_compile()

    def slot_remove_note(self):
        """
        Removes note along with all its files. If the  current note is being
        replaced, blank annotationSourceTextEdit and annotationWidget.
        """
        uid = self.documentWidget.ImgLabel.closest_id
        #print 'Current note: %d' % self.documentWidget.ImgLabel.current_uid
        self.documentWidget.ImgLabel.notes[uid].remove_files()
        self.documentWidget.ImgLabel.notes[uid].remove_png()
        #print 'Main remove note %d' % uid
        if self.documentWidget.ImgLabel.current_uid == uid:
            self.annotationSourceTextEdit.setText('')
            white_pix = QtGui.QPixmap()
            white_pix.fill()
            self.annotationWidget.ImgLabel.setPixmap(white_pix)
            self.documentWidget.ImgLabel.displayed_uid = -2
            self.documentWidget.ImgLabel.current_uid = -2
            self.annotationSourceDockWidget.setWindowTitle('')
            self.annotationDockWidget.setWindowTitle('')
        del self.documentWidget.ImgLabel.notes[uid]
        self.documentWidget.update_image()

    def slot_hide_controls(self):
        """ Slot to hide controls properly and avoid recursion. """
        if self.controlsWidget.isVisible():
            self.actionControls.setChecked(True)
        if self.annotationDockWidget.isHidden():
            self.actionControls.setChecked(False)

    def slot_hide_annotation(self):
        """ Slot to hide annotation properly and avoid recursion. """
        if self.annotationDockWidget.isVisible():
            self.actionAnnotation.setChecked(True)
        if self.annotationDockWidget.isHidden():
            self.actionAnnotation.setChecked(False)

    def slot_hide_annotation_source(self):
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

    def slot_force_compile(self):
        """ Slot to force compilation through the compileButton. """
        self.old_text = ''
        self.slot_compile_annotation()

    def slot_compile_annotation(self):
        """
        Slot to compile the current annotation by changing annotationWidget's
        ImgLabel's Pixmap to the updated one.
        """
        text = unicode(self.annotationSourceTextEdit.toPlainText())
        if (self.old_text != text and
            self.documentWidget.ImgLabel.current_uid  != -2):
            self.old_text = text
            self.current_note.remove_png()
            self.current_note.text = text
            self.current_note.update()
            self.displayed_uid = self.current_note.uid
            self.annotationWidget.ImgLabel.setPixmap(
                                            self.current_note.icon)

    def keyPressEvent(self, event):
        if self.docpath != '':
            if (event.matches(QtGui.QKeySequence.Find) or
                                            event.key() == QtCore.Qt.Key_Slash):
                self.searchDockWidget.show()
                self.searchWidget.searchLineEdit.selectAll()
                self.searchWidget.searchLineEdit.setFocus()
            elif event.key() == QtCore.Qt.Key_Escape:
                self.searchDockWidget.hide()

    def resizeEvent(self, event):
        """ Slot to adjust widgets when MainWindow is resized. """
        if self.scaleComboBox.currentIndex() == 1:
            self.documentWidget.fit_to_width_or_height(1)
        elif self.scaleComboBox.currentIndex() == 2:
            self.documentWidget.fit_to_width_or_height(2)

    def closeEvent(self, event):
        """
        On close, cleanup files.
        """
        for note in self.documentWidget.ImgLabel.notes.values():
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
