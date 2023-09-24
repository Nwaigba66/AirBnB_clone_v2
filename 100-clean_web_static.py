#!/usr/bin/python3
"""
Fabfile to cleanup of out of date archives
"""
import os
from datetime import datetime
from fabric.api import local, env, run, runs_once

# list of servers
env.hosts = ["100.26.142.104", "54.237.24.119"]


@runs_once
def clean_local(number):
    """
    Deletes the out-of-date archives locally
    """
    list_of_archives = local("ls -1 versions", capture=True).split()

    # delete the uneeded archives
    if number == 0:
        archives_to_delete = list_of_archives[:-1]
    else:
        archives_to_delete = list_of_archives[:-number]

    for archive in archives_to_delete:
        local("rm -f versions/" + archive)
        # print("versions/" + archive + " to be deleted")


def clean_remote(number):
    """
    Deletes the out-of-date archives remotely
    """
    list_of_archives = run("ls -1 /data/web_static/releases").split()

    # tailor the list of archives to include only web_static_
    tailored_list = []
    for archive in list_of_archives:
        if "web_static_" in archive:
            tailored_list.append(archive)
    list_of_archives = tailored_list

    print("Remote Machine")
    # delete the uneeded archives
    if number == 0:
        archives_to_delete = list_of_archives[:-1]
    else:
        archives_to_delete = list_of_archives[:-number]

    for archive in archives_to_delete:
        run("rm -rf /data/web_static/releases/" + archive)
        # print("/data/web_static/releases/" + archive + " to be deleted")


def do_clean(number=0):
    """
    Deletes out-of-date archives locally and remotely
    """
    # local machine
    clean_local(number)

    # remote machines
    clean_remote(number)
