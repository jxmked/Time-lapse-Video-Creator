#!/usr/bin/env python3
# -*- coding UTF-8 -*-
#
# @Package Name TLVC (Time Lapse Video Creator)
#
# Configuration JSON file Parser

from os.path import join
from json import loads, JSONDecodeError

class Config:
    
    configName = "Config.json"
    
    def __init__(self, name=None, ncfg=False) -> None:
        
        conf = {}
        self.setting = {}
        self.myConfig = {}
        self.directories = {}
        self.sys_directories = {}
        
        try:
            # Load JSON Text from file
            
            # fopen : method
            with open(join(self.__root__, self.configName), "r") as fopen:
                conf = loads(fopen.read())
                
                # Global Config
                self.setting = conf.get("setting")
                
                # Set Environment Mode
                self.SYS_ENV = self.setting.get("env_mode", "production")
                
                # Do we have class object config?
                if not ncfg:
                    # Object Properties
                    self.myConfig = conf.get(name)
                    self.directories = self.myConfig.get("directories")
                    self.sys_directories = self.myConfig.get("system_directories")
                    
                return self
            
        
        except JSONDecodeError as EE:
            # Parsing Error
            self.writeLog("Config", "Error Parsing config file", "failed", EE)
        
        except FileNotFoundError as EE:
            # Config File does not exists
            self.writeLog("Config", "Config file does not exists", "error", EE)
            
        exit("Cannot start.")
    
    def getConfig(self):
        return self.myConfig.get("configuration", {})
