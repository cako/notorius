README
======

Introduction
------------

Introducing notorius!

![notorius][img1]
[img1]: http://i.imgur.com/qeYCo.png

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

###### Debian-based distros

Get the deb for you architecture:
[32-bit](https://github.com/downloads/cako/notorius/notorius-0.1_i386.deb),
[64-bit](https://github.com/downloads/cako/notorius/notorius-0.1_amd64.deb). 

###### Other distros

Get a TeX distribution and ImageMagick. Then download the appropriate binary:
[32-bit](https://github.com/downloads/cako/notorius/notorius.32),
[64-bit](https://github.com/downloads/cako/notorius/notorius.64) and run it!

### Windows

Get a LaTeX distribution, for example, [MikTeX](http://miktex.org/2.9/setup).
Download the
[installer](https://github.com/downloads/cako/notorius/notorius0.1-setup.exe)
and run it!

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
