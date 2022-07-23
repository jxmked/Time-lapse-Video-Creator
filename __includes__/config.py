#!/usr/bin/env python3
# -*- coding UTF-8 -*-

# @Package Name TLVC (Time Lapse Video Creator)

# Configuration JSON file Parser

from json import loads, JSONDecodeError
from os.path import join, isfile
from StorageManager import StorageManager

class Config(object):
    configName : str = "Config.json"
    
    def __init__(self, ncfg : bool = None):
        
        conf : object = None
        self.setting : object = {}
        self.myConfig : object = {}
        
        # Check Config File Existence
        if isfile(join(self.__root__, self.configName)):
            
            # Load JSON Text from file
            with open(self.configName, "r") as fopen:
                try:
                    conf = loads(fopen.read())
                    
                    # Global Config
                    self.setting : object = conf.get("setting")
                    
                    # Do we have class object config?
                    if not ncfg:
                        # Object Properties
                        self.myConfig : object = conf.get(self.__class__.__name__)
                    
                    # Init Storage Manager
                    super().__init__()
                    
                    # We're good
                    return None
                except JSONDecodeError:
                    pass
            
        # Not existing or failed to parse
        print("-+" * 8, end="-\n")
        print("Error in config file: %s" % self.configName)
        exit("Cannot start.")
    
