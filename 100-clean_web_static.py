#!/usr/bin/python3
import os
from fabric.api import *

env.hosts = ['100.25.180.98', '100.26.133.223']


def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        numb (int): The number of archives to keep.

    If numb is 0 or 1, keeps only the most recent archive. If
    numb is 2, keeps the most and second-most recent archives,
    etc.
    """
    numb = 1 if int(numb) == 0 else int(numb)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for j in range(numb)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
