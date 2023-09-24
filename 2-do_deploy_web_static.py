#!/usr/bin/python3
"""
Fabfile to handle deployment of files to remote servers
"""
import os
from datetime import datetime
from fabric.api import local, env, put, run

# list of servers
env.hosts = ["100.26.142.104", "54.237.24.119", "34.229.255.253"]


def do_deploy(archive_path):
    """
    Sends archive to all web servers
    """
    # if the archive file at path doesn't exist
    if not os.path.exists(archive_path):
        return False

    try:

        archive_name = os.path.basename(archive_path)

        # upload file from local to remote servers /tmp/ dir
        tmp_arch_path = "/tmp/" + archive_name
        put(archive_path, tmp_arch_path)

        # create the directory to unarchive to on servers
        archive_name_no_ext = archive_name.split('.')[0]
        unarchive_dir = "/data/web_static/releases/" + archive_name_no_ext
        run("mkdir -p " + unarchive_dir)

        # uncompress archive into unarchive_dir
        run("tar -xzf " + tmp_arch_path + " -C " + unarchive_dir)

        # delete the archive from /tmp/ dir on servers
        run("rm -f " + tmp_arch_path)

        # move all the content from inner web_static dir
        # into outer and delete the empty inner dir
        inner_dir = unarchive_dir + "/web_static"
        run("rsync -a " + inner_dir + "/* " + unarchive_dir)
        run("rm -rf " + inner_dir)

        # delete and re-establish symlink to /data/web_static/current/ dir
        run("rm -rf /data/web_static/current")
        run("ln -s " + unarchive_dir + " " + "/data/web_static/current")

        return True

    except Exception:
        return False
