#!/usr/bin/env python3
# -*- coding UTF-8 -*-

# Require `sox` package from terminal
# 'apt install sox -y`

from os import system
from os import name as osName
from os.path import join, isfile
from __includes__.config import Config
from __includes__.helpers import createDir

class Notification:
    
    bundles = [
        {
            "success" : "mixkit-quick-win-video-game-notification-269.wav",
            "error" : "windows_xp_error.mp3",
        },
        {
            "success" : "mixkit-unlock-game-notification-253.wav",
            "error" : "windows_xp_error.mp3",
        },
        {
            "success" : "mixkit-arcade-score-interface-217.wav",
            "error" : "windows_xp_error.mp3",
        },
        {
            "success" : "notification sound.mp3",
            "error" : "windows_xp_error.mp3",
        }
    ]
    
    config = Config()
    
    ps = False # Mute. Bool
    
    __isInitiated = False
    __status = "ok"
    
    subFolders = {
        "ringtone" : "media",
        "runtime" : "temp"
    }
    
    # posix == Termux for sure and ???
    # nt == Windows
    ENVs = ["posix"]
    logs = []
    
    driver = object
    
    def __init__(self, selected=1):
        
        self.sounds = {
            "success" : self.bundles[selected]["success"],
            "error" : self.bundles[selected]["error"]
        }
        
        # Python version 3.10 and after #
        # Import What we need 
        match osName:
            case "posix":
                from __includes__.assets.Notification.drivers.PosixSoundPlayer import PosixSoundPlayer
                self.driver = PosixSoundPlayer()
            case default:
                self.addLog("System environment is not supported", "error")
                return None
        
        if self.__isInitiated:
            self.addLog("Already initiated", "log")
            return None
        
        self.objName = self.__class__.__name__
        
        # Object Parent Directory
        a = self.config.getDirectories().get("assets")
        self.path = join(a, self.objName)
        
        # Main Path
        createDir(self.path)
        
        # Create Object Self Base Directory
        self.__createDirectories()
        
        # Check in-use assets is existing
        self.__chkAudio()
        
        # Check if `sox.play` is available
        self.__chkPackage()
        
        self.__isInitiated = True
    
    # Init system
    def __createDirectories(self):
        for k, v in self.subFolders.items():
            a = join(self.path, v)
            createDir(a)
    
    # Check systen
    def __chkAudio(self):
        
        arr = []
        for index in self.sounds:
            n = join(self.path, self.subFolders["ringtone"], self.sounds[index])
            
            if not isfile(n):
                arr.append(n)
            
        
        if len(arr) > 0:
            print("Notification missing audio file(s):")
            self.addLog("Some Audio File does not exists.", "error")
            for x in arr:
                print("\t%s" % x)
            
            print("")
            
            print("\nCannot start.")
            exit(1)
    
    def __chkPackage(self):
        
        # Print it into black hole. Hahaha
        out = system("play --version > /dev/null")
        
        # `is not` only works for variables
        if out != 0:
            print("`sox` package is not available.")
            self.addLog("sox package is not installed", "error")
            self.__status = "error"
        
    # Create query and evaluate
    def __call(self, audio):
        # Package, No Output
        cmd = ["play", "-q"]
        
        cmd.append(join(self.path,self.subFolders["ringtone"], audio))
        
        if not self.ps:
            system(" ".join(cmd))
    
    # Play sound. Notification Trigger
    def error(self):
        if self.__status == "ok" and osName in self.ENVs:
            self.__call(self.sounds["error"])
        
    def success(self):
        if self.__status == "ok" and osName in self.ENVs:
            self.__call(self.sounds["success"])
    
    # Mute 
    def mute(self):
        self.ps = True
    # Loggings
    def addLog(self, message, status):
        self.logs.append({
            "message" : message,
            "status" : status
        })
    
    def getLogs(self):
        return self.logs
    
