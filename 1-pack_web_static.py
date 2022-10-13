#!/usr/bin/python3

"""
Write a Fabric script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB Clone repo
"""
from fabric.api import local
from datetime import datetime


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
