README
======

Introduction
------------

Introducing notorius!

![notorius][img1]
[img1]: http://i.imgur.com/TxHAd.png

Annotating PDF files is hard. There are a few options, but none of them are good
enough for the technically inclined. Most PDF annotators use either ASCII text
or free form tools.

The question arises: How does one annotate a PDF with LaTeX notation. The answer
is, you simply don't. To repair the situation, I've written Notorius.

Before, I'd written a couple of scripts (first
[annotate_pdf](https://github.com/cako/annotate_pdf) and then
[pdfnoter](https://github.com/cako/pdfnoter)) but they were half-assed and hard
to use. So I decided I'd write a full-blown PDF reader. This is my meager
attempt at doing so.

The project is very much a work in progress, though as of now, it is entirely
functional. You can open PDF, and Okular files, or simply import notes contained
in an XML file on top of an already open PDF. Saving is also done through Okular
archives or XML files.

Requirements
------------
The requirements are below. For platform specific instructions see Installation.

* [Python](http://www.python.org/download/) (versions 2.6 or 2.7)
* [PyQt4](http://www.riverbankcomputing.co.uk/software/pyqt/download)
* [python-poppler-qt4](http://code.google.com/p/python-poppler-qt4/)
* [LaTeX](http://www.latex-project.org/)

One of the following:

* [dvipng](http://sourceforge.net/projects/dvipng/)
* [ImageMagick](http://www.imagemagick.org/script/index.php) (necessary if you
want to use `pdflatex` or `pslatex` (which are required for the `tikz` package,
for example), but currently unavailable for Windows.)


Installation
------------
### Windows

This has been tested with 32-bit Windows XP, but it should work on newer
systems.

Before anything make sure you have a LaTeX distribution. A common one for
Windows is MikTeX, download it from the following website.

[`http://miktex.org/2.9/setup`](http://miktex.org/2.9/setup)

Let's install Python. Download and install the following file.

[`http://python.org/ftp/python/2.7.2/python-2.7.2.msi`](http://python.org/ftp/python/2.7.2/python-2.7.2.msi)

Now, let's install PyQt4. Download and install the following file.

[`http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-Py2.7-x86-gpl-4.8.6-1.exe`](http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-Py2.7-x86-gpl-4.8.6-1.exe)

Finally, to  install python-poppler-qt4, download and install the following
file.

[`https://home.in.tum.de/~lorenzph/python-poppler-qt4/python-poppler-qt4-0.16.2.win32-py2.7-pyqt-4.8.4.exe`](https://home.in.tum.de/~lorenzph/python-poppler-qt4/python-poppler-qt4-0.16.2.win32-py2.7-pyqt-4.8.4.exe)

Now run it! Don't worry about dvipng, it comes with LaTeX.

    C:\Python27\pythonw.exe C:\Path\To\main.py


### Ubuntu

# Automated

For an automated installation, download and run the install script found
[in the downloads](http://dl.dropbox.com/u/3087188/notorius_ubuntu_install.sh).
For the clueless,

    chmod +x notorius_ubuntu_install.sh
    ./notorius_ubuntu_install.sh

Notorius will be in the menu under Applications>Office, but it can also be run
from the command line with

    notorius

# Manual

First, you'll need a LaTeX distribution, if you don't already have one.

    sudo apt-get install texlive-latex-base

Second, you will need PyQt4. If you don't have it, install it with:

    sudo apt-get install python-qt4

Finally, you have to install `python-popper-qt4`. To build it, you will need to
install the following libraries:

    sudo apt-get install python-qt4-dev python-sip-dev libpoppler-qt4-dev g++

Then download it, unpack it, build and install:

    wget http://code.google.com/p/python-poppler-qt4/downloads/detail?name=python-poppler-qt4-0.16.2.tar.gz
    tar xvzf python-poppler-qt4-0.16.2.tar.gz
    cd python-poppler-qt4-0.16.2/
    python setup.py build
    sudo python setup.py install

It can also be installed with
[`pip`](http://www.pip-installer.org/en/latest/index.html):

    sudo pip install python-poppler-qt4

If you want (recommended) install ImageMagick with

    sudo apt-get install imagemagick

After the installation, the `-dev` libraries and `g++` can be uninstalled:

    sudo apt-get remove python-qt4-dev python-sip-dev libpoppler-qt4-dev g++
    sudo apt-get autoremove


License
------- 
Copyright 2011 Carlos Alberto da Costa Filho

This file is part of Notorius.

Notorius is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Notorius is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
