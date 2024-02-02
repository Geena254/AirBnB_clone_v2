#!/usr/bin/python3
"""A module for a Fabric script that generates a .tgz archive."""
from datetime import datetime
from fabric.api import local, runs_once
import os


@runs_once
def do_pack():
    """Generate a .tgz archive from the contents of the web_static folder."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    time_format = datetime.now()
    arch_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        time_format.year,
        time_format.month,
        time_format.day,
        time_format.hour,
        time_format.minute,
        time_format.second
    )
    try:
        print("Packing web_static to {}".format(arch_name))
        local("tar -cvzf {} web_static".format(arch_name))
        size = os.stat(arch_name).st_size
        print("web_static packed: {} -> {} Bytes".format(arch_name, size))
    except Exception:
        output = None
    return output
