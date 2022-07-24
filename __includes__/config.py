#!/usr/bin/env python3
# -*- coding UTF-8 -*-
#
# @Package Name TLVC (Time Lapse Video Creator)
#
# Configuration JSON file Parser

from json import loads, JSONDecodeError
from os.path import join

class Config(object):
    
    configName : str = "Config.json"
    
    def __init__(self, ncfg=False) -> None:
        
        conf = {}
        self.setting = {}
        self.myConfig = {}
        
        try:
            # Load JSON Text from file
            
            # fopen : method
            with open(join(self.__root__, self.configName), "r") as fopen:
                conf = loads(fopen.read())
                
                # Global Config
                self.setting = conf.get("setting")
                    
                # Do we have class object config?
                if not ncfg:
                    # Object Properties
                    self.myConfig = conf.get(self.__class__.__name__)
                    
                # We're good
                return None
            
        
        except JSONDecodeError as EE:
            # Parsing Error
            self.writeLog("Config", "Error Parsing config file", "failed", EE)
        
        except FileNotFoundError as EE:
            # Config File does not exists
            self.writeLog("Config", "Config file does not exists", "error", EE)
            
        exit("Cannot start.")
    
