#!/usr/bin/python3
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ['100.25.180.98', '100.26.133.223']


def deploy():
    """Create and distribute an archive to a web server."""
    arch_path = do_pack()
    if arch_path is None:
        return False
    return do_deploy(arch_path)

def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    d_time = datetime.utcnow()
    arch_file = "versions/web_static_{}{}{}{}{}{}.tgz".format(d_time.year,
                                                         d_time.month,
                                                         d_time.day,
                                                         d_time.hour,
                                                         d_time.minute,
                                                         d_time.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(arch_file)).failed is True:
        return None
    return arch_file


def do_deploy(arch_path):
    """Distributes an archive to a web server.

    Args:
        arch_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(arch_path) is False:
        return False
    file = arch_path.split("/")[-1]
    name = file.split(".")[0]

    if put(arch_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True
