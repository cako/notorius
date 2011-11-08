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
is no integration between the two yet. There is also no way to keep track of
annotations.

Requirements
------------
* python 2.6
* pyqt4
* python-popper-qt4

Installation
------------
Once you've got the python libraries, simply run main.py.

[img1]: http://i.imgur.com/OSsXu.png
