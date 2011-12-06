#!/bin/bash
sudo apt-get install texlive-latex-base
sudo apt-get install python-qt4
sudo apt-get install python-pip
temp=(python-qt4-dev python-sip-dev libpoppler-qt4-dev g++)
rem=()
for lib in ${temp[*]}
do
    if echo `sudo apt-get install -y $lib` | grep -q "is already the newest version"
    then
        echo "$lib was already installed. Will not remove it."
    else
        echo "Installed $lib."
        rem=(${rem[*]} $lib)
    fi 
done

sudo pip install python-poppler-qt4

wget --no-check-certificate  "https://github.com/cako/notorius/tarball/master " -O - | tar xz
mv cako-notorius-*/* $HOME/.notorius
sudo ln -s $HOME/.notorius/src/main.py /usr/bin/notorius
sudo ln -s $HOME/.notorius/img/note64.png /usr/share/icons/notorius.png
sudo cp $HOME/.notorius/notorius.desktop /usr/share/applications

for lib in ${rem[*]}
do
    sudo apt-get remove $lib
done
