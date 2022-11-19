#!/usr/bin/env python3
# -*- coding UTF-8 -*-
# 
# @Package Name TLVC (Time Lapse Video Creator)
#
# Get Current Environment
from __includes__.envres import envRes
import os, psutil, re

class Get_Environment:
    def __init__(self) -> None:
        # Get the parent process name.
        self.pprocName = psutil.Process(os.getppid()).name()

        print(self.pprocName)

        self.isPowerShell()

        pass

    def isPowerShell(self):
        # https://stackoverflow.com/questions/55597797/detect-whether-current-shell-is-powershell-in-python/55598796#55598796

        # See if it is Windows PowerShell (powershell.exe) or PowerShell Core (pwsh[.exe]):
        return bool(re.fullmatch('pwsh|pwsh.exe|powershell.exe', self.pprocName))

    def isCommandPrompt(self):
        return bool(re.fullmatch('cmd|cmd.exe|commandprompt.exe|command.exe|command', self.pprocName))
