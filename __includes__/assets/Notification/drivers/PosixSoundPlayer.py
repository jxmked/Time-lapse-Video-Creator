#! /usr/bin/env python3
# -*- coding UTF-8 -*-

# @Package Name TLVC (Time Lapse Video Creator)

## Using `sox.play` to play audio files
### 'pkg isntall sox -y'

from __includes__.assets.Notification.drivers.driver import Driver

class PosixSoundPlayer(Driver):
    # Valid Exit Code
    validExitCode = [0, 256]
    
    def __init__(self):
        super().__init__()
        
        ## For Development ##
        #self.noExitError()
        #self.noRaise()
        
        self.setPackage("play")
        
    def playSound(self, path):
        self.sound(path, "-q")