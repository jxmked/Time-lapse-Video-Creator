#!/usr/bin/env python3

from os import system as console

class FFMPEG:
    def __init__(self):
        self.overwrite = False
        self.xtl = {}
        pass
    
    # @Param: Array
    def execute(self, cmd):
        if not isinstance(cmd, list):
            raise Exception("Not an array")
        
        if self.overwrite:
            cmd.insert(0, "-y")
        
        # Lessen too much info about ffmpeg
        cmd.insert(0, "-hide_banner")
        
        if console("ffmpeg %s" % (" ".join(cmd))) == 0:
            return 0
        
        raise Exception("Error while executing ffmpeg command")
    
    def overwriteFlag(self):
        self.overwrite = True
        
    def initialize(self):
        if not self.xtl.isInTermux():
            print("Unable to install packages and libraries in not Termux environment")
            print("Please, install manually in your environment...\n")
            print("ffmpeg")
            exit(0)
        
        print("Checking and Installing `ffmpeg`")
        print("pkg install ffmpeg -y")
        if not console("pkg install ffmpeg -y") == 0:
            print("\nError: ")
            print("Something went wrong while installing `ffmpeg`")
            print("Required Package/Library unable to download\n")
            return 1