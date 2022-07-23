#! /usr/bin/env python3
# -*- coding UTF-8 -*-

# @Package Name TLVC (Time Lapse Video Creator)

from __includes__.notification import Notification
from __includes__.failsafe import Failsafe
from __includes__.command import Command
from __includes__.timer import Timer
from __includes__.config import Config

class Controller(object):
    
    notif = Notification()

    cmd = Command()
    execute = cmd.execute()
    timer = Timer()
    cfg = Config()
    
    def __init__(self, name):
        self.fs = Failsafe(name)