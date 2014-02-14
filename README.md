etmv
====

Enjoy the m...ing Video!

ETMV disables the linux screensaver (+dpms), if a fullscreen (flash) window is open!


## Installation ##

ETMV requires [Python 2](http://www.python.org/download/releases/2.7.6/),
[ooxcb](https://github.com/samurai-x/ooxcb) and [psutil](https://code.google.com/p/psutil/).

Make sure to start etmv with your desktop environment (e.g. `.xinitrc`):

    # Arch Linux
    python2 etmv.py
    # Ubuntu / Debian etc.
    python etmv.py


## Useage ##

By default you don't require any of these options:

```
usage: etmv.py [-h] [--interval INTERVAL] [--name NAME] [--display DISPLAY]
               [--auth AUTH]

Disable dpms and screensaver, if the currently active window is a fullscreen
flash window or matches a few criterias.

  -h, --help           show this help message and exit
  --interval INTERVAL  The interval to check if there is a matching window to
                       either enable or disable the screensaver.
  --name NAME          Disable the screensaver, if the currently active
                       fullscreen window belongs to this process (fnmatching
                       supported). This option can be used multiple times.
                       Defaults to: chromium, opera, firefox, mplayer, mpv and
                       vlc.
  --display DISPLAY    The X display to connect to, if not specified the
                       DISPLAY environment variable will be used.
  --auth AUTH          Custom authentication cookie used to connect to the
```



