sed -e s/`grep 'VERSION = ' ~/Programming/python/notorius/src/window.py | cut -d '%' -f 3`/\'`date +"%y%m%d-%H%M"`\'/ ~/Programming/python/notorius/src/window.py > ~/Programming/python/notorius/src/window_v.py
mv ~/Programming/python/notorius/src/window_v.py ~/Programming/python/notorius/src/window.py
pyuic4 -o src/window_ui.py src/window.ui
pyuic4 -o src/offset_window_ui.py src/offset_window.ui
pyuic4 -o src/preamble_window_ui.py src/preamble_window.ui
rm src/*.pyc
