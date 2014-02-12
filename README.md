etmv
====

Enjoy the m...ing Video!

ETMV disables the linux screensaver, if a fullscreen (flash) window is open!


## Installation ##

ETMV requires [Python 2](http://www.python.org/download/releases/2.7.6/),
[ooxcb](https://github.com/samurai-x/ooxcb), [psutil](https://code.google.com/p/psutil/).

Installation dependencies on Arch Linux:

    pacman -S python2 python2-pip
    sudo pip2 install ooxcb psutil


Installation dependencies on Ubuntu/Debian:

    sudo apt-get install python
    sudo apt-get install python-pip
    sudo pip install ooxcb psutil

Installation dependencies others:

    I bet you can figure that out!


Make sure to start etmv when starting your desktop environment (e.g. `.xinitrc`):

    # Arch
    python2 etmv.py
    # Ubuntu
    python etmv.py



