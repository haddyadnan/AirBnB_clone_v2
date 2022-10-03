#!/usr/bin/python3
# Write a Fabric script that generates a .tgz archive from the contents
# of the web_static folder of your AirBnB Clone repo, using the function

from gzip import FNAME
from fabric.api import local
from datetime import datetime

def do_pack():
    """
    Generates a .tgx archive from web_static
    """
    try:
        local("mkdir -p versions")
        fnme = f"versions/web_static_{datetime.now().strftime(('%Y%m%d%H%M%S'))}.tgz"
        archive = local(f"tar -cvzf {fnme} web_static")
        return fnme
    except:
        return None