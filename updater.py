import subprocess
import os
import urllib
import urllib2
import hashlib
from shutil import copyfile


class ArcDpsUpdater:
    def __init__(self):
        self.file = 'Gw2-64'  # Executable Name
        self.game_path = 'C:\\Guild Wars 2\\'  # Executable Path

        """
        *** Mandatory URI paths ***
        
        DON'T CHANGE THESE UNLESS ARC DOES!
        """
        self.md5_uri = 'https://www.deltaconnected.com/arcdps/x64/d3d9.dll.md5sum'
        self.d3d9_uri = 'https://www.deltaconnected.com/arcdps/x64/d3d9.dll'
        self.bt_uri = 'https://www.deltaconnected.com/arcdps/x64/buildtemplates/d3d9_arcdps_buildtemplates.dll'

        """
        *** Command line arguments ***
        
        Add any commandline arguments you need here separated by a comma and enclosed in single quotes
        List of arguments available at https://wiki.guildwars2.com/wiki/Command_line_arguments
            
            E.g.: arguments = ['-clientport 80', '-maploadinfo']
        """
        self.arguments = []

    def check_for_updates(self):
        d3d9_path = self.game_path + 'bin64/d3d9.dll'
        d3d9_backup_path = self.game_path + 'bin64/d3d9.dll.bak'
        bt_path = self.game_path + 'bin64/d3d9_arcdps_buildtemplates.dll'
        bt_backup_path = self.game_path + 'bin64/d3d9_arcdps_buildtemplates.dll.bak'
        dll_exists = os.path.isfile(d3d9_path)
        if dll_exists:
            existing_md5 = self._calculate_md5(d3d9_path)
            if existing_md5 != self._original_md5():
                print 'ArcDPS is out of date'
                copyfile(d3d9_path, d3d9_backup_path)
                copyfile(bt_path, bt_backup_path)
                self._update_arcdps(d3d9_path, bt_path)
            else:
                print 'ArcDPS is up to date'
                self._run_gw2()
        else:
            self._update_arcdps(d3d9_path, bt_path)

    def _update_arcdps(self, d3d9path, btpath):
        d3d9_file = urllib.URLopener()
        d3d9_file.retrieve(self.d3d9_uri, d3d9path)
        bt_file = urllib.URLopener()
        bt_file.retrieve(self.bt_uri, btpath)
        print 'Completed ArcDPS install'
        self._run_gw2()

    def _run_gw2(self):
        self._launch_application(self.arguments) if self.arguments is not None and len(
            self.arguments) < 1 else self._launch_application(self.arguments)

    def _launch_application(self, arguments):
        print 'Launching game...'
        path = self.game_path + self.file + '.exe {}'.format(" ".join(arguments))
        return subprocess.Popen(path)

    def _calculate_md5(self, fname):
        return hashlib.md5(open(fname, 'rb').read()).hexdigest()

    def _original_md5(self):
        response = urllib2.urlopen(self.md5_uri).read()
        return response.split(' ', 1)[0]
