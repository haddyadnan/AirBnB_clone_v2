#!/usr/bin/python3

"""Write a Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers"""

from fabric.api import *
import os

env.hosts = ["3.238.197.104", "3.238.204.66"]
env.user = "ubuntu"

def do_deploy(archive_path):
    """ distribute archive to web servers """
    if (os.path.isfile(archive_path) is False):
        return False

    try:
        file_a = archive_path.split("/")[-1]
        new_folder = ("/data/web_static/releases/" + file_a.split(".")[0])
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(new_folder))
        run(f"sudo tar -xzf /tmp/{file_a} -C {new_folder}")
        run(f"sudo rm /tmp/{file_a}")
        run(f"sudo mv {new_folder}/web_static/* {new_folder}/")
        run(f"sudo rm -rf {new_folder}/web_static")
        run('sudo rm -rf /data/web_static/current')
        run(f"sudo ln -s {new_folder} /data/web_static/current")
        print("New version deployed")
        return True
    except:
        return False
