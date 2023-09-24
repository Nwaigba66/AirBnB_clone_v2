#!/usr/bin/python3
"""
Fabfile to handle deployment of files to remote servers
"""
import os
from datetime import datetime
from fabric.api import local, env, put, run, runs_once

# list of servers
env.hosts = ["100.26.142.104", "34.229.255.253", "54.237.24.119"]


@runs_once
def do_pack():
    """
    Creates a .tgz archive of web_static/ & stores it in versions/
    """
    try:
        # create dir "versions" if it doesn't exist already
        local("mkdir -p versions")

        # create the name of the archive matching the template:
        # web_static_<year><month><day><hour><minute><second>.tgz
        current_time = datetime.now()
        date_stamp = current_time.strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_" + date_stamp
        full_archive_path = "versions/" + archive_name + ".tgz"

        # create the archive
        local("tar -czvf " + full_archive_path + " web_static")

        return full_archive_path

    except Exception:
        return None


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


def deploy():
    """
    Creates a .tgz archive and deploys it to remote servers
    """
    archive_path = do_pack()

    if archive_path:
        return do_deploy(archive_path)
    else:
        return False
