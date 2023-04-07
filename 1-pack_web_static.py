#!/usr/bin/python3
"""[summary]
"""
from fabric.api import local
from datetime import datetime
import time


def do_pack():
    """compress a file for deployment
    Returns:
    type]: [description]
    """
    clocktime = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
    try:
        local('mkdir -p versions')
        localtar = local(
            'tar -czvf versions/web_static_{}.tgz web_static/'.format(
                clocktime), capture=True)
        return (localtar)
    except Exception:
        return None
