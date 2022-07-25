#!/usr/bin/env python3
# -*- coding UTF-8 -*-
#
# @Package Name TLVC (Time Lapse Video Creator)
# 
# Main Object

from argparse import ArgumentParser as AP

#from os import environ
from os.path import dirname
from atexit import register

from __includes__.Logging import Logging as LG
from __includes__.config import Config
from __includes__.StorageManager import StorageManager
from Controller import Controller

class Main(Config, StorageManager, LG):
    
    __root__ = dirname(__file__)
    
    SYS_ENV = "development"
    
    def __init__(self) -> None:
        LG.__init__(self)
        
        Config.__init__(self, "Main")
        StorageManager.__init__(self)
        
        # Storage Manager Methods
        self.setObjectName("Main")
        self.createSystemDirectories()
        self.createDirectories()
        
        
        self.CTRL = Controller.__init__(self)
        self.writeLog("Main", "Hey")
        register(self.printLogs)
        

if __name__ == '__main__':
    Main()