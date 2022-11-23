#! /usr/bin/env python3
# -*- coding UTF-8 -*-
# 
# @Package Name TLVC (Time Lapse Video Creator)
# 
# Logging System to keep track of errors or something you want

from __includes__.envres import envRes

class Logging(object):
    # Global Variable
    __logs__ = envRes.get("logging")
    
    def __init__(self):
        pass
    
    @staticmethod
    def writeLog(name, msg, state=None, EE=None):
        state = (state if state else "log")
        EE = (EE if EE else None)
        
        Logging.__logs__.append({
            "message" : msg,
            "object" : name,
            "state" : state,
            "exception" : EE
        })
        
    def printLogs(self ) -> None:
        if len(self.__logs__) < 1:
            return None
        
        print("Logs: ")
        print("-+" * 9, end="-\n")
        
        for k, v in enumerate(self.__logs__):
            print("%s : %s" % (v.get("object", "Null"), v.get("state", "Null")))
            print("Message: %s" % v.get("message", "Null"))
            
            if v.get("exception"):
                print("Exception caught: %s" % v.get("exception"))
            
            print("-+" * 9, end="-\n")
        
    

# We can import only 
def writeLog(name, msg, state=None, EE=None):
    Logging.writeLog(name, msg, state, EE)