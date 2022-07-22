#! /usr/bin/env python3
# -*- coding UTF-8 -*-

# @Package Name TLVC (Time Lapse Video Creator)

# I don't know if this is driver or not
# I just think so that this is a driver. Hahaha

from os import system
from os.path import isfile
from atexit import register

class Driver(object):
    logs = []
    
    # No Error Raising During Runtime
    __noRaise = False
    
    # Print all errors caught before exiting
    __noExitError = False
    __SoundList = []
    
    def __init__(self):
        try:
            self.validExitCode
        except AttributeError:
            self.addLog("No valid exit code to look up from subclass", "error")
            
            if not self.__noRaise:
                raise Exception("No valid exit code to look up from subclass")
        pass
    
    def setPackage(self, name):
        """
        This would get package name from sub class.
        A package name should be able to play sound from CLI
        """
        if not isinstance(name, str):
            self.addLog("Package name should be a valid string", "error")
            
            if not self.__noRaise:
                raise Exception("Package name should be a valid string")
        
        # Testing...
        if system("%s &> /dev/null" % name) not in self.validExitCode:
            self.addLog("Package name does not recognize by your system", "error")
            
            if not self.__noRaise:
                raise Exception("Package name does not recognize by your system.\nPackage Name: %s" % name)
        
        # Package Name or Sub Package Name
        self.__pkgName = name
        
        register(self.__onExitError)
    
    def audioList(self, soundList):
        if len(soundList) <= 0:
            self.addLog("audioList cannot be an empty list/array", "error")
            
            if not self.__noRaise:
                raise Exception("audioList cannot be an empty list/array")
        
        if not isinstance(soundList, list):
            self.addLog("audioList only accepts an list/array. '%s' given" % type(soundList), "error")
            
            if not self.__noRaise:
                raise Exception("audioList only accepts an list/array. '%s' given" % type(soundList))
        
        notExisting = []
        
        self.__SoundList = soundList
        
        for v in soundList:
            if not isfile(v):
                notExisting.append("%s" % v)
        
        if len(notExisting) > 0:
            self.addLog("Audio file does not exists.\n    %s" % ("\n    ".join(notExisting)), "error")
            
            if not self.__noRaise:
                raise Exception("Audio file does not exists. [%s]" % (", ".join(notExisting)))
        
    def sound(self, soundPath, args=None):
        if soundPath not in self.__SoundList:
            self.addLog("File '%s' not exists on sound list" % soundPath, "error")
            
            if not self.__noRaise:
                raise Exception("File '%s' not exists on sound list" % soundPath)
        
        cmd = [self.__pkgName, soundPath]
        
        if not args == None:
            if isinstance(args, list):
                cmd.extend(args)
            elif isinstance(args, str):
                cmd.append(args)
            elif isinstance(args, int):
                cmd.append(args)
            else:
                self.addLog("No handler for arguments", "error")
        
        # Print nothing
        cmd.append("&> /dev/null")
        
        system(" ".join(cmd))
    
    # Error and stats handlers and flags #
    
    def addLog(self, message, state):
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
        
        for k, v in enumerate(self.getLogs()):
            print("%s -> %s" % (k, v["state"]))
            print("  %s" % v["message"])
            print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
            