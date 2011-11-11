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

The project is very much in its infancy, but key parts have already been
implemented. So far it can open PDF files and generate annotations, but there
is no integration between the two. There is also no way to keep track of
annotations.

Requirements
------------
* [python 2.6](http://www.python.org/getit/releases/2.6/)
* [PyQt4](http://www.riverbankcomputing.co.uk/software/pyqt/download)
* [python-popper-qt4](http://code.google.com/p/python-poppler-qt4/)
* [latex](http://www.latex-project.org/)
* [dvipng](http://sourceforge.net/projects/dvipng/)

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

[img1]: http://i.imgur.com/E3vyQ.png
