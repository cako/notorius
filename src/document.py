#!/usr/bin/python
# -*- coding: UTF-8 -*-
#==============================================================================#
#                                                                              #
# Copyright 2011 Carlos Alberto da Costa Filho                                 #
#                                                                              #
# This file is part of Fermat.                                                 #
#                                                                              #
# Fermat is free software: you can redistribute it and/or modify               #
# it under the terms of the GNU General Public License as published by         #
# the Free Software Foundation, either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
# Fermat is distributed in the hope that it will be useful,                    #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                 #
# GNU General Public License for more details.                                 #
#                                                                              #
# You should have received a copy of the GNU General Public License            #
# along with this program. If not, see <http://www.gnu.org/licenses/>.         #
#                                                                              #
#==============================================================================#

import os
#import djvu
import popplerqt4
from zipfile import ZipFile
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from constants import *

class Document(object):
    """
    The Document class creates a unified interface to obtain Qt objects from
    different document file formats. It provides, amongst other things, QImages
    of pages QStrings of text, etc.
    """

    def __init__(self, filepath):
        if filepath:
            self.filepath = filepath
            self._ext = self._extension_of(self.filepath)
            if self._ext == 'pdf':
                self._doc = self._load_pdf(self.filepath)
            elif self._ext == 'djvu':
                self._doc = self._load_djvu(self.filepath)
            elif self._ext == 'okular':
                self._doc = self._load_okular(self.filepath)
            else:
                print 'Not a supported filetype.'
                self._doc = None

    def _extension_of(self, filepath):
        """ Returns the lowercase extension of a file. """
        return os.path.splitext(filepath)[1][1:].lower().strip()

    def _load_pdf(self, filepath):
        """
        Loads a PDF file and sets the correct RenderHint.
        Returns a popplerqt4.Document object if successful, returns None if
        not.
        """
        doc = popplerqt4.Poppler.Document.load(filepath)
        if doc is not None:
            doc.setRenderHint(doc.Antialiasing)
            doc.setRenderHint(doc.TextAntialiasing)
            doc.setRenderHint(doc.TextHinting)
            print 'Loaded PDF file %s.' % filepath
        else:
            print 'Not a valid PDF file.'
        return doc

    def _load_djvu(self, filepath):
        print 'Djvu not supported yet.'
        return None

    def _load_okular(self, filepath):
        """
        Loads an Okular file. The Okular file is unpacked and the function
        returns the embedded PDF or Djvu file.
        """
        zipf = ZipFile(filepath, 'r')
        zipf.extractall(TMPDIR)
        docname =  [ filename for filename in zipf.namelist() if (
                            self._extension_of(filename) != 'xml' ) ][0]
        ext = self._extension_of(docname)
        docpath = os.path.join(TMPDIR, docname)
        if ext == 'pdf':
            doc = self._load_pdf(docpath)
        elif ext == 'djvu':
            doc = self._load_djvu(docpath)
        elif ext == 'okular':
            doc = self._load_okular(self.filepath)
        else:
            print 'Not a supported filetype.'
            doc = None
        if doc is not None:
            print 'Loaded Okular file %s.' % filepath
        return doc

a = Document('/home/cako/Desktop/GPY001008.pdf')
b = Document('/home/cako/Desktop/test.okular')
