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

""" Constants. """

import getpass
import os
import subprocess
from random import randint
from platform import system as systemplat

PREAMBLE = '''\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
'''

USERNAME = getpass.getuser()

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
        if DPI_X >= 500 or DPI_Y >= 500:
            DPI_X = DPI_Y = 96
    except OSError:
        DPI_X = DPI_Y = 96
else:
    DPI_X = DPI_Y = 96


COMPILER = 'pdflatex'
try:
    PROC = subprocess.Popen([COMPILER, "--version"], stdout=subprocess.PIPE)
    PROC.stdout.close()
except OSError:
    COMPILER = 'latex'

if PLATFORM == 'Windows':
    COMPILER = 'latex'

DIR = os.path.dirname(__file__)

if PLATFORM == 'Linux' or PLATFORM == 'MacOS':
    TMPDIR = os.getenv('TMPDIR')
    if not TMPDIR:
        TMPDIR = '/tmp/'
elif PLATFORM == 'Windows':
    TMPDIR = os.getenv('TEMP')
    if not TMPDIR:
        TMPDIR = DIR
else:
    TMPDIR = DIR

TMPDIR_WHILE = TMPDIR
while os.path.isdir(TMPDIR_WHILE):
    TMPDIR_WHILE = os.path.join(TMPDIR, 'notorius-%s' % str(randint(0, 999)))
TMPDIR = TMPDIR_WHILE
os.mkdir(TMPDIR)
