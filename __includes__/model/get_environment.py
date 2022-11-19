#!/usr/bin/env python3
# -*- coding UTF-8 -*-
# 
# @Package Name TLVC (Time Lapse Video Creator)
#
# Get Current Environment

from __includes__.envres import envRes
import os, re, sys

class Get_Environment:
    def __init__(self) -> None:
        # Get the parent process name.
        
        if self.isWindow():
            try:
                import psutil

                self.pprocName = psutil.Process(os.getppid()).name()

                pwrshll:bool = self.isPowerShell()
                cmd:bool = self.isCommandPrompt()

                """
                Raise exception if both pwrshll and cmd are true
                We cannot make any system command due to environment collision
                """
                
                if pwrshll:
                    envRes.set("ENV", "powershell")
                
                elif cmd:
                    envRes.set("ENV", "cmd")
                
                else:
                    raise Exception("Cannot Start: Unknown Environment")
                
            except BaseException as BE:
                raise Exception("Cannot Start: Unknown Environment")
                
        elif self.isLinux():
            envRes.set("ENV", "linux")
        
        else:
            envRes.set("ENV", "null")

    
    def isWindow(self) -> bool:
        try:
            name:str = os.name
            platform:str = sys.platform
            env:str = os.environ.get("OS")

            if name == "nt" or platform == "win32" or env == "Windows_NT":
                return True
        except:
            pass

        return False
    
    def isLinux(self):
        try:
            name:str = os.name
            platform:str = sys.platform
            env:str = os.environ.get("OS")

            if name == "posix" or platform == "linux" or env == None:
                return True
        except:
            pass

        return False


    def isPowerShell(self):
        # https://stackoverflow.com/questions/55597797/detect-whether-current-shell-is-powershell-in-python/55598796#55598796

        # See if it is Windows PowerShell (powershell.exe) or PowerShell Core (pwsh[.exe]):
        return bool(re.fullmatch('pwsh|pwsh.exe|powershell.exe', self.pprocName))

    def isCommandPrompt(self):
        return bool(re.fullmatch('cmd|cmd.exe|commandprompt.exe|command.exe|command', self.pprocName))
