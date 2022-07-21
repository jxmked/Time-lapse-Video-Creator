#! /usr/bin/env python3
# -*- coding UTF-8 -*-

# I don't know if this is driver or not
# I just think so that this is a driver. Hahaha

from os import system
from os.path import isfile
from atexit import register

class Driver:
    logs = []
    
    # No Error Raising During Runtime
    __noRaise = False
    
    # Print all errors caught before exiting
    __noExitError = False
    
    def __init__(self, name):
        """
        This would get package name from sub class.
        A package name should be able to play sound from CLI
        """
        if not isinstance(name, str):
            self.addLog("Package name should be a valid string", "error")
            
            if not self.__noRaise:
                raise Exception("Error from %s" % __file__)
        
        # Testing...
        if system("%s &> /dev/null" % name) != 0:
            self.addLog("Package name does not recognize by your system", "error")
            
            if not self.__noRaise:
                raise Exception("Error from %s" % __file__)
            
        
        self.__pkgName = name
        
        register(self.__onExitError)
    
    def setSounds(self, soundList):
        if not isinstance(soundList, list):
            self.addLog("setSound only accepts an list/array. '%s' given" % type(soundList), "error")
            
            if not self.__noRaise:
                raise Exception("Error from %s" % __file__)
            
        
        notExisting = []
        
        for k, v in soundList:
            if not isfile(v):
                notExisting.append("  %s" % v)
        
        if len(notExisting) > 0:
            self.addLog("Audio file does not exists.\n'%s'" % ("\n".join(notExisting)), "error")
            
            if not self.__noRaise:
                raise Exception("Error from %s" % __file__)
        
    def playSound(self, soundPath, args=None):
        if not isfile(soundPath):
            self.addLog("File '%s' not exists" % soundPath, "error")
            
            if not self.__noRaise:
                raise Exception("Error from %s" % __file__)
        
        cmd = [self.__pkgName]
        
        if not args == None:
            if isinstance(args, list):
                cmd.extend(args)
            elif isinstance(args, str):
                cmd.append(str)
            elif isinstance(args, int):
                cmd.append(args)
            else:
                self.addLog("No handler for arguments", "error")
        
        # Print nothing
        cmd.append("&> /dev/null")
        
        system(" ".join(cmd))
    
    # Error and stats handlers and flags #
    
    def addLog(message, state):
        self.logs.append({
            "message" : message,
            "state" : state
        })
    
    def getLogs(self):
        return self.logs
    
    def noRaise(self):
        self.__noRaise = True
    
    def noExitError(self):
        self.__noExitError = True
    
    def __onExitError(self):
        if self.__noExitError:
            return None
        
        for k, v in self.getLogs():
            print("%s -> %s" % (k, v["state"]))
            print("%s" % v["message"])
            print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")