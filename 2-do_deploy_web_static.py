#!/usr/bin/python3
"""
A Fabric script that distributes an archive to my web servers
"""
import os
from datetime import datetime
from fabric.api import *

env.hosts = ["100.25.180.98", "100.26.133.223"]
env.user = "ubuntu"


def do_pack():
    """
        This returns the archive path if archive has generated correctly.
    """

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    arch_f_path = "versions/web_static_{}.tgz".format(date)
    t_gzip_archive = local("tar -cvzf {} web_static".format(arch_f_path))

    if t_gzip_archive.succeeded:
        return arch_f_path
    else:
        return None


def do_deploy(archive_path):
    """
        Distribute archive.
    """
    if os.path.exists(archive_path):
        # Extract the archive to /data/web_static/releases/<filename without extension>/
        archived_filename = archive_path[9:]
        new_version = "/data/web_static/releases/" + archived_filename[:-4]
        archived_filename = "/tmp/" + archived_filename
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(new_version))
        run("sudo tar -xzf {} -C {}/".format(archived_filename,
                                             new_version))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(new_version,
                                                new_version))
        run("sudo rm -rf {}/web_static".format(new_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(new_version))

        print("New version deployed!")
        return True

    return False
