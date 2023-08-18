import sys

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

import os
import stat
import glob


class CustomBuildHook(BuildHookInterface):

    def initialize(self, version, build_data):
        # chmod +x
        for f in glob.glob("./bin/*.sh"):
            st = os.stat(f)
            os.chmod(f, st.st_mode | stat.S_IEXEC | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    def finalize(self, version, build_data, artifact_path):
        # post install
        old_target_dir = '/opt/cacheschedconfig'
        try:
            if not os.path.exists(old_target_dir):
                os.makedirs(old_target_dir)
            # sysconfig
            directory = os.path.join(old_target_dir, 'etc', 'sysconfig')
            if not os.path.exists(directory):
                os.makedirs(directory)
            for f in glob.glob("./etc/*"):
                f_base = os.path.basename(f)
                dst = os.path.join(directory, f_base)
                src = os.path.join(sys.prefix, 'etc', 'sysconfig', f_base)
                if os.path.exists(dst):
                    os.remove(dst)
                os.symlink(src, dst)
            # bin
            directory = os.path.join(old_target_dir, 'bin')
            if not os.path.exists(directory):
                os.makedirs(directory)
            for f in glob.glob("./bin/*"):
                f_base = os.path.basename(f)
                dst = os.path.join(directory, f_base)
                src = os.path.join(sys.prefix, 'bin', f_base)
                if os.path.exists(dst):
                    os.remove(dst)
                os.symlink(src, dst)
            # cron
            directory = '/etc/cron.d'
            for f in glob.glob("./cron/*"):
                f_base = os.path.basename(f)
                dst = os.path.join(directory, f_base)
                src = os.path.join(sys.prefix, 'etc', 'cron.d', f_base)
                if os.path.exists(dst):
                    os.remove(dst)
                os.symlink(src, dst)
        except Exception:
            pass
