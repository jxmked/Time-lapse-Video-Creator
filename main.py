#!/user/bin/env python3

from sys import path
from os import path as opath
from os import system as console
from sys import argv as params

path.append("__include__/.")

from xTools import xTools
from Timer import Timer
from FFMPEG import FFMPEG as fmpg
from Videos import Videos
from Audio import Audio


if params[0] == opath.basename(__file__):
    params.pop(0)

class Main:
    
    ERR = []
    FLAGS = ["notOnly"]
    toClean = False
    
    def __init__(self):
        self.rscOut = "Resource Out"
        self.V = Videos()
        self.A = Audio()
        self.FMG = fmpg()
        
        self.V.xtl = xTools
        self.A.xtl = xTools
        self.xtl = xTools
        self.FMG.xtl = xTools
        self.V.execute = self.FMG.execute
        self.A.execute = self.FMG.execute
        self.V.fOutput = self.rscOut
        self.A.fOutput = self.rscOut
        self.V.A = self.A
        self.A.V = self.V
        self.timer = Timer()
        pass 
    
    def initialize(self):
        self.V.initialize()
        self.A.initialize()
        
        self.ERR.append(self.FMG.initialize())
        
        ## Checking and installing soundFile module
        print("\n\nChecking `soundFile` if installed in python")
        try:
            import soundFile
        except:
            if not self.xtl.isInTermux():
                print("Unable to automatically install libraries/packages.")
                print("Please install manually in python...\n")
                print("soundFile")
                exit(0)
            
            print("python3 -m pip install soundFile")
            if not console("python3 -m pip install soundFile --no-input") == 0:
                self.ERR.append(1)
        
        
        print("\n\nReady To Run")
    
    
    def start(self):
        self.timer.start()
        
        self.A.start(True)
        self.V.start(True)
        
        self.timer.end()
        
        print("~-" * 10, end="~\n")
        self.timer.printLapse("Finished")
        print("-~" * 10, end="-\n")
        
        if self.toClean:
            self.cleanUp()
        
    def only(self):
        self.FLAGS[0] = "only"
        pass
        
    def _help(self):
        exit(0)
        pass
    
    def fading(self, param):
        self.V.fading(param)
        self.A.fading(param)
        pass
    
    def merge(self):
        pass
    
    def setFadeOut(self, param):
        self.V.fadeOut(param)
        self.A.fadeOut(param)
        pass
    
    def setFadeIn(self, param):
        self.V.fadeIn(param)
        self.A.fadeIn(param)
        pass
    
    def cleanUpAfter(self):
        print("Warning: All Files System Generated File will be deleted after compiling except the Final Compiled Video.")
        self.toClean = True
        pass
    
    def arg_initClean(self):
        self.cleanUp()
        exit(0)
    
    def cleanUp(self):
        
        fr = [
            self.V.fOutput, 
         #   self.V.fInput,
            self.V.fDuplicatedRemoved,
           # self.A.fInput,
            self.A.fTrimmed
        ]
        print("Clearing up!")
        
        for s in fr:
            for file in self.xtl.getFiles(s, "any"):
                aPath = self.xtl.joinPath(s, file)
                self.xtl.deleteFile(aPath)
                
                print("%s" % aPath)
        
        
    
obj = Main()

# Declaration of key-value pair is important
DECLARED = []
FLAGS = {
   # "-help" : obj._help,
   # "-h" : obj._help,
    
    "-init" : {
        "func" : obj.initialize,
        "description" : "Automatically install some required Libraries/Packages and create Folders "
    },
    "-i" : {
        "func" : obj.initialize,
        "description" : "Automatically install some required Libraries/Packages and create Folders "
    },
    
    "-cleanAfter" : {
        "func" : obj.cleanUpAfter,
        "description" : "Clear all system generated files except final compiled video."
    },
    
    # Since, we only have remove Duplicated option...
    #"-only" : obj.only, # Only Triggered Flag To Init
    
    "-remove_duplicated" : {
        "func" : obj.V.initRemoveDuplicatedFrames, # Remove Duplicated Frames
        "description" : "Init Remove Duplicated Frames Only"
    },
    "-crossfadeDuration:" : {
        "func" : obj.A.setCrossFadeDuration,
        "description" : "Set custom Crossfade Duration in Audio. Effective when having multiple Audio File."
    },
    
    # Currently not available
    # "-merge" : obj.merge, # Merge all videos from V.fDuplicatedRemoved
    
    "-fading:" : {
        "func" : obj.fading,
        "description" : "Set custom fade-in-out in both music and video"
    },
    "-fadeOut:" : {
        "func" : obj.setFadeOut,
        "description" : "Set custom fade-out in Music and Video."
    },
    
    "-fadeIn:" : {
        "func" : obj.setFadeIn,
        "description" : "Set custom fade-in in Music and Video."
    },
    
    "-vFading:" : {
        "func" : obj.V.fading,
        "description" : "Set custom fade-in-out duration in Video"
    },
    
    "-vFadeIn:" : {
        "func" : obj.V.fadeIn,
        "description" : "Set custom fade-in duration in Video"
    },
    
    "-vFadeOut:" : {
        "func" : obj.V.fadeOut,
        "description" : "Set custom fade-out duration in Video"
    },
    
    "-aFading:" : {
        "func" : obj.A.fading,
        "description" : "Set custom fade-in-out duration in Audio"
    },
    
    "-aFadeIn:" : {
        "func" : obj.A.fadeIn,
        "description" : "Set custom fade-in duration in Audio"
    },
    
    "-aFadeOut:" : {
        "func" : obj.A.fadeOut,
        "description" : "Set custom fade-out duration in Audio"
    },
    
    "-overwrite" : {
        "func" : obj.FMG.overwriteFlag,
        "description" : "Overwrite all existing files with new one. Old files will be replace by new generated files."
    },
    
    "-start" : {
        "func" : obj.start,
        "description" : "Start Compiling"
    },
    
    "-s" : {
        "func" : obj.start,
        "description" : "Start Compiling"
    },
    
    "-cleanNow" : {
        "func" : obj.arg_initClean,
        "description" : "Clean All System Generated Files after execution. Files from input folders and Final Compiled Video `Output.mp4` is not included."
    }
}


# Parameter Handler
if len(params) == 0:
    obj._help()
else:
    variabled = {} # Store all Flags with variables
    for index in range(len(params)):
        s = params[index].split(":")
        
        if len(s) == 2:
            variabled[s[0] + ":"] = s[1]
            params[index] = s[0] + ":"
        
    
    
    # Check if all params are existing in dict
    for param in params:
        if not param in FLAGS:
            raise Exception("'%s' is not a valid parameter" % param)
    
    
    for key in FLAGS:
        if key in params:
            if key in DECLARED:
                print("Already Triggered: %s. Unable to start" % key)
                exit(0)
            
            DECLARED.append(key)
            
            # If Flag has Value
            if key in variabled:
                FLAGS[key]['func'](variabled[key])
                continue
            
            # If Flag has No Value
            FLAGS[key]['func']()
            
        

# Flags 

"""
-init = Install All Requirements
-start = Start Compiling 
"""