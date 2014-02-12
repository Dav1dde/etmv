import sys
import time
import traceback
import subprocess

import psutil

import ooxcb
from ooxcb.protocol import xproto
from ooxcb.contrib.ewmh import ewmh_get_window_name

# Requires ooxcb and psutil

# TODO nice commandline options


# Disable the screensaver for any video which is currently fullscreen and in foreground
FULLSCREEN_ENOUGH = False
# If above is false, disable for these programs which are in fullscreen (all lower case!)
FULLSCREEN_NAMES = ['chromium', 'mplayer', 'firefox', 'vlc']


_NET_WM_STATE_FULLSCREEN = 352


def enable_screensaver():
    subprocess.check_call(['xset', '+dpms'])
    subprocess.check_call(['xset', 's', 'on'])

def disable_screensaver():
    subprocess.check_call(['xset', '-dpms'])
    subprocess.check_call(['xset', 's', 'off'])


def is_fullscreen(window):
    states = window.get_property('_NET_WM_STATE', 'ATOM').reply().value.to_atoms()
    for atom in states:
        if 'fullscreen' in atom.name.lower():
            return True

def get_pid(window):
    return int(window.get_property('_NET_WM_PID', 'CARDINAL').reply().value[0])


def check(screen):
    window = screen.get_active_window()
    #return is_fullscreen(window)

    if is_fullscreen(window):
        if FULLSCREEN_ENOUGH:
            return True

        name = ewmh_get_window_name(window).strip()

        if name in ['plugin-container', 'Microsoft Silverlight']:
            return True

        try:
            pid = get_pid(window)
        except ValueError:
            return False

        process = psutil.Process(pid)
        return process.name.lower() in FULLSCREEN_NAMES

    return False


def main():
    def log():
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                    limit=None, file=sys.stderr)

    conn = ooxcb.connect()
    screen = conn.setup.roots[conn.pref_screen]
    activated = False

    while True:
        try:
            if check(screen):
                if not activated:
                    disable_screensaver()
                activated = True
            elif activated:
                    enable_screensaver()
                    activated = False
        except KeyboardInterrupt:
            break
        except:
            log()

        time.sleep(180)


if __name__ == '__main__':
    main()