#!/usr/bin/env python3


from os import system as cmd
from __includes__.config import Config

class Command:
    
    config = {
        "priority" : {
            "mode" : False,
            "level" : "-20" # -20 <-> 20
        },
        "set_threads" : {
            "mode" : False,
            "count" : 12 # Threads Count. 
        },
        "overwrite" : True,
        "benchmark" : {
            "mode" : False,
            "level" : "basic" # basic, all
        },
        "logging" : {
            "mode" : False,
            "level" : "debug" # trace, debug, verbose, info, warning, error, fatal, panic, quiet 
        }
    }
    
    inputList = []
    output = ""
    title = ""
    cmdLog = [] # args, state
    
    def __init__(self):
        pass
    def getLogs(self):
        return self.cmdLog
    
    def setInput(self, arr):
        if isinstance(arr, list):
            for item in arr:
                self.inputList.append("-i \"%s\"" % item)
        
        elif isinstance(arr, str):
                self.inputList.append("-i \"%s\"" % arr)
        
        elif isinstance(arr, bool):
            if arr == False:
                self.inputList = []
        
    def setOutput(self, out):
        self.output = "\"%s\"" % out
    
    def setTitle(self, txt):
        self.title = txt
    
    def execute(self, arr, run=None):
        assert isinstance(arr, list), "Command must be an Array"
        
        run = (True if run in [None, 1, True] else False)
        
        cfg = self.config
        
        if cfg["benchmark"]["mode"]:
            if cfg["benchmark"]["level"] == "basic":
                arr.insert(0, "-benchmark")
            elif cfg["benchmark"]["level"] == "all":
                arr.insert(0, "-benchmark_all")
            else:
                print("No available method for benchmark %s" % cfg["benchmark"]["level"])
        
        arr.insert(0, "-nostdin")
        arr.insert(0, "-hide_banner")
        
        if cfg["logging"]["mode"]:
            arr.insert(0, "-loglevel %s" % cfg["logging"]["level"])
        
        if cfg["set_threads"]["mode"]:
            arr.insert(0, "-threads %s" % cfg["set_threads"]["count"])
        
        arr.insert(0, ("-y" if cfg["overwrite"] else "-n"))
        
        arr.insert(0, "ffmpeg")
        
        if len(self.inputList) > 0:
            arr.insert(1, " ".join(self.inputList))
            
        if self.output:
            arr.append(self.output)
            
            self.inputList = []
            self.output = ""
        
        if cfg["priority"]["mode"]:
            arr.insert(0, "nice -%s" % cfg["priority"]["level"])
        
        query = " ".join(arr)
        
        if self.title:
            print()
            print("-+" * 10, end="-\n")
            print("Name: %s" % self.title)
            
            self.title = ""
            
            print("--" * 10)
        else:
            print("-+" * 10, end="-\n")
        
        print(query)
        print("-+" * 10, end="-\n")
        
        
        res = (cmd(query) if run else 0)
        
        if res is 0 and run is True:
            state = "success"
        elif run is False:
            state = "failed"
        else:
            state = "error"
        
        self.cmdLog.append(( state, query ))
        
        assert res == 0, "\nCurrent Command:\n\t%s" % query
        
    
