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
from __includes__.Controller import Controller

class Main(Config):
    
    __root__ : str = dirname(__file__)
    _logs : list = []
    
    def __init__(self) -> None:
        register(self.__printLogs)
        super().__init__(True)
        
        # Extend Controller
        self.CTRL : Controller = Controller(self)
        
        
       # print(self.fuck)
    def writeLog(self, 
            objName : str, 
            msg : str, 
            state : str, 
            EE : str
        ) -> None:
        
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