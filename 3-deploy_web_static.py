#!/usr/bin/python3

"""
Write a Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers
"""
from datetime import datetime
from fabric.api import *
import os

env.hosts = ["3.238.197.104", "3.238.204.66"]
env.user = "ubuntu"


def do_pack():
    """
    Generates a .tgx archive from web_static
    """
    try:
        local("mkdir -p versions")
        fnme = "versions/web_static_"
        fnme = fnme + f"{datetime.now().strftime(('%Y%m%d%H%M%S'))}.tgz"
        archive = local(f"tar -cvzf {fnme} web_static")
        return fnme
    except Exception:
        return None


def do_deploy(archive_path):
    """distribute archive to web servers"""
    if os.path.isfile(archive_path) is False:
        return False

    try:
        file_a = archive_path.split("/")[-1]
        new_folder = "/data/web_static/releases/" + file_a.split(".")[0]
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(new_folder))
        run(f"sudo tar -xzf /tmp/{file_a} -C {new_folder}")
        run(f"sudo rm /tmp/{file_a}")
        run(f"sudo mv {new_folder}/web_static/* {new_folder}/")
        run(f"sudo rm -rf {new_folder}/web_static")
        run("sudo rm -rf /data/web_static/current")
        run(f"sudo ln -s {new_folder} /data/web_static/current")
        print("New version deployed")
        return True
    except Exception:
        return False


def deploy():
    """
    Deploy
    """
    archive_path = do_pack()
    print(archive_path)
    if not archive_path:
        return False
    resp = do_deploy(archive_path)
    return resp
