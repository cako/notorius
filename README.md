README
======

Introduction
------------

Introducing notorius!

![notorius][img1]

Annotating PDF files is hard. There are a few
options, but none of them are good enough for the
technically inclined. Most PDF annotators use either
ASCII text or free form tools.

The question arises: How does one annotate a PDF
with LaTeX notation. The answer is, you simply
don't.

I've written a couple of scripts (first
[annotate_pdf](https://github.com/cako/annotate_pdf) and then
[pdfnoter](https://github.com/cako/pdfnoter)) but they were half-assed and hard
to use. So I decided I'd write a full-blown PDF reader. This is my meager
attempt at doing so.

The project is very much a work in progress, but key parts have already been
implemented. So far it can open PDF files and add, edit and remove annotations.
Exporting annotations is done using Okular's xml format. Meaning, export it as
a .okular, and open it in Okular! Reading is not yet implemented.


Requirements
------------
* [python 2.6](http://www.python.org/getit/releases/2.6/)
* [PyQt4](http://www.riverbankcomputing.co.uk/software/pyqt/download)
* [python-popper-qt4](http://code.google.com/p/python-poppler-qt4/)
* [latex](http://www.latex-project.org/)

One of the following:

* [dvipng](http://sourceforge.net/projects/dvipng/)
* [imagemagick](http://www.imagemagick.org/script/index.php) (necessary if you
want to use `pdflatex` or `pslatex` (which are required for the `tikz` package)


Installation
------------
Once you've got the python libraries, simply run main.py. Following are the
installation instructions for the libraries.

### Ubuntu

First, you'll need a LaTeX installation, if you don't already have one.

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

After the installation, the `-dev` libraries and `g++` can be uninstalled:

    sudo apt-get remove python-qt4-dev python-sip-dev libpoppler-qt4-dev g++
    sudo apt-get autoremove

[img1]: http://i.imgur.com/98h5k.png

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
