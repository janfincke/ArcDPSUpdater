import _winreg
import hashlib
import os
import subprocess
import urllib
import urllib2
from shutil import copyfile

from time import sleep


class ArcDpsUpdater:
    def __init__(self):
        self.md5_uri = 'https://www.deltaconnected.com/arcdps/x64/d3d9.dll.md5sum'
        self.d3d9_uri = 'https://www.deltaconnected.com/arcdps/x64/d3d9.dll'
        self.bt_uri = 'https://www.deltaconnected.com/arcdps/x64/buildtemplates/d3d9_arcdps_buildtemplates.dll'
        try:
            settings_file = open('settings.txt', 'rb')
            with settings_file as f:
                settings = ''.join(f.readline())
        except:
            settings = ''
        self.arguments = settings

        registry_path = r'Software\\ArenaNet\\Guild Wars 2'
        try:
            key_64 = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, registry_path, 0,
                                     _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY)
            value_64 = _winreg.QueryValueEx(key_64, "Path")[0]
            self.file = value_64
            self.game_path = self.file.split(os.path.basename(self.file))[0]
        except WindowsError as e:
            try:
                key_32 = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, registry_path, 0,
                                         _winreg.KEY_READ | _winreg.KEY_WOW64_32KEY)
                value_32 = _winreg.QueryValueEx(key_32, "Path")[0]
                self.file = value_32
                self.game_path = self.file.split(os.path.basename(self.file))[0]
            except WindowsError as e:
                print 'Could not get registry keys for game path!'
                raw_input('Press any key to continue...')
                raise SystemExit

        if not os.path.isdir(self.game_path):
            print 'Unable to find game path!'
            raw_input('Press any key to continue...')
            raise SystemExit

        if not os.path.isfile(self.file):
            print 'Unable to find game executable!'
            raw_input('Press any key to continue...')
            raise SystemExit

    def check_for_updates(self):
        d3d9_path = self.game_path + 'bin64\\d3d9.dll'
        d3d9_backup_path = self.game_path + 'bin64\\d3d9.dll.bak'
        bt_path = self.game_path + 'bin64\\d3d9_arcdps_buildtemplates.dll'
        bt_backup_path = self.game_path + 'bin64\\d3d9_arcdps_buildtemplates.dll.bak'
        dll_exists = os.path.isfile(d3d9_path)
        if dll_exists:
            existing_md5 = self._calculate_md5(d3d9_path)
            if existing_md5 != self._original_md5():
                print 'ArcDPS is out of date.'
                sleep(1)
                copyfile(d3d9_path, d3d9_backup_path)
                copyfile(bt_path, bt_backup_path)
                self._update_arcdps(d3d9_path, bt_path)
            else:
                print 'ArcDPS is up to date!'
                self._run_gw2()
        else:
            self._update_arcdps(d3d9_path, bt_path)

    def _update_arcdps(self, d3d9path, btpath):
        print 'Downloading d3d9.dll...'
        d3d9_file = urllib.URLopener()
        d3d9_file.retrieve(self.d3d9_uri, d3d9path)
        print 'Downloading d3d9_arcdps_buildtemplates.dll...'
        bt_file = urllib.URLopener()
        bt_file.retrieve(self.bt_uri, btpath)
        print 'Completed ArcDPS install!'
        self._run_gw2()

    def _run_gw2(self):
        sleep(1)
        self._launch_application(self.arguments)

    def _launch_application(self, arguments):
        path = self.file + ' {}'.format(arguments)
        return subprocess.Popen(path)

    def _calculate_md5(self, fname):
        return hashlib.md5(open(fname, 'rb').read()).hexdigest()

    def _original_md5(self):
        response = urllib2.urlopen(self.md5_uri).read()
        return response.split(' ', 1)[0]
