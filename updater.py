import subprocess
import os
import urllib2
import hashlib


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
        
        Add any commandline arguments you need here separated by a comma and encloded in single quotes
        List of arguments available at https://wiki.guildwars2.com/wiki/Command_line_arguments
            
            E.g.: arguments = ['-clientport 80', '-maploadinfo']
        """
        self.arguments = []

    def check_for_updates(self):
        dll_path = self.game_path + 'bin64/d3d9.dll'
        dll_exists = os.path.isfile(dll_path)
        if dll_exists:
            existing_md5 = self._calculate_md5(dll_path)
            if existing_md5 != self._original_md5():
                print 'ArcDPS is out of date'
                # TODO: implement file backups
                self._update_arcdps()
            else:
                print 'ArcDPS is up to date'
                self._run_gw2()
        else:
            print 'Unable to find d3d9.dll from current game path'

    def _update_arcdps(self):
        # TODO: implement updating
        pass

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
