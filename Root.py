#!/usr/bin/env python3
# -*- coding UTF-8 -*-
# 
# @Package Name TLVC (Time Lapse Video Creator)
# 
# Root contains global in-class method

#from __includes__.notification import Notification
from __includes__.Logging import writeLog 
from __includes__.failsafe import Failsafe
from __includes__.timer import Timer
from __includes__.StorageManager import StorageManager
from __includes__.envres import envRes
from __includes__.command import Command

class Root:
    
    def __init__(self):
        self.__root__ = envRes.get("ROOT")
        self.logger = writeLog
        self.envRes = envRes
        
        self.failsafe = Failsafe
        self.timer = Timer
        self.storage_manager = StorageManager()
        #self.notif = Notification
        
        self.cmd = Command()
        self.execute = self.cmd.execute
    
        pass