#! /usr/bin/env python3
# -*- coding UTF-8 -*-
# 
# @Package Name TLVC (Time Lapse Video Creator)
# 
# Main Controller

#from __includes__.notification import Notification
from __includes__.failsafe import Failsafe
from __includes__.command import Command
from __includes__.timer import Timer as T
from __includes__.StorageManager import StorageManager
#from __includes__.audio import Audio

class Controller(Command):
    cmd : Command = Command()
    execute = cmd.execute
    
    fuck = True
    def __init__(self, name=None) -> None:
        
        #print(type(self.execute))
        self.fs : Failsafe = T()
        