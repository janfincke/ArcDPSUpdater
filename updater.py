import subprocess
import os
import urllib
import urllib2
import hashlib
from shutil import copyfile
from time import sleep


class ArcDpsUpdater:
    def __init__(self):
        settings_file = open('settings.txt', 'rb')
        lines = settings_file.read().splitlines()
        settings = []
        for line in lines:
            try:
                line = line.split('= ', 1)[1]
            except IndexError:
                line = ""
            settings.append(line)
        self.file = settings[1]
        self.game_path = settings[0]
        self.md5_uri = settings[2]
        self.d3d9_uri = settings[3]
        self.bt_uri = settings[4]
        self.arguments = settings[5]

    def check_for_updates(self):
        d3d9_path = self.game_path + '/bin64/d3d9.dll'
        d3d9_backup_path = self.game_path + '/bin64/d3d9.dll.bak'
        bt_path = self.game_path + '/bin64/d3d9_arcdps_buildtemplates.dll'
        bt_backup_path = self.game_path + '/bin64/d3d9_arcdps_buildtemplates.dll.bak'
        
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
        self._launch_application(self.arguments) if self.arguments is not None and len(
            self.arguments) < 1 else self._launch_application(self.arguments)

    def _launch_application(self, arguments):
        path = self.game_path + self.file + '.exe {}'.format(arguments)
        return subprocess.Popen(path)

    def _calculate_md5(self, fname):
        return hashlib.md5(open(fname, 'rb').read()).hexdigest()

    def _original_md5(self):
        response = urllib2.urlopen(self.md5_uri).read()
        return response.split(' ', 1)[0]
