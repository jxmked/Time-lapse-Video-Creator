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

class Root:
    
    logger = writeLog
    envRes = envRes
    
    failsafe = Failsafe
    timer = Timer
    storage_manager = StorageManager()
    #notif = Notification
    
    def __init__(self):
        pass