sed -e s/`grep 'VERSION = ' ~/Programming/python/notorius/src/window.py | cut -d '%' -f 3`/\'`date +"%y%m%d-%H%M"`\'/ ~/Programming/python/notorius/src/window.py > ~/Programming/python/notorius/src/window_v.py
mv ~/Programming/python/notorius/src/window_v.py ~/Programming/python/notorius/src/window.py
