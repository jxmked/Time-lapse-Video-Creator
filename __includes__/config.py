#!/usr/bin/env python3
# -*- coding UTF-8 -*-

# Configuration JSON file Parser

from json import loads, dumps
import os


class Config:
    isLoaded = False
    
    configPath = ""
    configName = "Config.json"
    
    __config = {}
    
    def __init__(self):
        if self.isLoaded:
            return None
        
        self.__getJson()
        self.__createDirectories()
    
    def getMyConfig(self, obj):
        name = obj.__class__.__name__
        return self.__config[name]
    
    def getDirectories(self):
        return self.__config["directories"]
        
    def __createDirectories(self):
        conf = self.__config
        
        # Check `directories` key in json
        
        if not "directories" in conf:
            print("Invalid JSON file.")
            print("Cannot start")
            exit("error")
        
        # Create Existing Directories From Json File
        for k, v in conf.get("directories").items():
            try:
                os.makedirs(v)
            except FileExistsError:
                pass
    
    def __getJson(self):
        
        # Check Config File Existence
        if not os.path.exists(self.configName):
            print("-+" * 8, end="-\n")
            print("Config file `%s` does not exists." % self.configName)
            print("Cannot start")
            exit("Error")
        
        # Load JSON Text from file
        with open(self.configName, "r") as fopen:
            try:
                self.__config = loads(fopen.read())
            except JSONDecodeError:
                print("Errro Parsing Config File.")
                print("Cannot start.")
                exit("error")
                
            