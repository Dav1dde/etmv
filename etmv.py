#/usr/bin/env python2

import time
import fnmatch
import traceback
import subprocess

try:
    import psutil
except ImportError:
    _HAS_PSUTIL = False
else:
    _HAS_PSUTIL = True

import ooxcb
from ooxcb.util import Mixin
from ooxcb.protocol import xproto
#from ooxcb.protocol import screensaver
from ooxcb.exception import ProtocolException
from ooxcb.contrib.ewmh import ewmh_get_window_name


class ETMVException(Exception):
    pass


def process_name_from_pid(pid):
    if _HAS_PSUTIL:
        try:
            return psutil.Process(pid).name
        except psutil.NoSuchProcess, e:
            raise ETMVException(e.message)

    try:
        return subprocess.check_output(['ps', '-p', str(pid), 'comm=']).strip()
    except subprocess.CalledProcessError, e:
        raise ETMVException(e.message)


_NET_WM_STATE_FULLSCREEN = 352

class WindowMixin(Mixin):
    target_class = xproto.Window

    def is_fullscreen(self):
        ''' Returns True if the Window is in fullscreen mode '''
        repl = self.get_property('_NET_WM_STATE', 'ATOM').reply()
        states = repl.value.to_atoms()
        for atom in states:
            if 'fullscreen' in atom.name.lower():
                return True

    def is_flash(self):
        name = ewmh_get_window_name(self).strip()
        return name in ['plugin-container', 'Microsoft Silverlight']

    def get_pid(self):
        ''' Returns _NET_WM_PID if exists, otherwise 0 '''
        repl = self.get_property('_NET_WM_PID', 'CARDINAL').reply()
        return int(repl.value[0]) if len(repl.value) > 0 else 0

    def get_process_name(self):
        pid = self.get_pid()
        return process_name_from_pid(pid)

WindowMixin.mixin()


class ScreenSaverControl(object):
    DISABLED = 0
    ENABLED = 1

    def __init__(self, connection, fnames=None):
        self.fnames = ['chromium', 'opera', 'firefox', 'mplayer', 'mpv', 'vlc']
        if not fnames is None:
            self.fnames = fnames

        self.connection = connection
        self.screen = connection.setup.roots[connection.pref_screen]
        self.state = ScreenSaverControl.ENABLED

    def run(self, interval=-1):
        if interval <= 0:
            ss = self.connection.core.get_screen_saver().reply()
            interval = (ss.interval-1)/2

        while True:
            self.change_state_if_needed()
            time.sleep(interval)

    def change_state_if_needed(self):
        if self.should_disable():
            if self.state == ScreenSaverControl.ENABLED:
                self.disable_screensaver()
        elif self.state == ScreenSaverControl.DISABLED:
            self.enable_screensaver()

    def should_disable(self):
        current = self.screen.get_active_window()

        if current.is_fullscreen():
            if current.is_flash():
                return True

            try:
                name = current.get_process_name()
            except (ETMVException, ProtocolException):
                return False

            for fn in self.fnames:
                if fnmatch.fnmatch(name, fn):
                    return True
        return False


    # TODO use ooxcb for that, unfortunatly it doesn't support the dpms ext
    def enable_screensaver(self):
        subprocess.check_call(['xset', '+dpms'])
        subprocess.check_call(['xset', 's', 'on'])
        self.state = ScreenSaverControl.ENABLED

    def disable_screensaver(self):
        subprocess.check_call(['xset', '-dpms'])
        subprocess.check_call(['xset', 's', 'off'])
        self.state = ScreenSaverControl.DISABLED


def main():
    import sys
    import argparse

    def log(logfile):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                    limit=None, file=logfile)

    parser = argparse.ArgumentParser(
        description=
            'Disable dpms and screensaver, if the currently active '
            'window is a fullscreen flash window or matches a few criterias.'
    )

    parser.add_argument(
        '--interval', dest='interval',
        type=int, default=-1,
        help='The interval to check if there is a matching window to either '
             'enable or disable the screensaver.'
    )

    parser.add_argument(
        '--name', dest='name',
        action='append', default=None,
        help='Disable the screensaver, if the currently active fullscreen '
             'window belongs to this process (fnmatching supported). '
             'This option can be used multiple times. '
             'Defaults to: chromium, opera, firefox, mplayer, mpv and vlc.'
    )

    parser.add_argument(
        '--display', dest='display',
        default='',
        help='The X display to connect to, if not specified the DISPLAY '
             'environment variable will be used.'
    )

    parser.add_argument(
        '--auth', dest='auth',
        default=None,
        help='Custom authentication cookie used to connect to the display.'
    )

    ns = parser.parse_args()

    connection = ooxcb.connect(ns.display, auth_string=ns.auth)
    ssc = ScreenSaverControl(connection, ns.names)

    try:
        ssc.run(ns.interval)
    except KeyboardInterrupt:
        pass
    except Exception:
        log(sys.stderr)


if __name__ == '__main__':
    main()