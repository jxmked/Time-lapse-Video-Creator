#!/usr/bin/env python3
# -*- coding UTF-8 -*-
# 
# @Package Name TLVC (Time Lapse Video Creator)
#
# Execute commands

from os import system
import subprocess
from __includes__.envres import envRes
from __includes__.model.config import Config

class Command(Config):
    
    config:dict = {
        "priority" : {
            "mode" : True,
            "level" : "normal" # low | normal | high | realtime | abovenormal | belownormal
        },
        "set_threads" : {
            "mode" : False,
            "count" : 12 # Threads Count. 
        },
        "overwrite" : True,
        "benchmark" : {
            # "mode" : False,
            "level" : "basic" # basic, all
        },
        "logging" : {
            # "mode" : True,
            "level" : "info" # trace, debug, verbose, info (default), warning, error, fatal, panic, quiet 
        }
    }
    
    """Logging Level -> ffmpeg -loglevel %
    trace, debug, verbose, info, warning, error, fatal, panic
    """
    __LOGGING_LEVELS__:list[str] = ["trace", "debug", "verbose", "info", "warning", "error", "fatal", "panic", "quiet"]
    
    inputList:list[str] = []
    output:str = ""
    title:str = ""
    cmdLog:list[str] = [] # args, state
    
    def __init__(self) -> None:
        # super().__init__()

        self.ENV:str|None = envRes.get("ENV")
        
        
    def getLogs(self) -> list[str]:
        return self.cmdLog
    
    def setInput(self, arr:list[str]|str|bool) -> None:
        if isinstance(arr, list):
            for item in arr:
                self.inputList.append("-i \"%s\"" % item)
        
        elif isinstance(arr, str):
                self.inputList.append("-i \"%s\"" % arr)
        
        elif isinstance(arr, bool):
            if arr == False:
                self.inputList = []
        
    def setOutput(self, out:str) -> None:
        self.output = "\"%s\"" % out
    
    def setTitle(self, txt:str) -> None:
        self.title:str = txt
    
    def execute(self, arr:list[str], run:int|bool|None=None) -> None:
        assert isinstance(arr, list), "Command must be an Array"
        
        run = (True if run in [None, 1, True] else False)
        
        cfg:dict[str, dict[str, str|bool|int]|str|bool|int] = self.config
        config:dict = self.config 

        match config.get("benchmark", {}).get("level", ):
            case "basic":
                arr.insert(0, "-benchmark")
               
            case "all":
                arr.insert(0, "-benchmark_all")    
                
            case _:
                print(f"No available method for benchmark {config.get('benchmark', {}).get('level')}")
        

        arr.insert(0, "-nostdin")
        arr.insert(0, "-hide_banner")
        
        if not config.get("logging", {}).get('level') in self.__LOGGING_LEVELS__:
            print("Invalid Logging Level") # Errors

        arr.insert(0, f"-loglevel {config.get('logging', {}).get('level', 'info')}")
        
        if config.get("set_threads", {}).get("mode", False) and config.get('set_threads', {}).get('count', False) is not False:
            arr.insert(0, f"-threads {config.get('set_threads', {}).get('count')}")
        
        arr.insert(0, ("-y" if cfg["overwrite"] else "-n"))
        
        arr.insert(0, "ffmpeg")
        
        if len(self.inputList) > 0:
            arr.insert(1, " ".join(self.inputList))
            
        if self.output:
            arr.append(self.output)
            
            self.inputList = []
            self.output = ""
        

        # Set Priority
        if config.get("priority", {}).get("mode", False):
            AVAILABLE_LEVELS:dict[str, int] = {
                # My config
                "low": 20,
                "normal": 0,
                "high": -10,
                "realtime": -15,
                "abovenormal": -20,
                "belownormal": 10
            }


            match envRes.get("ENV"):
                case "linux":
                    level:str = config.get("priority", {}).get("level", "")
                    arr.insert(0, f"nice -{AVAILABLE_LEVELS[config.get('priority', {}).get('level', 'normal')]}")

                case "powershell":
                    print("Currently Priority is not available in Powershell or Command Prompt")
                    # [{/low | /normal | /high | /realtime | /abovenormal | /belownormal}]
                    # 20 0 -10 -15 -20 10
                    # arr.insert(0, f"start 'ffmpeg' {config.get('priority', {}).get('level', 'normal')} /wait /b ")
                    

        query:str = " ".join(arr)
        
        print()
        print("-+" * 10, end="-\n")
        if self.title:
            print("Name: %s" % self.title)
            self.title = ""
            print("--" * 10)
        
        print(query)
        print("-+" * 10, end="-\n")
        
        res:int = 0

        if self.ENV == "powershell" or self.ENV == "cmd":
            out:subprocess.Popen[bytes] = subprocess.Popen(query, stdout=subprocess.PIPE)
            out.communicate()[0]
            res = out.returncode

        elif self.ENV == "linux":
            res = (system(query) if run else 0)
        
        else:
            raise Exception("Failed to execute: Unknown Environment")

        state:str|None = None
        if res == 0 and run == True:
            state = "success"
        elif run is False:
            state = "failed"
        else:
            state = "error"
        
        # self.writeLog("Command", "Query: %s" % query, state)
        # self.cmdLog.append(( state, query ))
        
        assert res == 0, "\nCurrent Command:\n\t%s" % query
        
    



