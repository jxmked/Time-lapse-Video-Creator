#!/usr/bin/env python3
# -*- coding UTF-8 -*-

# @Package Name TLVC (Time Lapse Video Creator)

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
        }, {
            "success" : "mixkit-unlock-game-notification-253.wav",
            "error" : "windows_xp_error.mp3",
        }, {
            "success" : "mixkit-arcade-score-interface-217.wav",
            "error" : "windows_xp_error.mp3",
        }, {
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
        
        ## Python version 3.10 and after ##
        # Import what we need 
        match osName:
            case "posix":
                from __includes__.assets.Notification.drivers.PosixSoundPlayer import PosixSoundPlayer
                self.driver = PosixSoundPlayer()
            case default:
                self.addLog("System environment is not supported", "error")
                raise Exception("System environment is not supported")
        
        if self.__isInitiated:
            self.addLog("Already initiated", "log")
            return None
        
        self.objName = self.__class__.__name__
        
        # Object Parent Directory
        a = self.config.getDirectories().get("assets")
        self.path = join(a, self.objName)
        
        # Main Path
        createDir(self.path)
        
        # Check audio if existing.
        self.driver.audioList([join(self.path, self.subFolders["ringtone"], v) for k, v in self.sounds.items()])
        
        # Modify self.sound to actual path
        for k, v in self.sounds.items():
            self.sounds[k] = join(self.path, self.subFolders["ringtone"], v)
        
        self.__isInitiated = True
        
    
    # Play sound. Notification Trigger
    def error(self):
        if self.__status == "ok" and osName in self.ENVs:
            self.driver.playSound(self.sounds["error"])
        
    def success(self):
        if self.__status == "ok" and osName in self.ENVs:
            self.driver.playSound(self.sounds["success"])
    
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
    
