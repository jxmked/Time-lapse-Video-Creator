#!/usr/bin/env python3
# -*- coding UTF-8 -*-
# 
# @Package Name TLVC (Time Lapse Video Creator)
# 
# Root contains global in-class method

#from __includes__.notification import Notification
from __includes__.model.Logging import writeLog 
from __includes__.model.failsafe import Failsafe
from __includes__.model.timer import Timer
from __includes__.model.StorageManager import StorageManager
from __includes__.envres import envRes
from __includes__.model.command import Command


import os

class Root:
    
    def __init__(self):
        self.ENV:str|None = envRes.get("ENV")
        self.__root__:str = envRes.get("ROOT") or "."
        self.logger = writeLog
        self.envRes = envRes
        
        self.failsafe = Failsafe
        self.timer = Timer
        self.timers:dict[str, int] = {}
        self.storage_manager = StorageManager()
        
        #self.notif = Notification
        
        self.cmd = Command()
        self.execute = self.cmd.execute
        
        """
        Output resources
        
        - Duplicated frames removed
        - Trimmed and processed Audio
        - Final Output
        """
        self.processed = os.path.join(self.__root__, "__Resources__")
        
        pass
