#! /usr/bin/env python3
# -*- coding UTF-8 -*-
# 
# @Package Name TLVC (Time Lapse Video Creator)
# 
# Main Controller

#from __includes__.notification import Notification
from __includes__.Logging import writeLog as log
from __includes__.failsafe import Failsafe
from __includes__.command import Command
from __includes__.timer import Timer as T
from __includes__.StorageManager import StorageManager
#from __includes__.audio import Audio
from argparse import ArgumentParser as AP

class Controller(Command):
    # Main Child Object
    # Class Name: Main
    
    def __init__(self):
        Command.__init__(self)
      #  LG.__init__(self)
        
        log("Controller", "logll")
        print("From Controller")
        print(self.config)
       # self.fs = Failsafe()
       # print(self.__class__.__name__)
        
       # self.execute([])
    
    def 
