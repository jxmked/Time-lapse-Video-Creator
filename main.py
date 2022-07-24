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

from __includes__.config import Config
from __includes__.StorageManager import StorageManager

#from Controller import Controller

class Main(Config, StorageManager):
    
    __root__ = dirname(__file__)
    _logs = []
    SYS_ENV = "development"
    
    def __init__(self) -> None:
        # Call before exiting
        register(self.__printLogs)
        
        Config.__init__(self)
        StorageManager.__init__(self)
        
        # Storage Manager Methods
        self.setObjectName("Main")
        self.createSystemDirectories()
        self.createDirectories()
        
        
        print(self.sys_directories)
        print(self.directories)
        # Extend Controller
       # self.CTRL = Controller(self)
        
    
    def writeLog(self, objName, msg, state, EE=None) -> None:
        if not EE:
            EE = "Null"
            
        self._logs.append({
            "message" : msg,
            "state" : state,
            "exception" : EE,
            "name" : objName
        })
    
    def __printLogs(self) -> None:
        if len(self._logs) < 1:
            return
        
        print("\nError caught during runtime.")
        print("-+" * 9, end="-\n")
        
        for k, v in enumerate(self._logs):
            print("%s: %s" % (v["name"], v["state"]))
            print("Message: %s" % v["message"])
            print("Caught: %s" % v["exception"])
            
            print("-+" * 9, end="-\n")
        
    


if __name__ == '__main__':
    Main()