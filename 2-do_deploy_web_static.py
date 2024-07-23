#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers.
"""
from fabric.api import env, put, run
import os

env.hosts = ['100.26.216.113', '34.204.60.227']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path (str): The path to the archive file.

    Returns:
        bool: True if all operations have been done correctly, otherwise False.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Get the file name with extension
        file_name = archive_path.split("/")[-1]
        # Get the file name without extension
        name_no_ext = file_name.split(".")[0]

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/{}".format(file_name))

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
        run("mkdir -p /data/web_static/releases/{}/".format(name_no_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file_name, name_no_ext))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(file_name))

        # Move the contents of the extracted folder to the final location
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name_no_ext, name_no_ext))

        # Delete the extracted folder as it's now empty
        run("rm -rf /data/web_static/releases/{}/web_static".format(name_no_ext))

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name_no_ext))

        print("New version deployed!")
        return True
    except Exception as e:
        return False
