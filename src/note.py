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

""" Note. """

import os
import datetime
import subprocess
from PyQt4 import QtGui

from constants import *

class Note(object):
    """
    Note handles the creation and compilation of notes.
    """
    def __init__(self, text = None, preamble = PREAMBLE, compiler = COMPILER,
                 page = 1, pos = None, uid = -1):
        self.filename = self.generate_filename()
        self.icon = QtGui.QPixmap()

        self.text = text
        self._preamble = preamble
        self.compiler = compiler
        self.page = page
        self.pos = pos
        self.uid = uid
        self.cdate = datetime.datetime.now()
        #self.cdate.replace(microsecond = 0)
        self.mdate = self.cdate

        self.tex_source = u''

    @property
    def preamble(self):
        return self._preamble
    @preamble.setter
    def preamble(self, preamble):
        self._preamble = preamble
        #self.ImageLabel = preamble
        self.update()

    def generate_filename(self):
        """
        Generates a random filename with extension .note.tex.
        Returns the filename.
        """
        exists = True
        while exists:
            filename = os.path.join(TMPDIR,
                                    str(randint(0, 999999)) + ".note.tex")
            try:
                open(filename, 'w')
                exists = False
            except IOError:
                exists = True
        self.filename = filename
        return filename

    def generate_file(self):
        """
        Generates the file on which the source will be written.
        Returns True if successful, False otherwise.
        """
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
        """
        Compiles the note tex file.
        Returns True if successful, False otherwise.
        """
        #print 'Generating dvi/pdf/ps'
        try:
            subprocess.call([self.compiler, "--interaction=nonstopmode",
                             "-output-directory", TMPDIR,
                             self.filename], stdout=subprocess.PIPE)
            return True
        except OSError:
            print 'You do not have %s installed!' % self.compiler
            return False

    def generate_png(self):
        """
        Generates the png of the note and its bordered version.
        Returns True if successful, False otherwise.
        """
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

        dvipng_cmd = ["dvipng", "-x", "1500", "-Q", "17", "-T", "tight",
                            "--follow", "-o", filename_png, filename_ext]
        dvipng_cmd_b = ["dvipng", "-x", "1500", "-Q", "17", "-T", "tight",
                            "--follow", "-o", filebase + 'border.png',
                            filename_ext]
        imagemagick_cmd  = ["convert", "-trim", "-density",
                                "%fx%f" % (1.5*DPI_X, 1.5*DPI_Y),
                                filename_ext, filename_png]
        imagemagick_cmd_b  = ["convert", "-bordercolor", "white", "-border",
                             "10x10",
                             #"-bordercolor", "grey", "-border", "2x2",
                             filename_png, filebase + 'border.png']
        if ext == 'dvi':
            try:
                subprocess.call(dvipng_cmd, stdout=subprocess.PIPE)
                subprocess.call(dvipng_cmd_b, stdout=subprocess.PIPE)
                return True
            except OSError:
                print 'You do not have dvipng installed!'
                print 'Falling back on ImageMagick'
                try:
                    subprocess.call(imagemagick_cmd, stdout=subprocess.PIPE)
                    subprocess.call(imagemagick_cmd_b, stdout=subprocess.PIPE)
                    return True
                except OSError:
                    print 'You do not have ImageMagick installed!'
                    return False
        elif (ext == 'pdf') or (ext == 'ps'):
            try:
                subprocess.call(imagemagick_cmd, stdout=subprocess.PIPE)
                subprocess.call(imagemagick_cmd_b, stdout=subprocess.PIPE)
                return True
            except OSError:
                print 'You do not have ImageMagick installed!'
                return False


    def generate_source(self):
        """
        Generates the note tex source file.
        Returns True if successful, False otherwise.
        """
        #print 'Generating source'
        tex_source  = self.preamble  + "\n"
        tex_source += '\pagestyle{empty}' + "\n"
        tex_source += "\\begin{document}\n"
        tex_source += "\\noindent\n"
        tex_source += self.text
        tex_source += "\n"+ '\end{document}'
        self.tex_source = tex_source

    def remove_files(self):
        """
        Removed auxiliary files: aux, log, tex, pdf/ps/dvi.
        """
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
                #print 'File %s was already removed.' % filename
                pass

    def remove_png(self):
        """
        Removes the png file and its bordered version.
        """
        #print 'Removing png'
        for ext in ['png', 'border.png']:
            filename = self.filename.rstrip('tex') + ext
            try:
                os.remove(filename)
            except OSError:
                #print 'File %s was already removed.' % filename
                pass

    def update(self):
        """
        Updates the note_pix QPixmap with the updated note.
        """
        #print 'Updating note %s' % self.uid
        self.generate_source()
        if self.generate_file():
            if self.generate_from_tex():
                if self.generate_png():
                    self.remove_files()
                    self.icon.load(self.filename.rstrip('tex') + 'png')

