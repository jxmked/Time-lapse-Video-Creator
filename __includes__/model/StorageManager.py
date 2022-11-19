#! /usr/bin/env python3
# -*- coding UTF-8 -*-

# @Package Name TLVC (Time Lapse Video Creator)

from os import makedirs
from os.path import isfile, join, isdir
from __includes__.envres import envRes

class StorageManager(object):
    
    directories = {}
    __name__ = None
    
    def __init__(self):
        pass
    
    def setObjectName(self, name):
        self.__name__ = name
    
    def createSystemDirectories(self):
        assets_directory = join("__includes__", "assets", self.__name__)
        
        # Path to System Directories
        for k, v in self.sys_directories.items():
            # This should be a directory and must be existing
            p = join(self.__root__, assets_directory, v)
            self.__create_directory__(p)
            self.sys_directories[k] = p
        
    def createDirectories(self):
        # Path to Accessible Directory
        for k, v in self.directories.items():
            # This should be a directory and must be existing
            p = join(self.__root__, v)
            
            self.__create_directory__(p)
            self.sys_directories[k] = p
        
    def __create_directory__(self, p):
        if not isdir(p) and not isfile(p):
            makedirs(p)
            
        elif isfile(p) and envRes.get("ENV_MODE") in ["development", "debug", "logging"]:
            self.writeLog("StorageManager", '{p} does exists and it is a file', "error")
            
            if envRes.get("ENV_MODE") == "development":
                raise Exception('{p} is already existing but as a file.')
            
        
    