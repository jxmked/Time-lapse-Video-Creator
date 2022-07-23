#! /usr/bin/env python3
# -*- coding UTF-8 -*-

# @Package Name TLVC (Time Lapse Video Creator)

from os.path import isfile, join, isdir, makedirs

class StorageManager(object):
    
    
    
    ## Directories should have
    # input -> input
    # resources output -> resource
    
    directories = {}
    
    def __init__(self):
        
        # Path to Accessible Directory
        for k, v in self.myConfig.get("directories").item():
            # This should be a directory and must be existing
            p = join(self.__root__, self.__class__.__name__, v)
            self.createDir(p)
        
    
    def createDir(self, p):
        if not isdir(p) and not isfile(p):
            self.directories[k] = p
            makedirs(p)
            
        if isfile(p):
            raise Exception('{p} is already existing but as a file.')
        
    
