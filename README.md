README
======

Introduction
------------

Introducing notorius!

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


Installation
------------
### Linux

Get a TeX distribution and ImageMagick. Then download the appropriate binary:
32-bit (soon),
[64-bit](https://github.com/cako/notorius/blob/master/build/notorius.64), and run it!

### Windows

Get a LaTeX distribution, for example, [MikTeX](http://miktex.org/2.9/setup).
Download the
[installer](https://github.com/cako/notorius/blob/master/build/notorius0.2-setup.exe)
and run it! You can also use the program without installing it, download the
binary [here](https://github.com/cako/notorius/blob/master/build//notorius.exe).


Screenshot
----------

![notorius][img1]
[img1]: http://i.imgur.com/qeYCo.png
>>>>>>> ec83657dc045ac0e4f2143b9331ffd05802c20cf

Screenshot
----------

![notorius][img1]
[img1]: http://i.imgur.com/qeYCo.png

Source
------

In order to run the program with Python instead of a binary, make sure you have
the right dependencies first.
These are the ``PyQt4`` and ``popplerqt4``. In Ubuntu 12.04 or later, they are
both available through the package manager in packages ``python-qt4`` and
``python-poppler-qt4``.
Once this is done, ``cd`` into the ``src`` folder and run ``python main.py``.


License
------- 
Copyright 2013 Carlos Alberto da Costa Filho

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
